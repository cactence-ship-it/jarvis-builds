use kartal_agent_orchestrator::{MockProvider, Policy, Provider, ProviderKind, Task};

fn main() {
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
        std::process::exit(2);
    }

    let response = MockProvider.execute(&task.instruction).expect("mock provider cannot fail");
    println!("mode=offline-mock");
    println!("task_id={}", task.id);
    println!("result={}", response.text);
    println!("paid_api_calls=0");
}
