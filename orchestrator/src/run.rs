//! One panel run: the author writes an engineering report for a task, the guard checks
//! it, and the other two partners review it. Every paid call is charged against the
//! owner's budget before it is made. Nothing is written to git and nothing is merged.

use crate::guard::{self, Verdict};
use crate::panel::{self, PanelDecision, PanelReview};
use crate::providers::{HttpProvider, Transport};
use crate::{BlockReason, Policy, ProviderKind, ProviderResponse, Task, ENGINEER_SYSTEM_PROMPT};

/// A partner the panel can call. Implemented by `HttpProvider` and by test fakes.
pub trait Partner {
    fn kind(&self) -> ProviderKind;
    fn model(&self) -> &str;
    fn worst_case_cost_micros(&self, system: &str, user: &str) -> u64;
    fn actual_cost_micros(&self, r: &ProviderResponse) -> u64;
    fn complete(&self, system: &str, user: &str) -> Result<ProviderResponse, String>;
}

impl<T: Transport> Partner for HttpProvider<T> {
    fn kind(&self) -> ProviderKind {
        self.config.kind
    }
    fn model(&self) -> &str {
        &self.config.model
    }
    fn worst_case_cost_micros(&self, system: &str, user: &str) -> u64 {
        self.config.worst_case_cost_micros(system, user)
    }
    fn actual_cost_micros(&self, r: &ProviderResponse) -> u64 {
        self.config.actual_cost_micros(r)
    }
    fn complete(&self, system: &str, user: &str) -> Result<ProviderResponse, String> {
        HttpProvider::complete(self, system, user)
    }
}

/// Owner switches, read from the runner environment:
/// `KARTAL_PAID_DISPATCH=on` (kill switch; anything else blocks every paid call) and
/// `KARTAL_RUN_BUDGET_MICROS` (USD micro-dollars this run may spend; missing means 0).
pub fn policy_from_lookup(get: impl Fn(&str) -> Option<String>) -> Result<Policy, String> {
    let enabled = get("KARTAL_PAID_DISPATCH").is_some_and(|v| v.trim() == "on");
    let budget = match get("KARTAL_RUN_BUDGET_MICROS").filter(|v| !v.trim().is_empty()) {
        Some(v) => v
            .trim()
            .parse::<u64>()
            .map_err(|_| "KARTAL_RUN_BUDGET_MICROS is not a whole number".to_string())?,
        None => 0,
    };
    Ok(Policy {
        paid_dispatch_enabled: enabled,
        per_run_budget_micros: budget,
        ..Policy::default()
    })
}

/// Content id of the report: reviews are bound to exactly this text.
pub fn report_id(report: &str) -> String {
    let mut h: u64 = 0xcbf2_9ce4_8422_2325;
    for b in report.as_bytes() {
        h ^= u64::from(*b);
        h = h.wrapping_mul(0x0100_0000_01b3);
    }
    format!("r{h:016x}")
}

pub fn review_prompt(author: ProviderKind, task: &str, report: &str, id: &str) -> String {
    format!(
        "İNCELEME GÖREVİ\n\
         Aşağıdaki rapor {author} tarafından aşağıdaki görev için yazıldı. Rapor kimliği: {id}\n\
         Raporu bağımsız incele. Yazarın iddialarını kanıt sayma; kanıt yoksa bunu bulgu olarak yaz.\n\n\
         Yanıt biçimi:\n\
         1. satır, tam olarak: KARAR: KABUL  ya da  KARAR: RET\n\
         2. satır, tam olarak: İNCELENEN: {id}\n\
         Sonra her bulgu için: rapor bölümü veya dosya:satır, sorun, önerilen düzeltme.\n\n\
         GÖREV\n{task}\n\nRAPOR\n{report}\n",
        author = author.name(),
        task = task.trim(),
    )
}

