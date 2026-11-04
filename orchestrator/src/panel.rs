//! Three-partner collaboration: OpenAI (GPT), Anthropic (Claude) and Google (Gemini).
//!
//! One partner authors a change; the other two review the exact commit independently.
//! The change is approved only when both reviewers accept that commit. A single
//! rejection blocks it; a split decision goes to the owner. No partner can review its
//! own work, and a review of an older commit counts for nothing.
//!
//! Approval here never merges anything: merging stays an owner action.

use crate::ProviderKind;

/// The three working partners, in authoring rotation order.
pub const PARTNERS: [ProviderKind; 3] = [
    ProviderKind::OpenAi,
    ProviderKind::Anthropic,
    ProviderKind::Gemini,
];

impl ProviderKind {
    pub fn name(self) -> &'static str {
        match self {
            ProviderKind::Mock => "mock",
            ProviderKind::OpenAi => "openai",
            ProviderKind::Anthropic => "anthropic",
            ProviderKind::Gemini => "gemini",
        }
    }

    /// Environment variable the runner reads the provider key from. Never stored in the repo.
    pub fn api_key_env(self) -> Option<&'static str> {
        match self {
            ProviderKind::Mock => None,
            ProviderKind::OpenAi => Some("OPENAI_API_KEY"),
            ProviderKind::Anthropic => Some("ANTHROPIC_API_KEY"),
            ProviderKind::Gemini => Some("GEMINI_API_KEY"),
        }
    }
}

/// Author for the n-th task (0-based): GPT, Claude, Gemini, GPT, ...
/// Rotation keeps any single partner from authoring and steering everything.
pub fn author_for(task_index: usize) -> ProviderKind {
    PARTNERS[task_index % PARTNERS.len()]
}

/// The two partners that must review the author's change.
pub fn reviewers_for(author: ProviderKind) -> Vec<ProviderKind> {
    PARTNERS.iter().copied().filter(|p| *p != author).collect()
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct PanelReview {
    pub reviewer: ProviderKind,
    pub reviewed_commit: String,
    pub accepted: bool,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum PanelDecision {
    /// Both reviewers accepted the current commit. Ready for the owner to merge.
    Approved,
    /// Every counted review rejected the current commit.
    Rejected { by: Vec<ProviderKind> },
    /// One accepted, one rejected: the owner decides.
    Disputed {
        accepted_by: Vec<ProviderKind>,
        rejected_by: Vec<ProviderKind>,
    },
    /// Still waiting for these reviewers on the current commit.
    Pending { missing: Vec<ProviderKind> },
}

/// Decide on a change from the reviews collected so far.
///
/// Counted reviews: by one of the author's two reviewers, for exactly `current_commit`.
/// If a reviewer reviewed the same commit more than once, its latest review counts.
/// A rejection is decisive as soon as it arrives, so the author can start fixing
/// without waiting for the second reviewer.
pub fn decide(
    author: ProviderKind,
    current_commit: &str,
    reviews: &[PanelReview],
) -> PanelDecision {
    let reviewers = reviewers_for(author);
    let mut accepted_by = Vec::new();
    let mut rejected_by = Vec::new();
    let mut missing = Vec::new();

    for r in &reviewers {
        let latest = reviews
            .iter()
            .rev()
            .find(|x| x.reviewer == *r && x.reviewed_commit == current_commit);
        match latest {
            Some(x) if x.accepted => accepted_by.push(*r),
            Some(_) => rejected_by.push(*r),
            None => missing.push(*r),
        }
    }

    match (accepted_by.is_empty(), rejected_by.is_empty()) {
        (false, false) => PanelDecision::Disputed {
            accepted_by,
            rejected_by,
        },
        (_, false) => PanelDecision::Rejected { by: rejected_by },
        _ if missing.is_empty() => PanelDecision::Approved,
        _ => PanelDecision::Pending { missing },
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use ProviderKind::{Anthropic, Gemini, OpenAi};

    fn rv(reviewer: ProviderKind, sha: &str, accepted: bool) -> PanelReview {
        PanelReview {
            reviewer,
            reviewed_commit: sha.into(),
            accepted,
        }
    }

    #[test]
    fn authorship_rotates_through_all_three() {
        let first: Vec<_> = (0..6).map(author_for).collect();
        assert_eq!(
            first,
            vec![OpenAi, Anthropic, Gemini, OpenAi, Anthropic, Gemini]
        );
    }

    #[test]
    fn each_author_gets_the_other_two_as_reviewers() {
        assert_eq!(reviewers_for(OpenAi), vec![Anthropic, Gemini]);
        assert_eq!(reviewers_for(Anthropic), vec![OpenAi, Gemini]);
        assert_eq!(reviewers_for(Gemini), vec![OpenAi, Anthropic]);
    }

    #[test]
    fn approval_needs_both_reviewers_on_the_exact_commit() {
        let one = [rv(Anthropic, "abc", true)];
        assert_eq!(
            decide(OpenAi, "abc", &one),
            PanelDecision::Pending {
                missing: vec![Gemini]
            }
        );
        let both = [rv(Anthropic, "abc", true), rv(Gemini, "abc", true)];
        assert_eq!(decide(OpenAi, "abc", &both), PanelDecision::Approved);
    }

    #[test]
    fn self_review_does_not_count() {
        let reviews = [
            rv(OpenAi, "abc", true),
            rv(OpenAi, "abc", true),
            rv(Gemini, "abc", true),
        ];
        assert_eq!(
            decide(OpenAi, "abc", &reviews),
            PanelDecision::Pending {
                missing: vec![Anthropic]
            }
        );
    }

    #[test]
    fn a_new_commit_invalidates_old_approvals() {
        let reviews = [rv(Anthropic, "old", true), rv(Gemini, "old", true)];
        assert_eq!(
            decide(OpenAi, "new", &reviews),
            PanelDecision::Pending {
                missing: vec![Anthropic, Gemini]
            }
        );
    }

    #[test]
    fn one_rejection_blocks_and_a_split_goes_to_the_owner() {
        let rejected = [rv(Gemini, "abc", false)];
        assert_eq!(
            decide(Anthropic, "abc", &rejected),
            PanelDecision::Rejected { by: vec![Gemini] }
        );
        let split = [rv(OpenAi, "abc", true), rv(Gemini, "abc", false)];
        assert_eq!(
            decide(Anthropic, "abc", &split),
            PanelDecision::Disputed {
                accepted_by: vec![OpenAi],
                rejected_by: vec![Gemini]
            }
        );
    }

    #[test]
    fn latest_review_by_the_same_reviewer_wins() {
        let reviews = [
            rv(Gemini, "abc", false),
            rv(Gemini, "abc", true),
            rv(Anthropic, "abc", true),
        ];
        assert_eq!(decide(OpenAi, "abc", &reviews), PanelDecision::Approved);
    }

    #[test]
    fn keys_come_from_separate_environment_variables() {
        assert_eq!(Gemini.api_key_env(), Some("GEMINI_API_KEY"));
        assert_eq!(ProviderKind::Mock.api_key_env(), None);
        let envs: Vec<_> = PARTNERS.iter().filter_map(|p| p.api_key_env()).collect();
        assert_eq!(envs.len(), 3);
    }
}
