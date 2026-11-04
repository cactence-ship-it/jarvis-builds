//! Offline-first orchestration primitives. No provider network calls are implemented.

pub mod guard;

/// System prompt for model providers: senior-engineer conduct and the report format
/// that `guard::scan_engineering_report` checks. Single source; the owner-facing copy
/// in kartal-s-twin/agents/GPT_DAVRANIS_KURALLARI.md points here.
pub const ENGINEER_SYSTEM_PROMPT: &str = include_str!("../prompts/engineer_tr.txt");

/// Full request text for a provider: engineer rules, then the task instruction.
pub fn engineer_prompt(instruction: &str) -> String {
    format!("{ENGINEER_SYSTEM_PROMPT}\nGÖREV\n{}\n", instruction.trim())
}

use std::collections::HashSet;
use std::fs::{File, OpenOptions};
use std::io::{self, Write};
use std::path::Path;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Task {
    pub id: String,
    pub input_commit: String,
    pub provider: ProviderKind,
    pub estimated_cost_micros: u64,
    pub instruction: String,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ProviderKind {
    Mock,
    OpenAi,
    Anthropic,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum BlockReason {
    PaidDispatchDisabled,
    BudgetExceeded,
    EmptyTaskId,
    EmptyCommit,
    EmptyInstruction,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Policy {
    /// Paid providers remain disabled until a future, explicit owner-authorised release.
    pub paid_dispatch_enabled: bool,
    pub per_run_budget_micros: u64,
    pub spent_micros: u64,
    pub max_attempts: u8,
}

impl Default for Policy {
    fn default() -> Self {
        Self {
            paid_dispatch_enabled: false,
            per_run_budget_micros: 0,
            spent_micros: 0,
            max_attempts: 3,
        }
    }
}

impl Policy {
    pub fn authorize(&self, task: &Task) -> Result<(), BlockReason> {
        if task.id.trim().is_empty() {
            return Err(BlockReason::EmptyTaskId);
        }
        if task.input_commit.trim().is_empty() {
            return Err(BlockReason::EmptyCommit);
        }
        if task.instruction.trim().is_empty() {
            return Err(BlockReason::EmptyInstruction);
        }
        if task.provider != ProviderKind::Mock && !self.paid_dispatch_enabled {
            return Err(BlockReason::PaidDispatchDisabled);
        }
        let total = self.spent_micros.saturating_add(task.estimated_cost_micros);
        if total > self.per_run_budget_micros {
            return Err(BlockReason::BudgetExceeded);
        }
        Ok(())
    }

    pub fn record_spend(&mut self, amount_micros: u64) -> Result<(), BlockReason> {
        let next = self.spent_micros.saturating_add(amount_micros);
        if next > self.per_run_budget_micros {
            return Err(BlockReason::BudgetExceeded);
        }
        self.spent_micros = next;
        Ok(())
    }
}

/// Stable key for deduplicating a task against a particular input revision.
pub fn idempotency_key(task: &Task) -> String {
    format!(
        "{}:{}:{:?}",
        task.id.trim(),
        task.input_commit.trim(),
        task.provider
    )
}

pub fn retry_delay_seconds(attempt: u8, max_attempts: u8) -> Option<u64> {
    if attempt == 0 || attempt >= max_attempts {
        return None;
    }
    Some(
        1_u64
            .checked_shl(u32::from(attempt - 1))
            .unwrap_or(u64::MAX)
            .min(60),
    )
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ProviderResponse {
    pub text: String,
    pub input_tokens: u64,
    pub output_tokens: u64,
}

pub trait Provider {
    fn kind(&self) -> ProviderKind;
    fn execute(&self, instruction: &str) -> Result<ProviderResponse, String>;
}

/// Deterministic provider for tests and offline development; it never accesses a network.
pub struct MockProvider;
impl Provider for MockProvider {
    fn kind(&self) -> ProviderKind {
        ProviderKind::Mock
    }
    fn execute(&self, instruction: &str) -> Result<ProviderResponse, String> {
        Ok(ProviderResponse {
            text: format!("MOCK_ONLY: {}", instruction.trim()),
            input_tokens: 0,
            output_tokens: 0,
        })
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Review {
    pub reviewer: String,
    pub reviewed_commit: String,
    pub accepted: bool,
}

/// A review is valid only for the exact commit and a different reviewer.
pub fn review_is_valid(review: &Review, author: &str, current_commit: &str) -> bool {
    !review.reviewer.trim().is_empty()
        && review.reviewer != author
        && review.reviewed_commit == current_commit
        && review.accepted
}

pub fn append_audit(path: &Path, event: &str) -> io::Result<()> {
    let safe = event.replace(['\n', '\r'], " ");
    let mut file: File = OpenOptions::new().create(true).append(true).open(path)?;
    writeln!(file, "{}", safe)
}

/// Tracks dispatch keys within one process. Persistent queue state remains in the existing YAML system.
#[derive(Default)]
pub struct DispatchLedger {
    seen: HashSet<String>,
}
impl DispatchLedger {
    pub fn claim(&mut self, key: String) -> bool {
        self.seen.insert(key)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn task(provider: ProviderKind) -> Task {
        Task {
            id: "T-001".into(),
            input_commit: "abc123".into(),
            provider,
            estimated_cost_micros: 0,
            instruction: "inspect task".into(),
        }
    }

    #[test]
    fn paid_dispatch_is_off_by_default() {
        assert_eq!(
            Policy::default().authorize(&task(ProviderKind::OpenAi)),
            Err(BlockReason::PaidDispatchDisabled)
        );
        assert!(Policy::default()
            .authorize(&task(ProviderKind::Mock))
            .is_ok());
    }

    #[test]
    fn budget_is_a_hard_ceiling() {
        let mut p = Policy {
            per_run_budget_micros: 100,
            ..Policy::default()
        };
        assert!(p.record_spend(80).is_ok());
        assert_eq!(p.record_spend(21), Err(BlockReason::BudgetExceeded));
        assert_eq!(p.spent_micros, 80);
    }

    #[test]
    fn retry_count_is_bounded() {
        assert_eq!(retry_delay_seconds(1, 3), Some(1));
        assert_eq!(retry_delay_seconds(2, 3), Some(2));
        assert_eq!(retry_delay_seconds(3, 3), None);
    }

    #[test]
    fn duplicate_dispatch_is_rejected() {
        let mut ledger = DispatchLedger::default();
        assert!(ledger.claim("T-001:abc:Mock".into()));
        assert!(!ledger.claim("T-001:abc:Mock".into()));
        assert!(ledger.claim("T-001:def:Mock".into()));
    }

    #[test]
    fn review_must_be_independent_and_match_current_commit() {
        let r = Review {
            reviewer: "claude".into(),
            reviewed_commit: "abc".into(),
            accepted: true,
        };
        assert!(review_is_valid(&r, "openai", "abc"));
        assert!(!review_is_valid(&r, "claude", "abc"));
        assert!(!review_is_valid(&r, "openai", "new-sha"));
    }

    #[test]
    fn mock_provider_is_deterministic_and_offline() {
        let result = MockProvider.execute("hello").unwrap();
        assert_eq!(result.text, "MOCK_ONLY: hello");
        assert_eq!(result.input_tokens, 0);
    }

    #[test]
    fn engineer_prompt_wraps_the_task() {
        let p = engineer_prompt("  lastik zarfını kontrol et \n");
        assert!(p.starts_with("ROL: BAŞ MÜHENDİS"));
        assert!(p.ends_with("GÖREV\nlastik zarfını kontrol et\n"));
    }

    #[test]
    fn invalid_task_is_rejected() {
        let mut t = task(ProviderKind::Mock);
        t.id.clear();
        assert_eq!(
            Policy::default().authorize(&t),
            Err(BlockReason::EmptyTaskId)
        );
    }
}
