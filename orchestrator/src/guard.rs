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

/// `|| true` is legitimate where failure is expected and harmless: cleanup in a trap,
/// killing a process that may already be gone, removing a file that may not exist, or
/// reading an optional stamp file. It is never legitimate on a build or test command.
fn is_cleanup_or_probe(line: &str) -> bool {
    line.starts_with("trap ")
        || line.contains("kill ")
        || line.contains("rm -f ")
        || line.contains("$(cat ")
}

/// D-029: new code is Rust. A new Python file is allowed only for Blender (its API is
/// Python only) and as a test of the existing Python modules.
fn is_disallowed_new_python(path: &str) -> bool {
    path.ends_with(".py")
        && !path.starts_with("kartal-s-twin/tools/blender/")
        && !path.starts_with("kartal-s-twin/tests/")
}

/// Scan a unified diff (`git diff base...head`) for changes that make checks weaker,
/// delete tests, or flip owner-only switches.
pub fn scan_diff(diff: &str) -> Vec<Finding> {
    let mut out = Vec::new();
    let mut file = String::new();
    let mut old_file = String::new();
    let mut new_file = false;
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
            if new_file && is_disallowed_new_python(&file) {
                push(
                    &mut out,
                    Severity::Reject,
                    "new-python-file",
                    &file,
                    n,
                    "new code must be Rust (D-029); new .py only under tools/blender/ or tests/"
                        .to_string(),
                );
            }
            new_file = false;
            continue;
        }
        if let Some(rest) = raw.strip_prefix("--- ") {
            new_file = rest == "/dev/null";
            old_file = rest.strip_prefix("a/").unwrap_or(rest).to_string();
            continue;
        }
        if raw.starts_with("diff --git ") {
            new_file = false;
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
            if (t.contains("|| true") || t.contains("|| :")) && !is_cleanup_or_probe(t) {
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

/// Sections every engineering report must have: (rule label, accepted heading keywords).
const REPORT_SECTIONS: &[(&str, &[&str])] = &[
    ("problem", &["sorun", "problem"]),
    ("root-cause", &["kök neden", "root cause"]),
    (
        "options",
        &["seçenek", "alternatif", "options", "alternatives"],
    ),
    ("change", &["değişiklik", "change"]),
    ("verification", &["doğrulama", "verification"]),
    ("risks", &["risk"]),
];

/// Honest "I did not verify" statements; acceptable instead of evidence.
const NOT_VERIFIED: &[&str] = &[
    "çalıştırmadım",
    "çalıştırılmadı",
    "doğrulanmadı",
    "doğrulayamadım",
    "doğrulanamadı",
    "not run",
    "not verified",
    "could not verify",
];

/// Physical quantities that must carry a unit when a number is given.
const QUANTITIES: &[&str] = &[
    "uzunluk",
    "genişlik",
    "yükseklik",
    "çap",
    "mesafe",
    "boşluk",
    "kalınlık",
    "ağırlık",
    "kütle",
    "basınç",
    "tork",
    "voltaj",
    "gerilim",
    "akım",
    "sıcaklık",
    "hacim",
    "dingil",
    "length",
    "width",
    "height",
    "diameter",
    "distance",
    "clearance",
    "thickness",
    "weight",
    "mass",
    "pressure",
    "torque",
    "voltage",
    "current",
    "temperature",
    "volume",
    "wheelbase",
];

const UNITS: &[&str] = &[
    "mm", "cm", "m", "km", "µm", "um", "kg", "g", "t", "n", "kn", "n·m", "nm", "n.m", "bar", "kpa",
    "mpa", "pa", "psi", "°", "°c", "°f", "c", "k", "v", "mv", "kv", "a", "ma", "w", "kw", "hp",
    "bg", "ps", "l", "ml", "cc", "cm³", "m³", "rpm", "d/d", "dev/dak", "%", "s", "ms", "h", "hz",
    "khz", "inç", "inch", "in", "\"", "ah", "wh", "kwh",
];

fn heading_text(line: &str) -> Option<String> {
    let t = line.trim();
    if t.starts_with('#') || t.starts_with("**") {
        Some(
            t.trim_matches(|c| c == '#' || c == '*' || c == ' ')
                .to_lowercase(),
        )
    } else {
        None
    }
}

fn has_unit(line: &str) -> bool {
    line.split_whitespace().any(|tok| {
        let tok = tok.trim_matches(|c: char| ",;:()[]".contains(c));
        let rest = tok.trim_start_matches(|c: char| c.is_ascii_digit() || ".,±+-~".contains(c));
        let rest = rest.trim_end_matches('.').to_lowercase();
        !rest.is_empty() && UNITS.contains(&rest.as_str())
    })
}

fn has_number(line: &str) -> bool {
    line.split_whitespace().any(|tok| {
        let tok = tok.trim_matches(|c: char| ",;:()[]".contains(c));
        tok.chars().next().is_some_and(|c| c.is_ascii_digit())
    })
}

/// Scan an engineering report: everything `scan_response` checks, plus
/// * every section of the report format is present (missing -> Reject),
/// * the verification section carries evidence or says plainly that nothing was run,
/// * a physical quantity given as a number carries a unit (missing -> Warning).
pub fn scan_engineering_report(text: &str) -> Vec<Finding> {
    let mut out = scan_response(text);
    let lines: Vec<&str> = text.lines().collect();
    let headings: Vec<(usize, String)> = lines
        .iter()
        .enumerate()
        .filter_map(|(i, l)| heading_text(l).map(|h| (i, h)))
        .collect();

    for (rule, keys) in REPORT_SECTIONS {
        if !headings
            .iter()
            .any(|(_, h)| keys.iter().any(|k| h.contains(k)))
        {
            out.push(Finding {
                severity: Severity::Reject,
                rule: "missing-section",
                file: String::new(),
                line: 0,
                detail: format!(
                    "engineering report has no `{rule}` section ({})",
                    keys.join(" / ")
                ),
            });
        }
    }

    // Body of the verification section: from its heading to the next heading.
    let verification = headings
        .iter()
        .position(|(_, h)| REPORT_SECTIONS[4].1.iter().any(|k| h.contains(k)));
    if let Some(pos) = verification {
        let start = headings[pos].0 + 1;
        let end = headings.get(pos + 1).map_or(lines.len(), |(i, _)| *i);
        let body = lines[start..end].join("\n");
        let lower = body.to_lowercase();
        let honest = NOT_VERIFIED.iter().any(|p| lower.contains(p));
        let proven = has_run_evidence(&lower) && has_commit_sha(&body);
        if !honest && !proven {
            out.push(Finding {
                severity: Severity::Reject,
                rule: "verification-without-evidence",
                file: String::new(),
                line: headings[pos].0 + 1,
                detail: "verification needs a command exit status or CI run link plus the \
                         commit SHA, or an explicit statement that it was not run"
                    .to_string(),
            });
        }
    }

    for (idx, raw) in lines.iter().enumerate() {
        if heading_text(raw).is_some() {
            continue;
        }
        let lower = raw.to_lowercase();
        if QUANTITIES.iter().any(|q| lower.contains(q)) && has_number(raw) && !has_unit(raw) {
            out.push(Finding {
                severity: Severity::Warning,
                rule: "unitless-value",
                file: String::new(),
                line: idx + 1,
                detail: "physical quantity given without a unit".to_string(),
            });
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

    #[test]
    fn cleanup_and_probe_true_is_allowed_but_not_on_checks() {
        let diff = "\
+++ b/kartal-s-twin/tools/viewer_smoke/run.sh
+trap 'kill $srv 2>/dev/null || true' EXIT
+have=\"$(cat \"$STAMP\" 2>/dev/null || true)\"
+rm -f build/tmp.json || true
";
        assert!(scan_diff(diff).is_empty());
        let bad = "+++ b/kartal-s-twin/scripts/run_tests.sh\n+cargo test 2>/dev/null || true\n";
        assert_eq!(rules(&scan_diff(bad)), vec!["check-weakened"]);
    }

    #[test]
    fn new_python_files_are_rejected_outside_blender_and_tests() {
        let new = |path: &str| {
            format!("diff --git a/{path} b/{path}\nnew file mode 100644\n--- /dev/null\n+++ b/{path}\n+import os\n")
        };
        assert_eq!(
            rules(&scan_diff(&new("kartal-s-twin/tools/new_tool.py"))),
            vec!["new-python-file"]
        );
        assert!(scan_diff(&new("kartal-s-twin/tools/blender/lamps.py")).is_empty());
        assert!(scan_diff(&new("kartal-s-twin/tests/test_new.py")).is_empty());
        assert!(scan_diff(&new("orchestrator/src/new.rs")).is_empty());

        // Editing existing Python is allowed.
        let edit = "--- a/kartal-s-twin/tools/twin.py\n+++ b/kartal-s-twin/tools/twin.py\n+x = 1\n";
        assert!(scan_diff(edit).is_empty());
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

    const GOOD_REPORT: &str = "\
## Sorun
Lastik zarfı çapı yanlış.
## Kök neden
Spec 175/70 R14 kullanıyor, sahip 185/70 R14 bildirdi.
## Seçenekler
1. Spec'i değiştir. 2. İki konfigürasyon tut. İkincisi seçildi: geri alınabilir.
## Değişiklik
Dış çap 614.6 mm (ESTIMATED, ± 3 mm).
## Doğrulama
`pytest -q` exit code 0 at 8d9f16f, https://github.com/o/r/actions/runs/42
## Riskler ve açık kalanlar
Jant ölçüsü şerit metreyle ölçülmedi.
";

    #[test]
    fn complete_engineering_report_is_accepted() {
        let f = scan_engineering_report(GOOD_REPORT);
        assert!(f.is_empty(), "{f:?}");
    }

    #[test]
    fn report_without_root_cause_and_options_is_rejected() {
        let text = "## Sorun\nx\n## Değişiklik\ny\n## Doğrulama\nÇalıştırmadım.\n## Riskler\nz\n";
        let f = scan_engineering_report(text);
        assert_eq!(rules(&f), vec!["missing-section", "missing-section"]);
        assert_eq!(verdict(&f), Verdict::Reject);
    }

    #[test]
    fn verification_without_evidence_is_rejected_but_honesty_is_accepted() {
        let vague = GOOD_REPORT.replace(
            "`pytest -q` exit code 0 at 8d9f16f, https://github.com/o/r/actions/runs/42",
            "Kontrol ettim, sorun yok.",
        );
        assert_eq!(
            rules(&scan_engineering_report(&vague)),
            vec!["verification-without-evidence"]
        );

        let honest = GOOD_REPORT.replace(
            "`pytest -q` exit code 0 at 8d9f16f, https://github.com/o/r/actions/runs/42",
            "Testleri çalıştırmadım: ortamda build123d yok.",
        );
        assert!(scan_engineering_report(&honest).is_empty());
    }

    #[test]
    fn quantities_need_units() {
        assert!(has_unit("dingil mesafesi 2440 mm"));
        assert!(has_unit("basınç 2.2bar"));
        assert!(has_unit("tork 105 N·m"));
        assert!(!has_unit("dingil mesafesi 2440"));
        let text = GOOD_REPORT.replace("Dış çap 614.6 mm", "Dış çap 614.6");
        assert_eq!(
            rules(&scan_engineering_report(&text)),
            vec!["unitless-value"]
        );
    }

    #[test]
    fn engineer_prompt_requires_the_checked_report_format() {
        let prompt = crate::ENGINEER_SYSTEM_PROMPT;
        let headings: Vec<String> = prompt.lines().filter_map(heading_text).collect();
        for (rule, keys) in REPORT_SECTIONS {
            assert!(
                headings.iter().any(|h| keys.iter().any(|k| h.contains(k))),
                "prompt report format lacks `{rule}`"
            );
        }
    }

    #[test]
    fn sha_detection() {
        assert!(has_commit_sha("at 14e0e9f."));
        assert!(!has_commit_sha("deadbeef")); // no digit
        assert!(!has_commit_sha("1234567")); // no letter
        assert!(!has_commit_sha("abc12")); // too short
    }
}