/// Read a review's verdict. Only the exact two-line header counts; anything else is not
/// a review, so it cannot approve (or block) by accident.
pub fn parse_review(reviewer: ProviderKind, text: &str, id: &str) -> Option<PanelReview> {
    let mut lines = text.lines().map(str::trim).filter(|l| !l.is_empty());
    let accepted = match lines.next()? {
        "KARAR: KABUL" => true,
        "KARAR: RET" => false,
        _ => return None,
    };
    let reviewed = lines.next()?.strip_prefix("İNCELENEN:")?.trim();
    Some(PanelReview {
        reviewer,
        reviewed_commit: reviewed.to_string(),
        accepted: accepted && reviewed == id,
    })
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct CallRecord {
    pub role: &'static str,
    pub provider: ProviderKind,
    pub model: String,
    pub input_tokens: u64,
    pub output_tokens: u64,
    pub cost_micros: u64,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Outcome {
    /// Both reviewers accepted this exact report. The owner decides what happens next.
    Approved,
    /// The guard rejected the author's report before any review was paid for.
    GuardRejected,
    Panel(PanelDecision),
    /// Stopped before finishing: kill switch, budget, configuration or provider error.
    Blocked(String),
}

impl Outcome {
    pub fn label(&self) -> &'static str {
        match self {
            Outcome::Approved => "APPROVED",
            Outcome::GuardRejected => "REJECTED_BY_GUARD",
            Outcome::Panel(PanelDecision::Rejected { .. }) => "REJECTED",
            Outcome::Panel(PanelDecision::Disputed { .. }) => "DISPUTED",
            Outcome::Panel(PanelDecision::Pending { .. }) => "INCOMPLETE",
            Outcome::Panel(PanelDecision::Approved) => "APPROVED",
            Outcome::Blocked(_) => "BLOCKED",
        }
    }

    /// 0 approved, 1 owner decision needed, 2 rejected, 3 blocked.
    pub fn exit_code(&self) -> i32 {
        match self {
            Outcome::Approved | Outcome::Panel(PanelDecision::Approved) => 0,
            Outcome::Panel(PanelDecision::Disputed { .. })
            | Outcome::Panel(PanelDecision::Pending { .. }) => 1,
            Outcome::GuardRejected | Outcome::Panel(PanelDecision::Rejected { .. }) => 2,
            Outcome::Blocked(_) => 3,
        }
    }
}

#[derive(Debug, Clone)]
pub struct PanelRun {
    pub author: ProviderKind,
    pub report: Option<String>,
    pub report_id: Option<String>,
    pub report_findings: Vec<guard::Finding>,
    pub reviews: Vec<(ProviderKind, String)>,
    pub calls: Vec<CallRecord>,
    pub spent_micros: u64,
    pub budget_micros: u64,
    pub outcome: Outcome,
}

fn block_text(r: BlockReason) -> String {
    match r {
        BlockReason::PaidDispatchDisabled => {
            "paid dispatch is off (KARTAL_PAID_DISPATCH is not \"on\")".into()
        }
        BlockReason::BudgetExceeded => "the next call could exceed the run budget".into(),
        other => format!("{other:?}"),
    }
}

/// Charge-then-call: authorise the worst case, call, then record the real cost.
fn call(
    policy: &mut Policy,
    p: &dyn Partner,
    role: &'static str,
    user: &str,
    calls: &mut Vec<CallRecord>,
) -> Result<ProviderResponse, String> {
    let task = Task {
        id: format!("panel-{role}"),
        input_commit: "panel-run".into(),
        provider: p.kind(),
        estimated_cost_micros: p.worst_case_cost_micros(ENGINEER_SYSTEM_PROMPT, user),
        instruction: user.to_string(),
    };
    policy.authorize(&task).map_err(block_text)?;
    let r = p.complete(ENGINEER_SYSTEM_PROMPT, user)?;
    let cost = p.actual_cost_micros(&r);
    policy.charge(cost);
    calls.push(CallRecord {
        role,
        provider: p.kind(),
        model: p.model().to_string(),
        input_tokens: r.input_tokens,
        output_tokens: r.output_tokens,
        cost_micros: cost,
    });
    Ok(r)
}

/// Run the panel for one task. `partners` must contain the author and its two reviewers.
pub fn run_panel(
    task_text: &str,
    author: ProviderKind,
    partners: &[&dyn Partner],
    policy: &mut Policy,
) -> PanelRun {
    let mut run = PanelRun {
        author,
        report: None,
        report_id: None,
        report_findings: vec![],
        reviews: vec![],
        calls: vec![],
        spent_micros: 0,
        budget_micros: policy.per_run_budget_micros,
        outcome: Outcome::Blocked(String::new()),
    };
    let find = |k: ProviderKind| partners.iter().copied().find(|p| p.kind() == k);
    let finish = |mut run: PanelRun, policy: &Policy, outcome: Outcome| {
        run.spent_micros = policy.spent_micros;
        run.outcome = outcome;
        run
    };

    if task_text.trim().is_empty() {
        return finish(run, policy, Outcome::Blocked("task text is empty".into()));
    }
    let reviewers = panel::reviewers_for(author);
    for k in std::iter::once(author).chain(reviewers.iter().copied()) {
        if find(k).is_none() {
            return finish(
                run,
                policy,
                Outcome::Blocked(format!("partner {} is not configured", k.name())),
            );
        }
    }

    // 1. Author writes the engineering report.
    let author_p = find(author).expect("checked above");
    let report = match call(
        policy,
        author_p,
        "author",
        &format!("GÖREV\n{}", task_text.trim()),
        &mut run.calls,
    ) {
        Ok(r) => r.text,
        Err(e) => {
            return finish(
                run,
                policy,
                Outcome::Blocked(format!("author {}: {e}", author.name())),
            )
        }
    };
    let id = report_id(&report);
    run.report_findings = guard::scan_engineering_report(&report);
    run.report = Some(report.clone());
    run.report_id = Some(id.clone());

    // 2. The guard rejects before any review is paid for.
    if guard::verdict(&run.report_findings) == Verdict::Reject {
        return finish(run, policy, Outcome::GuardRejected);
    }

    // 3. Two independent reviews of exactly this report.
    let prompt = review_prompt(author, task_text, &report, &id);
    let mut panel_reviews = Vec::new();
    for k in reviewers {
        let p = find(k).expect("checked above");
        match call(policy, p, "reviewer", &prompt, &mut run.calls) {
            Ok(r) => {
                if let Some(rv) = parse_review(k, &r.text, &id) {
                    panel_reviews.push(rv);
                }
                run.reviews.push((k, r.text));
            }
            Err(e) => {
                return finish(
                    run,
                    policy,
                    Outcome::Blocked(format!("reviewer {}: {e}", k.name())),
                )
            }
        }
        // A rejection is decisive: do not pay for the second review.
        if matches!(
            panel::decide(author, &id, &panel_reviews),
            PanelDecision::Rejected { .. }
        ) {
            break;
        }
    }

    let outcome = match panel::decide(author, &id, &panel_reviews) {
        PanelDecision::Approved => Outcome::Approved,
        d => Outcome::Panel(d),
    };
    finish(run, policy, outcome)
}

fn usd(micros: u64) -> String {
    format!("${}.{:06}", micros / 1_000_000, micros % 1_000_000)
}

/// Markdown summary for the job page. Contains the model outputs, never keys or prompts.
pub fn render_markdown(run: &PanelRun) -> String {
    let mut s = String::new();
    s.push_str(&format!("# Panel run: {}\n\n", run.outcome.label()));
    s.push_str(&format!(
        "- Author: **{}**; reviewers: {}\n",
        run.author.name(),
        panel::reviewers_for(run.author)
            .iter()
            .map(|p| p.name())
            .collect::<Vec<_>>()
            .join(", ")
    ));
    if let Some(id) = &run.report_id {
        s.push_str(&format!("- Report id: `{id}`\n"));
    }
    s.push_str(&format!(
        "- Spent: {} of {} budget\n",
        usd(run.spent_micros),
        usd(run.budget_micros)
    ));
    match &run.outcome {
        Outcome::Blocked(why) => s.push_str(&format!("- Stopped: {why}\n")),
        Outcome::Panel(PanelDecision::Disputed { .. }) => {
            s.push_str("- Reviewers disagree: **the owner decides.**\n")
        }
        Outcome::Panel(PanelDecision::Pending { missing }) => s.push_str(&format!(
            "- No valid review from: {} (wrong header or report id)\n",
            missing
                .iter()
                .map(|p| p.name())
                .collect::<Vec<_>>()
                .join(", ")
        )),
        _ => {}
    }
    s.push_str("\n| Role | Provider | Model | In tokens | Out tokens | Cost |\n|---|---|---|---|---|---|\n");
    for c in &run.calls {
        s.push_str(&format!(
            "| {} | {} | {} | {} | {} | {} |\n",
            c.role,
            c.provider.name(),
            c.model,
            c.input_tokens,
            c.output_tokens,
            usd(c.cost_micros)
        ));
    }
    if !run.report_findings.is_empty() {
        s.push_str("\n## Guard findings on the report\n\n");
        for f in &run.report_findings {
            s.push_str(&format!(
                "- {} `{}` line {}: {}\n",
                f.severity.as_str(),
                f.rule,
                f.line,
                f.detail
            ));
        }
    }
    if let Some(r) = &run.report {
        s.push_str(&format!(
            "\n## Report ({})\n\n{}\n",
            run.author.name(),
            r.trim()
        ));
    }
    for (k, text) in &run.reviews {
        s.push_str(&format!("\n## Review ({})\n\n{}\n", k.name(), text.trim()));
    }
    s
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::cell::Cell;

    type Answer = Box<dyn Fn(&str) -> Result<String, String>>;

    /// Fake partner: fixed answer, fixed usage, counts its calls.
    struct Fake {
        kind: ProviderKind,
        answer: Answer,
        calls: Cell<u32>,
    }
    impl Fake {
        fn new(
            kind: ProviderKind,
            answer: impl Fn(&str) -> Result<String, String> + 'static,
        ) -> Self {
            Self {
                kind,
                answer: Box::new(answer),
                calls: Cell::new(0),
            }
        }
    }
    impl Partner for Fake {
        fn kind(&self) -> ProviderKind {
            self.kind
        }
        fn model(&self) -> &str {
            "fake"
        }
        fn worst_case_cost_micros(&self, _: &str, _: &str) -> u64 {
            1_000
        }
        fn actual_cost_micros(&self, _: &ProviderResponse) -> u64 {
            400
        }
        fn complete(&self, _: &str, user: &str) -> Result<ProviderResponse, String> {
            self.calls.set(self.calls.get() + 1);
            (self.answer)(user).map(|text| ProviderResponse {
                text,
                input_tokens: 10,
                output_tokens: 20,
            })
        }
    }

    const REPORT: &str = "## Sorun\nx\n## Kök neden\ny\n## Seçenekler\n1 / 2\n## Değişiklik\nz\n\
                          ## Doğrulama\nÇalıştırmadım: ağ yok.\n## Riskler ve açık kalanlar\nw\n";

    fn reviewer(verdict: &'static str) -> impl Fn(&str) -> Result<String, String> {
        move |prompt: &str| {
            let id = prompt
                .lines()
                .find_map(|l| l.split("Rapor kimliği: ").nth(1))
                .unwrap()
                .trim()
                .to_string();
            Ok(format!("KARAR: {verdict}\nİNCELENEN: {id}\n- bulgu yok"))
        }
    }

    fn open_policy(budget: u64) -> Policy {
        Policy {
            paid_dispatch_enabled: true,
            per_run_budget_micros: budget,
            ..Policy::default()
        }
    }

    #[test]
    fn two_acceptances_approve_and_costs_are_recorded() {
        let a = Fake::new(ProviderKind::OpenAi, |_| Ok(REPORT.into()));
        let b = Fake::new(ProviderKind::Anthropic, reviewer("KABUL"));
        let c = Fake::new(ProviderKind::Gemini, reviewer("KABUL"));
        let mut p = open_policy(10_000);
        let run = run_panel(
            "fren hattını modelle",
            ProviderKind::OpenAi,
            &[&a, &b, &c],
            &mut p,
        );
        assert_eq!(run.outcome, Outcome::Approved);
        assert_eq!(run.calls.len(), 3);
        assert_eq!(run.spent_micros, 1_200);
        assert!(render_markdown(&run).contains("# Panel run: APPROVED"));
    }

    #[test]
    fn kill_switch_blocks_before_any_call() {
        let a = Fake::new(ProviderKind::OpenAi, |_| Ok(REPORT.into()));
        let b = Fake::new(ProviderKind::Anthropic, reviewer("KABUL"));
        let c = Fake::new(ProviderKind::Gemini, reviewer("KABUL"));
        let mut p = Policy {
            per_run_budget_micros: 1_000_000,
            ..Policy::default()
        };
        let run = run_panel("t", ProviderKind::OpenAi, &[&a, &b, &c], &mut p);
        assert!(
            matches!(run.outcome, Outcome::Blocked(ref w) if w.contains("KARTAL_PAID_DISPATCH"))
        );
        assert_eq!(a.calls.get() + b.calls.get() + c.calls.get(), 0);
    }

    #[test]
    fn budget_stops_the_run_before_the_call_that_could_overrun() {
        let a = Fake::new(ProviderKind::OpenAi, |_| Ok(REPORT.into()));
        let b = Fake::new(ProviderKind::Anthropic, reviewer("KABUL"));
        let c = Fake::new(ProviderKind::Gemini, reviewer("KABUL"));
        // Author: worst case 1000 fits, costs 400. Reviewer 1: 400+1000 fits (1500), costs 400.
        // Reviewer 2: 800+1000 = 1800 > 1500 -> blocked without calling.
        let mut p = open_policy(1_500);
        let run = run_panel("t", ProviderKind::OpenAi, &[&a, &b, &c], &mut p);
        assert!(matches!(run.outcome, Outcome::Blocked(ref w) if w.contains("budget")));
        assert_eq!((b.calls.get(), c.calls.get()), (1, 0));
        assert_eq!(run.spent_micros, 800);
    }

    #[test]
    fn guard_rejects_a_bad_report_before_paying_for_reviews() {
        let a = Fake::new(ProviderKind::Gemini, |_| {
            Ok("Harika fikir! Tüm testler geçti.".into())
        });
        let b = Fake::new(ProviderKind::OpenAi, reviewer("KABUL"));
        let c = Fake::new(ProviderKind::Anthropic, reviewer("KABUL"));
        let mut p = open_policy(10_000);
        let run = run_panel("t", ProviderKind::Gemini, &[&a, &b, &c], &mut p);
        assert_eq!(run.outcome, Outcome::GuardRejected);
        assert_eq!(b.calls.get() + c.calls.get(), 0);
        assert_eq!(run.outcome.exit_code(), 2);
    }

    #[test]
    fn first_rejection_stops_and_split_goes_to_owner() {
        let a = Fake::new(ProviderKind::Anthropic, |_| Ok(REPORT.into()));
        let b = Fake::new(ProviderKind::OpenAi, reviewer("RET"));
        let c = Fake::new(ProviderKind::Gemini, reviewer("KABUL"));
        let mut p = open_policy(10_000);
        let run = run_panel("t", ProviderKind::Anthropic, &[&a, &b, &c], &mut p);
        assert!(matches!(
            run.outcome,
            Outcome::Panel(PanelDecision::Rejected { .. })
        ));
        assert_eq!(c.calls.get(), 0, "second review not paid for");

        // Reviewer order for Gemini as author is OpenAI, Anthropic.
        let a = Fake::new(ProviderKind::Gemini, |_| Ok(REPORT.into()));
        let b = Fake::new(ProviderKind::OpenAi, reviewer("KABUL"));
        let c = Fake::new(ProviderKind::Anthropic, reviewer("RET"));
        let run = run_panel(
            "t",
            ProviderKind::Gemini,
            &[&a, &b, &c],
            &mut open_policy(10_000),
        );
        assert!(matches!(
            run.outcome,
            Outcome::Panel(PanelDecision::Disputed { .. })
        ));
        assert_eq!(run.outcome.exit_code(), 1);
    }

    #[test]
    fn a_review_of_another_report_or_without_header_does_not_count() {
        let id = report_id(REPORT);
        assert!(
            parse_review(ProviderKind::OpenAi, "KARAR: KABUL\nİNCELENEN: r0", &id)
                .is_some_and(|r| !r.accepted || r.reviewed_commit != id)
        );
        assert_eq!(
            parse_review(ProviderKind::OpenAi, "Harika rapor, kabul!", &id),
            None
        );
        let ok = parse_review(
            ProviderKind::OpenAi,
            &format!("\nKARAR: KABUL\nİNCELENEN: {id}\n"),
            &id,
        )
        .unwrap();
        assert!(ok.accepted && ok.reviewed_commit == id);

        let a = Fake::new(ProviderKind::OpenAi, |_| Ok(REPORT.into()));
        let b = Fake::new(ProviderKind::Anthropic, |_| {
            Ok("Mükemmel, onaylıyorum.".into())
        });
        let c = Fake::new(ProviderKind::Gemini, reviewer("KABUL"));
        let run = run_panel(
            "t",
            ProviderKind::OpenAi,
            &[&a, &b, &c],
            &mut open_policy(10_000),
        );
        assert!(matches!(
            run.outcome,
            Outcome::Panel(PanelDecision::Pending { .. })
        ));
    }

    #[test]
    fn provider_errors_and_missing_partners_block() {
        let a = Fake::new(ProviderKind::OpenAi, |_| Err("HTTP 500".into()));
        let b = Fake::new(ProviderKind::Anthropic, reviewer("KABUL"));
        let c = Fake::new(ProviderKind::Gemini, reviewer("KABUL"));
        let run = run_panel(
            "t",
            ProviderKind::OpenAi,
            &[&a, &b, &c],
            &mut open_policy(10_000),
        );
        assert!(matches!(run.outcome, Outcome::Blocked(ref w) if w.contains("HTTP 500")));
        let run = run_panel(
            "t",
            ProviderKind::OpenAi,
            &[&a, &b],
            &mut open_policy(10_000),
        );
        assert!(matches!(run.outcome, Outcome::Blocked(ref w) if w.contains("gemini")));
    }

    #[test]
    fn policy_reads_kill_switch_and_budget() {
        let p = policy_from_lookup(|_| None).unwrap();
        assert!(!p.paid_dispatch_enabled && p.per_run_budget_micros == 0);
        let p = policy_from_lookup(|k| match k {
            "KARTAL_PAID_DISPATCH" => Some("on".into()),
            "KARTAL_RUN_BUDGET_MICROS" => Some("500000".into()),
            _ => None,
        })
        .unwrap();
        assert!(p.paid_dispatch_enabled && p.per_run_budget_micros == 500_000);
        assert!(
            policy_from_lookup(|k| (k == "KARTAL_RUN_BUDGET_MICROS").then(|| "5$".into())).is_err()
        );
        assert_eq!(usd(1_234_567), "$1.234567");
    }
}
