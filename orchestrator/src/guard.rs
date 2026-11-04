//! Output guard: model text and model diffs are untrusted.
//!
//! A model saying "done, all tests pass" is not evidence. This module turns the
//! repository's honesty rules into mechanical checks so that an agent cannot:
//!
//! * claim success without a CI run link or an exit-code record,
//! * pad answers with flattery instead of findings,
//! * make a red check green by weakening or deleting the check,
//! * flip owner-only switches (paid dispatch, VERIFIED status, force push).
//!
//! Everything here is pure string processing: no network, no git, no model calls.

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub enum Severity {
    /// Noise: reported, does not block.
    Warning,
    /// Allowed only with explicit owner approval.
    NeedsOwner,
    /// Never accepted automatically.
    Reject,
}

impl Severity {
    pub fn as_str(self) -> &'static str {
        match self {
            Severity::Warning => "warning",
            Severity::NeedsOwner => "needs-owner",
            Severity::Reject => "reject",
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Finding {
    pub severity: Severity,
    pub rule: &'static str,
    /// File path for diff findings; empty for free-text findings.
    pub file: String,
    /// 1-based line number in the scanned input.
    pub line: usize,
    pub detail: String,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Verdict {
    Accept,
    NeedsOwner,
    Reject,
}

impl Verdict {
    pub fn as_str(self) -> &'static str {
        match self {
            Verdict::Accept => "ACCEPT",
            Verdict::NeedsOwner => "NEEDS_OWNER",
            Verdict::Reject => "REJECT",
        }
    }

    /// Process exit code for the CLI: 0 accept, 1 owner approval required, 2 reject.
    pub fn exit_code(self) -> i32 {
        match self {
            Verdict::Accept => 0,
            Verdict::NeedsOwner => 1,
            Verdict::Reject => 2,
        }
    }
}

pub fn verdict(findings: &[Finding]) -> Verdict {
    match findings.iter().map(|f| f.severity).max() {
        Some(Severity::Reject) => Verdict::Reject,
        Some(Severity::NeedsOwner) => Verdict::NeedsOwner,
        _ => Verdict::Accept,
    }
}

/// Flattery and empty agreement. Matched case-insensitively.
const SYCOPHANCY: &[&str] = &[
    // English
    "great question",
    "excellent question",
    "you're absolutely right",
    "you are absolutely right",
    "you're completely right",
    "what a great idea",
    "brilliant idea",
    "excellent idea",
    "i'm thrilled",
    "happy to help!",
    "perfect! ",
    "amazing! ",
    // Turkish
    "harika bir soru",
    "çok güzel bir soru",
    "harika bir fikir",
    "mükemmel bir fikir",
    "kesinlikle haklısınız",
    "kesinlikle haklısın",
    "çok haklısınız",
    "çok haklısın",
    "harikasınız",
    "harikasın",
    "muhteşem bir",
    "mükemmel! ",
    "harika! ",
];

/// Claims that something was run, passed, pushed or is finished. Each one needs evidence.
const SUCCESS_CLAIMS: &[&str] = &[
    // English
    "all tests pass",
    "all tests passed",
    "tests are passing",
    "tests pass",
    "ci is green",
    "ci passed",
    "build passed",
    "build succeeded",
    "successfully pushed",
    "pushed to",
    "fully working",
    "fully tested",
    "production ready",
    "production-ready",
    "100% complete",
    "task complete",
    "everything works",
    // Turkish
    "tüm testler geçti",
    "bütün testler geçti",
    "testler geçti",
    "testler geçiyor",
    "ci yeşil",
    "derleme başarılı",
    "başarıyla push",
    "push edildi",
    "push ettim",
    "sorunsuz çalışıyor",
    "her şey çalışıyor",
    "tamamen çalışıyor",
    "eksiksiz tamamlandı",
    "başarıyla tamamlandı",
    "görev tamamlandı",
    "%100 tamamlandı",
];

/// Evidence that a check actually ran: a CI run link, or a recorded exit status.
fn has_run_evidence(lower: &str) -> bool {
    lower.contains("/actions/runs/")
        || lower.contains("exit code 0")
        || lower.contains("exit code: 0")
        || lower.contains("exit status 0")
        || lower.contains("exit=0")
}

/// A git object id (7..=40 hex chars, containing both a digit and a letter).
fn has_commit_sha(text: &str) -> bool {
    text.split(|c: char| !c.is_ascii_alphanumeric()).any(|tok| {
        (7..=40).contains(&tok.len())
            && tok.chars().all(|c| c.is_ascii_hexdigit())
            && tok.chars().any(|c| c.is_ascii_digit())
            && tok.chars().any(|c| c.is_ascii_alphabetic())
    })
}

/// Scan free text returned by a model (or pasted from a chat).
///
/// * flattery -> Warning (it is noise, and a sign the answer is tuned to please)
/// * a success claim without a CI link / exit status AND a commit SHA -> Reject
/// * flattery on a response with no findings and no evidence -> extra Warning
pub fn scan_response(text: &str) -> Vec<Finding> {
    let lower_all = text.to_lowercase();
    let evidence = has_run_evidence(&lower_all) && has_commit_sha(text);
    let mut out = Vec::new();

    for (idx, raw) in text.lines().enumerate() {
        let line = raw.to_lowercase();
        let n = idx + 1;
        // One flattery finding per line, even if several phrases overlap.
        if let Some(p) = SYCOPHANCY.iter().find(|p| line.contains(*p)) {
            out.push(Finding {
                severity: Severity::Warning,
                rule: "sycophancy",
                file: String::new(),
                line: n,
                detail: format!("flattery instead of content: \"{}\"", p.trim()),
            });
        }
        if !evidence {
            if let Some(p) = SUCCESS_CLAIMS.iter().find(|p| line.contains(*p)) {
                out.push(Finding {
                    severity: Severity::Reject,
                    rule: "unverified-claim",
                    file: String::new(),
                    line: n,
                    detail: format!(
                        "\"{p}\" claimed without a CI run link or exit status plus the commit SHA"
                    ),
                });
            }
        }
    }
    out
}

fn is_workflow(path: &str) -> bool {
    path.starts_with(".github/workflows/")
}

fn is_script_or_ci(path: &str) -> bool {
    is_workflow(path)
        || path.ends_with(".sh")
        || path.ends_with("Makefile")
        || path.ends_with(".yml")
        || path.ends_with(".yaml")
}

fn is_code(path: &str) -> bool {
    path.ends_with(".rs") || path.ends_with(".py")
}

fn is_test_marker(path: &str, trimmed: &str) -> bool {
    (path.ends_with(".rs") && trimmed == "#[test]")
        || (path.ends_with(".py")
            && (trimmed.starts_with("def test_") || trimmed.starts_with("async def test_")))
}

/// Scan a unified diff (`git diff base...head`) for changes that make checks weaker,
/// delete tests, or flip owner-only switches.
pub fn scan_diff(diff: &str) -> Vec<Finding> {
    let mut out = Vec::new();
    let mut file = String::new();
    let mut old_file = String::new();
    let mut tests_removed = 0usize;
    let mut tests_added = 0usize;
    let mut first_removed_test: Option<(String, usize)> = None;

    let push = |out: &mut Vec<Finding>, severity, rule, file: &str, line, detail: String| {
        out.push(Finding {
            severity,
            rule,
            file: file.to_string(),
            line,
            detail,
        })
    };

    for (idx, raw) in diff.lines().enumerate() {
        let n = idx + 1;
        if let Some(rest) = raw.strip_prefix("+++ ") {
            // A deleted file has `+++ /dev/null`; keep reporting it under its old name.
            file = match rest.strip_prefix("b/") {
                Some(p) => p.to_string(),
                None => old_file.clone(),
            };
            continue;
        }
        if let Some(rest) = raw.strip_prefix("--- ") {
            old_file = rest.strip_prefix("a/").unwrap_or(rest).to_string();
            continue;
        }
        if raw.starts_with("diff --git ") {
            continue;
        }

        if let Some(removed) = raw.strip_prefix('-') {
            let t = removed.trim();
            if is_test_marker(&file, t) {
                tests_removed += 1;
                first_removed_test.get_or_insert((file.clone(), n));
            }
            if is_workflow(&file) && t.contains("--check") && t.contains("cargo fmt") {
                push(
                    &mut out,
                    Severity::Reject,
                    "check-weakened",
                    &file,
                    n,
                    "format check removed from CI".to_string(),
                );
            }
            continue;
        }

        let Some(added) = raw.strip_prefix('+') else {
            continue;
        };
        let t = added.trim();
        if is_test_marker(&file, t) {
            tests_added += 1;
        }

        // Comments in YAML / shell / Makefiles do not execute.
        let script_comment = is_script_or_ci(&file) && t.starts_with('#');

        if is_workflow(&file) && !script_comment {
            if t.contains("cargo fmt") && !t.contains("--check") {
                push(
                    &mut out,
                    Severity::Reject,
                    "check-weakened",
                    &file,
                    n,
                    "CI rewrites formatting instead of checking it; use `cargo fmt --check`"
                        .to_string(),
                );
            }
            if t.starts_with("continue-on-error:") && t.contains("true") {
                push(
                    &mut out,
                    Severity::Reject,
                    "check-weakened",
                    &file,
                    n,
                    "CI step allowed to fail silently".to_string(),
                );
            }
            if t.contains("pull_request_target") {
                push(
                    &mut out,
                    Severity::Reject,
                    "secret-exposure",
                    &file,
                    n,
                    "pull_request_target runs untrusted code with repository secrets".to_string(),
                );
            }
        }

        if is_script_or_ci(&file) && !script_comment {
            if t.contains("|| true") || t.contains("|| :") {
                push(
                    &mut out,
                    Severity::Reject,
                    "check-weakened",
                    &file,
                    n,
                    "command failure swallowed with `|| true`".to_string(),
                );
            }
            if t.contains("--no-verify") {
                push(
                    &mut out,
                    Severity::Reject,
                    "check-weakened",
                    &file,
                    n,
                    "git hooks bypassed with --no-verify".to_string(),
                );
            }
            if t.contains("push --force") || t.contains("push -f ") || t.ends_with("push -f") {
                push(
                    &mut out,
                    Severity::NeedsOwner,
                    "history-rewrite",
                    &file,
                    n,
                    "force push rewrites published history".to_string(),
                );
            }
        }

        if is_code(&file) {
            if t.starts_with("#[ignore") {
                push(
                    &mut out,
                    Severity::Reject,
                    "test-disabled",
                    &file,
                    n,
                    "Rust test disabled with #[ignore]".to_string(),
                );
            }
            if t.starts_with("@pytest.mark.skip")
                || t.starts_with("@pytest.mark.xfail")
                || t.starts_with("@unittest.skip")
            {
                push(
                    &mut out,
                    Severity::Reject,
                    "test-disabled",
                    &file,
                    n,
                    "Python test skipped".to_string(),
                );
            }
            let compact: String = t.chars().filter(|c| !c.is_whitespace()).collect();
            if compact.starts_with("paid_dispatch_enabled:true")
                || compact.starts_with("paid_dispatch_enabled=true")
            {
                push(
                    &mut out,
                    Severity::NeedsOwner,
                    "paid-dispatch",
                    &file,
                    n,
                    "paid API dispatch switched on".to_string(),
                );
            }
        }

        if file.contains("specs/") && (file.ends_with(".yaml") || file.ends_with(".yml")) {
            let compact: String = t.chars().filter(|c| !c.is_whitespace()).collect();
            if compact.contains("status:VERIFIED") || compact.contains("status:VALIDATED") {
                push(
                    &mut out,
                    Severity::NeedsOwner,
                    "evidence-promotion",
                    &file,
                    n,
                    "value promoted to VERIFIED/VALIDATED; requires owner-held evidence"
                        .to_string(),
                );
            }
        }
    }

    if tests_removed > tests_added {
        let (f, n) = first_removed_test.unwrap_or_default();
        out.push(Finding {
            severity: Severity::Reject,
            rule: "test-removed",
            file: f,
            line: n,
            detail: format!(
                "{} test(s) removed, {} added: net loss of {}",
                tests_removed,
                tests_added,
                tests_removed - tests_added
            ),
        });
    }
    out
}

/// Scan commit subjects (one per line, e.g. `git log --format=%s base..head`).
/// Repeated identical subjects mean an agent retried blindly instead of fixing once.
pub fn scan_commit_subjects(log: &str) -> Vec<Finding> {
    let mut out = Vec::new();
    let mut seen: Vec<&str> = Vec::new();
    for (idx, raw) in log.lines().enumerate() {
        let s = raw.trim();
        if s.is_empty() {
            continue;
        }
        if seen.contains(&s) {
            out.push(Finding {
                severity: Severity::Warning,
                rule: "duplicate-commit",
                file: String::new(),
                line: idx + 1,
                detail: format!("commit subject repeated: \"{s}\""),
            });
        } else {
            seen.push(s);
        }
    }
    out
}

#[cfg(test)]
mod tests {
    use super::*;

    fn rules(f: &[Finding]) -> Vec<&'static str> {
        f.iter().map(|x| x.rule).collect()
    }

    #[test]
    fn flattery_is_flagged_but_does_not_block() {
        let f = scan_response("Harika bir soru!\nKesinlikle haklısınız.\nDosya 3 satır.");
        assert_eq!(rules(&f), vec!["sycophancy", "sycophancy"]);
        assert_eq!(verdict(&f), Verdict::Accept);
    }

    #[test]
    fn success_claim_without_evidence_is_rejected() {
        for text in [
            "Tüm testler geçti, push ettim.",
            "Done! All tests pass and CI is green.",
            "Görev tamamlandı.",
        ] {
            let f = scan_response(text);
            assert_eq!(verdict(&f), Verdict::Reject, "{text}");
            assert!(rules(&f).contains(&"unverified-claim"));
        }
    }

    #[test]
    fn success_claim_with_run_link_and_sha_is_accepted() {
        let text = "Testler geçti: commit 14e0e9f, \
                    https://github.com/o/r/actions/runs/123456";
        assert_eq!(verdict(&scan_response(text)), Verdict::Accept);
    }

    #[test]
    fn run_link_without_sha_is_not_enough() {
        let text = "CI is green: https://github.com/o/r/actions/runs/123456";
        assert_eq!(verdict(&scan_response(text)), Verdict::Reject);
    }

    #[test]
    fn plain_findings_are_accepted() {
        let text = "3 hata buldum. lib.rs:42 bütçe taşması kontrol edilmiyor.";
        assert!(scan_response(text).is_empty());
    }

    /// Regression: commit 14e0e9f replaced `cargo fmt --check` with `cargo fmt` in CI.
    #[test]
    fn replacing_fmt_check_with_fmt_is_rejected() {
        let diff = "\
diff --git a/.github/workflows/rust-orchestrator.yml b/.github/workflows/rust-orchestrator.yml
--- a/.github/workflows/rust-orchestrator.yml
+++ b/.github/workflows/rust-orchestrator.yml
@@ -27,2 +27,2 @@
-      - name: Format check
-        run: cargo fmt --manifest-path orchestrator/Cargo.toml --check
+      - name: Format Rust sources
+        run: cargo fmt --manifest-path orchestrator/Cargo.toml
";
        let f = scan_diff(diff);
        assert_eq!(verdict(&f), Verdict::Reject);
        assert_eq!(rules(&f), vec!["check-weakened", "check-weakened"]);
        assert!(f
            .iter()
            .all(|x| x.file == ".github/workflows/rust-orchestrator.yml"));
    }

    #[test]
    fn swallowed_failures_and_skipped_tests_are_rejected() {
        let diff = "\
+++ b/scripts/run_tests.sh
+pytest -q || true
+++ b/.github/workflows/ci.yml
+        continue-on-error: true
+++ b/orchestrator/src/lib.rs
+    #[ignore]
+++ b/kartal-s-twin/tests/test_spec.py
+@pytest.mark.skip(reason=\"flaky\")
";
        let f = scan_diff(diff);
        assert_eq!(
            rules(&f),
            vec![
                "check-weakened",
                "check-weakened",
                "test-disabled",
                "test-disabled"
            ]
        );
        assert_eq!(verdict(&f), Verdict::Reject);
    }

    #[test]
    fn net_test_deletion_is_rejected_but_moving_a_test_is_not() {
        let deleted = "+++ b/orchestrator/src/lib.rs\n-    #[test]\n-    fn budget() {}\n";
        assert_eq!(rules(&scan_diff(deleted)), vec!["test-removed"]);

        let moved = "+++ b/orchestrator/src/lib.rs\n-    #[test]\n+++ b/orchestrator/src/guard.rs\n+    #[test]\n";
        assert!(scan_diff(moved).is_empty());
    }

    #[test]
    fn owner_switches_need_owner() {
        let diff = "\
+++ b/orchestrator/src/main.rs
+        paid_dispatch_enabled: true,
+++ b/kartal-s-twin/specs/kartal_s_1997.yaml
+    status: VERIFIED
";
        let f = scan_diff(diff);
        assert_eq!(rules(&f), vec!["paid-dispatch", "evidence-promotion"]);
        assert_eq!(verdict(&f), Verdict::NeedsOwner);
    }

    #[test]
    fn pull_request_target_is_rejected() {
        let diff = "+++ b/.github/workflows/x.yml\n+on: pull_request_target\n";
        assert_eq!(verdict(&scan_diff(diff)), Verdict::Reject);
    }

    #[test]
    fn patterns_inside_docs_and_string_literals_are_ignored() {
        let diff = "\
+++ b/kartal-s-twin/agents/GPT_DAVRANIS_KURALLARI.md
+Never write `|| true`, `#[ignore]` or `cargo fmt` without --check.
+++ b/orchestrator/src/guard.rs
+            if t.starts_with(\"#[ignore\") {
";
        assert!(scan_diff(diff).is_empty());
    }

    #[test]
    fn deleting_a_whole_test_file_is_rejected() {
        let diff = "--- a/kartal-s-twin/tests/test_spec.py\n+++ /dev/null\n-def test_spec():\n";
        let f = scan_diff(diff);
        assert_eq!(rules(&f), vec!["test-removed"]);
        assert_eq!(f[0].file, "kartal-s-twin/tests/test_spec.py");
    }

    #[test]
    fn comments_in_workflows_and_scripts_are_ignored() {
        let diff = "\
+++ b/.github/workflows/x.yml
+  # pull_request_target and `|| true` are forbidden here
+++ b/scripts/run_tests.sh
+# never add || true
";
        assert!(scan_diff(diff).is_empty());
    }

    /// Regression: four identical commits on feat/rust-agent-orchestrator-plan.
    #[test]
    fn repeated_commit_subjects_are_flagged() {
        let log = "ci: format\nfeat(orchestrator): add offline Rust M0 core\n\
                   feat(orchestrator): add offline Rust M0 core\n\
                   feat(orchestrator): add offline Rust M0 core\n";
        let f = scan_commit_subjects(log);
        assert_eq!(f.len(), 2);
        assert_eq!(verdict(&f), Verdict::Accept);
    }

    #[test]
    fn sha_detection() {
        assert!(has_commit_sha("at 14e0e9f."));
        assert!(!has_commit_sha("deadbeef")); // no digit
        assert!(!has_commit_sha("1234567")); // no letter
        assert!(!has_commit_sha("abc12")); // too short
    }
}
