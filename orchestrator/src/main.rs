use std::io::Read;

use kartal_agent_orchestrator::guard::{self, Finding, Verdict};
use kartal_agent_orchestrator::{
    engineer_prompt, team_leader_prompt, MockProvider, Policy, Provider, ProviderKind, Task,
    ENGINEER_SYSTEM_PROMPT, TEAM_LEADER_SYSTEM_PROMPT,
};
use kartal_agent_orchestrator::{panel, providers, run};

const USAGE: &str = "\
usage:
  kartal-orchestrator                       offline smoke run (mock provider)
  kartal-orchestrator check-response [FILE] model/chat answer: flattery, unproven success claims
  kartal-orchestrator check-diff [FILE]     unified diff: weakened checks, removed tests, owner switches
  kartal-orchestrator check-commits [FILE]  commit subjects, one per line: blind retries
  kartal-orchestrator check-report [FILE]   engineering report: sections, evidence, units
  kartal-orchestrator prompt [TASK...]      print the senior-engineer system prompt (+ task)
  kartal-orchestrator leader-prompt [TASK...] print the Level-6 coordinator prompt (+ task)
  kartal-orchestrator panel-key --author openai|anthropic|gemini
                                            print the dispatch key for KARTAL_TASK at GITHUB_SHA
  kartal-orchestrator panel-run --author openai|anthropic|gemini [--mock]
                                            author writes, guard checks, other two review.
                                            Task text from KARTAL_TASK or stdin. Paid calls need
                                            KARTAL_PAID_DISPATCH=on and KARTAL_RUN_BUDGET_MICROS.
                                            Exit: 0 approved, 1 owner decides, 2 rejected, 3 blocked
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

fn env(name: &str) -> Option<String> {
    std::env::var(name).ok()
}

/// Offline stand-in for `--mock`: writes a well-formed report and accepts it.
struct MockPartner(ProviderKind);
impl run::Partner for MockPartner {
    fn kind(&self) -> ProviderKind {
        self.0
    }
    fn model(&self) -> &str {
        "mock"
    }
    fn worst_case_cost_micros(&self, _: &str, _: &str) -> u64 {
        0
    }
    fn actual_cost_micros(&self, _: &kartal_agent_orchestrator::ProviderResponse) -> u64 {
        0
    }
    fn complete(
        &self,
        _: &str,
        user: &str,
    ) -> Result<kartal_agent_orchestrator::ProviderResponse, String> {
        let text = match user.lines().find_map(|l| l.split("Rapor kimliği: ").nth(1)) {
            Some(id) => format!("KARAR: KABUL\nİNCELENEN: {}\n- mock inceleme", id.trim()),
            None => "## Sorun\nmock\n## Kök neden\nmock\n## Seçenekler\nmock\n## Değişiklik\nmock\n\
                     ## Doğrulama\nÇalıştırmadım: mock çalıştırma.\n## Riskler ve açık kalanlar\nmock\n"
                .to_string(),
        };
        Ok(kartal_agent_orchestrator::ProviderResponse {
            text,
            input_tokens: 0,
            output_tokens: 0,
        })
    }
}

fn parse_author(args: &[String]) -> Option<ProviderKind> {
    match args {
        [flag, name] if flag == "--author" => match name.as_str() {
            "openai" => Some(ProviderKind::OpenAi),
            "anthropic" => Some(ProviderKind::Anthropic),
            "gemini" => Some(ProviderKind::Gemini),
            _ => None,
        },
        _ => None,
    }
}

fn panel_key(args: &[String]) -> i32 {
    let Some(author) = parse_author(args) else {
        eprintln!("panel-key needs --author openai|anthropic|gemini");
        return 64;
    };
    let (Some(task), Some(sha)) = (
        env("KARTAL_TASK").filter(|t| !t.trim().is_empty()),
        env("GITHUB_SHA").filter(|s| !s.trim().is_empty()),
    ) else {
        eprintln!("panel-key needs KARTAL_TASK and GITHUB_SHA");
        return 64;
    };
    println!("{}", run::dispatch_key(author, &sha, &task));
    0
}

