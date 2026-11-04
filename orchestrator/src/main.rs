use std::io::Read;

use kartal_agent_orchestrator::guard::{self, Finding, Verdict};
use kartal_agent_orchestrator::panel;
use kartal_agent_orchestrator::{
    engineer_prompt, MockProvider, Policy, Provider, ProviderKind, Task, ENGINEER_SYSTEM_PROMPT,
};

const USAGE: &str = "\
usage:
  kartal-orchestrator                       offline smoke run (mock provider)
  kartal-orchestrator check-response [FILE] model/chat answer: flattery, unproven success claims
  kartal-orchestrator check-diff [FILE]     unified diff: weakened checks, removed tests, owner switches
  kartal-orchestrator check-commits [FILE]  commit subjects, one per line: blind retries
  kartal-orchestrator check-report [FILE]   engineering report: sections, evidence, units
  kartal-orchestrator prompt [TASK...]      print the senior-engineer system prompt (+ task)
FILE defaults to stdin ('-').
exit codes: 0 ACCEPT, 1 NEEDS_OWNER, 2 REJECT, 64 usage error";

fn read_input(arg: Option<&str>) -> std::io::Result<String> {
    match arg {
        None | Some("-") => {
            let mut s = String::new();
            std::io::stdin().read_to_string(&mut s)?;
            Ok(s)
        }
        Some(path) => std::fs::read_to_string(path),
    }
}

fn report(findings: &[Finding]) -> Verdict {
    let gha = std::env::var_os("GITHUB_ACTIONS").is_some();
    for f in findings {
        println!(
            "finding severity={} rule={} file={} line={} detail={}",
            f.severity.as_str(),
            f.rule,
            if f.file.is_empty() { "-" } else { &f.file },
            f.line,
            f.detail
        );
        // Inline annotations on the PR when running in GitHub Actions.
        if gha && !f.file.is_empty() {
            let level = match f.severity {
                guard::Severity::Reject => "error",
                _ => "warning",
            };
            println!("::{level} title={}::{}", f.rule, f.detail);
        }
    }
    let v = guard::verdict(findings);
    println!("findings={}", findings.len());
    println!("verdict={}", v.as_str());
    v
}

fn smoke() -> i32 {
    let task = Task {
        id: "M0-SMOKE".to_string(),
        input_commit: "local-dry-run".to_string(),
        provider: ProviderKind::Mock,
        estimated_cost_micros: 0,
        instruction: "Validate the offline orchestrator skeleton".to_string(),
    };

    let policy = Policy::default();
    if let Err(reason) = policy.authorize(&task) {
        eprintln!("BLOCKED: {reason:?}");
        return 2;
    }

    let response = MockProvider
        .execute(&task.instruction)
        .expect("mock provider cannot fail");
    // Provider output is untrusted: it goes through the guard before anything else sees it.
    let v = guard::verdict(&guard::scan_response(&response.text));
    println!("mode=offline-mock");
    println!("task_id={}", task.id);
    println!("result={}", response.text);
    println!("guard={}", v.as_str());
    let author = panel::author_for(0);
    let reviewers: Vec<_> = panel::reviewers_for(author)
        .iter()
        .map(|p| p.name())
        .collect();
    println!(
        "panel author={} reviewers={}",
        author.name(),
        reviewers.join(",")
    );
    println!("paid_api_calls=0");
    v.exit_code()
}

fn main() {
    let args: Vec<String> = std::env::args().skip(1).collect();
    let cmd = args.first().map(String::as_str);
    let file = args.get(1).map(String::as_str);

    let scan: fn(&str) -> Vec<Finding> = match cmd {
        None => std::process::exit(smoke()),
        Some("check-response") => guard::scan_response,
        Some("check-diff") => guard::scan_diff,
        Some("check-commits") => guard::scan_commit_subjects,
        Some("check-report") => guard::scan_engineering_report,
        Some("prompt") => {
            let task = args[1..].join(" ");
            if task.trim().is_empty() {
                print!("{ENGINEER_SYSTEM_PROMPT}");
            } else {
                print!("{}", engineer_prompt(&task));
            }
            return;
        }
        Some("-h") | Some("--help") => {
            println!("{USAGE}");
            return;
        }
        Some(other) => {
            eprintln!("unknown command: {other}\n{USAGE}");
            std::process::exit(64);
        }
    };

    let input = match read_input(file) {
        Ok(s) => s,
        Err(e) => {
            eprintln!("cannot read input: {e}");
            std::process::exit(64);
        }
    };
    std::process::exit(report(&scan(&input)).exit_code());
}
