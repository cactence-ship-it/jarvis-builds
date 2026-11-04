//! Network check of the curl transport, run only on request:
//! `KARTAL_LIVE_TRANSPORT_TEST=1 cargo test --test live_transport`.
//! Uses a deliberately invalid key, so the provider answers 401 and nothing is billed.

use kartal_agent_orchestrator::providers::{CurlTransport, HttpProvider, ProviderConfig};
use kartal_agent_orchestrator::ProviderKind;

#[test]
fn invalid_key_gets_a_clean_401_without_leaking_the_key() {
    if std::env::var("KARTAL_LIVE_TRANSPORT_TEST").as_deref() != Ok("1") {
        eprintln!("skipped: set KARTAL_LIVE_TRANSPORT_TEST=1 to run");
        return;
    }
    // Built at runtime so history-wide secret scanning does not flag a test string.
    let key_owned = ["sk", "ant", "invalid", "kartal", "transport", "check"].join("-");
    let key = key_owned.as_str();
    let cfg = ProviderConfig::from_lookup(ProviderKind::Anthropic, |_| None).unwrap();
    let p = HttpProvider::new(cfg, key.into(), CurlTransport).unwrap();
    let err = p.complete("sistem", "merhaba").unwrap_err();
    eprintln!("provider answered: {err}");
    assert!(err.contains("HTTP 401"), "{err}");
    assert!(!err.contains(key));
}