fn panel_run(args: &[String]) -> i32 {
    let mut author = None;
    let mut mock = false;
    let mut it = args.iter();
    while let Some(a) = it.next() {
        match a.as_str() {
            "--author" => author = it.next().cloned(),
            "--mock" => mock = true,
            other => {
                eprintln!("unknown panel-run argument: {other}\n{USAGE}");
                return 64;
            }
        }
    }
    let author = match author.as_deref() {
        Some("openai") => ProviderKind::OpenAi,
        Some("anthropic") => ProviderKind::Anthropic,
        Some("gemini") => ProviderKind::Gemini,
        _ => {
            eprintln!("--author must be openai, anthropic or gemini");
            return 64;
        }
    };
    let task = match env("KARTAL_TASK").filter(|t| !t.trim().is_empty()) {
        Some(t) => t,
        None => match read_input(None) {
            Ok(t) => t,
            Err(e) => {
                eprintln!("cannot read task: {e}");
                return 64;
            }
        },
    };

    let (run, summary) = if mock {
        let partners: Vec<MockPartner> = panel::PARTNERS.iter().map(|k| MockPartner(*k)).collect();
        let refs: Vec<&dyn run::Partner> =
            partners.iter().map(|p| p as &dyn run::Partner).collect();
        // Mock partners cost nothing; a zero budget still refuses any call that could.
        let mut policy = Policy {
            paid_dispatch_enabled: true,
            per_run_budget_micros: 0,
            ..Policy::default()
        };
        let r = run::run_panel(&task, author, &refs, &mut policy);
        let s = run::render_markdown(&r);
        (r, s)
    } else {
        let mut policy = match run::policy_from_lookup(env) {
            Ok(p) => p,
            Err(e) => {
                eprintln!("{e}");
                // Nothing was called: the workflow must not record this as a paid dispatch.
                println!("verdict=BLOCKED");
                println!("spent_micros=0");
                return 3;
            }
        };
        let mut partners = Vec::new();
        let mut problems = Vec::new();
        for kind in panel::PARTNERS {
            let key_var = kind.api_key_env().expect("partners have keys");
            let built = providers::ProviderConfig::from_lookup(kind, env).and_then(|cfg| {
                let key = env(key_var).ok_or(format!("{key_var} is not set"))?;
                providers::HttpProvider::new(cfg, key, providers::CurlTransport)
            });
            match built {
                Ok(p) => partners.push(p),
                Err(e) => problems.push(e),
            }
        }
        if !problems.is_empty() {
            for p in &problems {
                eprintln!("config: {p}");
            }
            println!("verdict=BLOCKED");
            println!("spent_micros=0");
            return 3;
        }
        let refs: Vec<&dyn run::Partner> =
            partners.iter().map(|p| p as &dyn run::Partner).collect();
        let r = run::run_panel(&task, author, &refs, &mut policy);
        let s = run::render_markdown(&r);
        (r, s)
    };

    println!("{summary}");
    if let Some(path) = env("GITHUB_STEP_SUMMARY") {
        if let Err(e) = std::fs::OpenOptions::new()
            .create(true)
            .append(true)
            .open(path)
            .and_then(|mut f| std::io::Write::write_all(&mut f, summary.as_bytes()))
        {
            eprintln!("cannot write job summary: {e}");
        }
    }
    println!("verdict={}", run.outcome.label());
    println!("spent_micros={}", run.spent_micros);
    run.outcome.exit_code()
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
        Some("panel-run") => std::process::exit(panel_run(&args[1..])),
        Some("panel-key") => std::process::exit(panel_key(&args[1..])),
        Some("leader-prompt") => {
            let task = args[1..].join(" ");
            if task.trim().is_empty() {
                print!("{TEAM_LEADER_SYSTEM_PROMPT}");
            } else {
                print!("{}", team_leader_prompt(&task));
            }
            return;
        }
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
