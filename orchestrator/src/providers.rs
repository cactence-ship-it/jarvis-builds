//! HTTP adapters for the three partners: OpenAI (GPT), Anthropic (Claude), Google (Gemini).
//!
//! Design limits:
//! * No HTTP crate: requests go through the system `curl`, configured on **stdin**, so the
//!   API key never appears on a command line, in the process list or in logs.
//! * Each provider's model and per-token price come from the runner environment. A
//!   provider without a configured price is refused: if cost cannot be computed, no call.
//! * Before every call the worst-case cost is charged against the budget; after the call
//!   the real usage is recorded.
//! * Response text is untrusted: the panel runs it through the guard.

use std::io::Write;
use std::process::{Command, Stdio};
use std::time::Duration;

use crate::json::{self, Value};
use crate::{ProviderKind, ProviderResponse};

/// Anthropic API version header (Messages API).
const ANTHROPIC_VERSION: &str = "2026-10-21";
/// Refusal fallback beta: on a safety refusal the server retries on a suitable model.
const ANTHROPIC_FALLBACK_BETA: &str = "server-side-fallback-2026-07-01";
/// Fallback models may cost more per token than the configured model; budget for it.
const ANTHROPIC_FALLBACK_MARGIN_PERCENT: u64 = 25;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ProviderConfig {
    pub kind: ProviderKind,
    pub model: String,
    pub max_output_tokens: u64,
    /// USD micro-dollars per 1,000,000 input tokens.
    pub price_in_micros_per_mtok: u64,
    /// USD micro-dollars per 1,000,000 output tokens (thinking tokens bill as output).
    pub price_out_micros_per_mtok: u64,
    pub timeout: Duration,
}

impl ProviderConfig {
    fn env_prefix(kind: ProviderKind) -> &'static str {
        match kind {
            ProviderKind::OpenAi => "KARTAL_OPENAI",
            ProviderKind::Anthropic => "KARTAL_ANTHROPIC",
            ProviderKind::Gemini => "KARTAL_GEMINI",
            ProviderKind::Mock => "KARTAL_MOCK",
        }
    }

    /// Read `KARTAL_<P>_MODEL`, `_PRICE_IN`, `_PRICE_OUT` (USD micros per 1M tokens) and
    /// optional `_MAX_OUTPUT` / `_TIMEOUT_SECS` through `get`.
    ///
    /// Anthropic has documented defaults (claude-opus-5-5 at $4 / $20 per 1M tokens).
    /// OpenAI and Gemini have none here: the owner sets their model and current price.
    pub fn from_lookup(
        kind: ProviderKind,
        get: impl Fn(&str) -> Option<String>,
    ) -> Result<Self, String> {
        let p = Self::env_prefix(kind);
        let var = |name: &str| get(&format!("{p}_{name}")).filter(|v| !v.trim().is_empty());
        let num = |name: &str| -> Result<Option<u64>, String> {
            var(name)
                .map(|v| {
                    v.trim()
                        .parse::<u64>()
                        .map_err(|_| format!("{p}_{name} is not a whole number"))
                })
                .transpose()
        };
        let (dm, din, dout) = match kind {
            ProviderKind::Anthropic => (Some("claude-opus-5-5"), Some(4_000_000), Some(20_000_000)),
            _ => (None, None, None),
        };
        let model = var("MODEL")
            .or(dm.map(String::from))
            .ok_or(format!("{p}_MODEL is not set"))?;
        let price_in = num("PRICE_IN")?
            .or(din)
            .ok_or(format!("{p}_PRICE_IN is not set"))?;
        let price_out = num("PRICE_OUT")?
            .or(dout)
            .ok_or(format!("{p}_PRICE_OUT is not set"))?;
        if price_in == 0 || price_out == 0 {
            return Err(format!("{p}_PRICE_IN/_PRICE_OUT must be above zero"));
        }
        Ok(Self {
            kind,
            model,
            max_output_tokens: num("MAX_OUTPUT")?.unwrap_or(16_000),
            price_in_micros_per_mtok: price_in,
            price_out_micros_per_mtok: price_out,
            timeout: Duration::from_secs(num("TIMEOUT_SECS")?.unwrap_or(600)),
        })
    }

    /// Upper bound on the cost of one call. Input tokens are bounded by input bytes
    /// (every tokenizer here emits at most one token per byte of UTF-8).
    pub fn worst_case_cost_micros(&self, system: &str, user: &str) -> u64 {
        let in_tokens = (system.len() + user.len()) as u64;
        let base = cost_micros(in_tokens, self.price_in_micros_per_mtok).saturating_add(
            cost_micros(self.max_output_tokens, self.price_out_micros_per_mtok),
        );
        if self.kind == ProviderKind::Anthropic {
            base.saturating_add(
                base.saturating_mul(ANTHROPIC_FALLBACK_MARGIN_PERCENT)
                    .div_ceil(100),
            )
        } else {
            base
        }
    }

    pub fn actual_cost_micros(&self, r: &ProviderResponse) -> u64 {
        cost_micros(r.input_tokens, self.price_in_micros_per_mtok)
            .saturating_add(cost_micros(r.output_tokens, self.price_out_micros_per_mtok))
    }
}

/// tokens × price-per-million, rounded up.
fn cost_micros(tokens: u64, micros_per_mtok: u64) -> u64 {
    let v = u128::from(tokens) * u128::from(micros_per_mtok);
    u64::try_from(v.div_ceil(1_000_000)).unwrap_or(u64::MAX)
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct HttpRequest {
    pub url: String,
    pub headers: Vec<(String, String)>,
    pub body: String,
}

/// Build the provider-specific request for one system + user turn.
pub fn build_request(cfg: &ProviderConfig, key: &str, system: &str, user: &str) -> HttpRequest {
    let q = json::quote;
    let ct = ("Content-Type".to_string(), "application/json".to_string());
    match cfg.kind {
        ProviderKind::OpenAi => HttpRequest {
            url: "https://api.openai.com/v1/chat/completions".into(),
            headers: vec![ct, ("Authorization".into(), format!("Bearer {key}"))],
            body: format!(
                "{{\"model\":{},\"max_completion_tokens\":{},\"messages\":[{{\"role\":\"system\",\"content\":{}}},{{\"role\":\"user\",\"content\":{}}}]}}",
                q(&cfg.model),
                cfg.max_output_tokens,
                q(system),
                q(user)
            ),
        },
        ProviderKind::Anthropic => HttpRequest {
            url: "https://api.anthropic.com/v1/messages".into(),
            headers: vec![
                ct,
                ("x-api-key".into(), key.to_string()),
                ("anthropic-version".into(), ANTHROPIC_VERSION.into()),
                ("anthropic-beta".into(), ANTHROPIC_FALLBACK_BETA.into()),
            ],
            body: format!(
                "{{\"model\":{},\"max_tokens\":{},\"output_config\":{{\"effort\":\"high\"}},\"fallbacks\":\"default\",\"system\":{},\"messages\":[{{\"role\":\"user\",\"content\":{}}}]}}",
                q(&cfg.model),
                cfg.max_output_tokens,
                q(system),
                q(user)
            ),
        },
        ProviderKind::Gemini => HttpRequest {
            url: format!(
                "https://generativelanguage.googleapis.com/v1beta/models/{}:generateContent",
                cfg.model
            ),
            headers: vec![ct, ("x-goog-api-key".into(), key.to_string())],
            body: format!(
                "{{\"systemInstruction\":{{\"parts\":[{{\"text\":{}}}]}},\"contents\":[{{\"role\":\"user\",\"parts\":[{{\"text\":{}}}]}}],\"generationConfig\":{{\"maxOutputTokens\":{}}}}}",
                q(system),
                q(user),
                cfg.max_output_tokens
            ),
        },
        ProviderKind::Mock => HttpRequest {
            url: String::new(),
            headers: vec![],
            body: String::new(),
        },
    }
}

fn api_error(v: &Value) -> Option<String> {
    let e = v.get("error")?;
    Some(
        e.get("message")
            .and_then(Value::as_str)
            .or_else(|| e.as_str())
            .unwrap_or("provider returned an error")
            .to_string(),
    )
}

fn usage(v: &Value, input: &[&str], output: &[&str]) -> Result<(u64, u64), String> {
    let i = v.path(input).and_then(Value::as_u64);
    let o = v.path(output).and_then(Value::as_u64);
    match (i, o) {
        (Some(i), Some(o)) => Ok((i, o)),
        _ => Err("response has no usage counts; cost cannot be recorded".into()),
    }
}

/// Extract text and usage. Any refusal, truncation or missing usage is an error, so the
/// panel never treats a partial answer as a complete one.
pub fn parse_response(kind: ProviderKind, body: &str) -> Result<ProviderResponse, String> {
    let v = json::parse(body).map_err(|e| format!("invalid JSON from provider: {e}"))?;
    if let Some(e) = api_error(&v) {
        return Err(e);
    }
    let (text, (input_tokens, output_tokens)) = match kind {
        ProviderKind::OpenAi => {
            let choice = v.get("choices").and_then(|c| c.at(0)).ok_or("no choices")?;
            match choice.get("finish_reason").and_then(Value::as_str) {
                Some("stop") => {}
                Some(r) => return Err(format!("generation ended early: finish_reason={r}")),
                None => return Err("no finish_reason".into()),
            }
            let text = choice
                .path(&["message", "content"])
                .and_then(Value::as_str)
                .ok_or("no message content")?
                .to_string();
            (
                text,
                usage(
                    &v,
                    &["usage", "prompt_tokens"],
                    &["usage", "completion_tokens"],
                )?,
            )
        }
        ProviderKind::Anthropic => {
            match v.get("stop_reason").and_then(Value::as_str) {
                Some("end_turn") => {}
                Some("refusal") => {
                    let cat = v
                        .path(&["stop_details", "category"])
                        .and_then(Value::as_str)
                        .unwrap_or("unspecified");
                    return Err(format!(
                        "model declined the request (refusal, category {cat})"
                    ));
                }
                Some(r) => return Err(format!("generation ended early: stop_reason={r}")),
                None => return Err("no stop_reason".into()),
            }
            // Content holds thinking blocks too; only `text` blocks are the answer.
            let text: String = v
                .get("content")
                .and_then(Value::as_array)
                .ok_or("no content")?
                .iter()
                .filter(|b| b.get("type").and_then(Value::as_str) == Some("text"))
                .filter_map(|b| b.get("text").and_then(Value::as_str))
                .collect::<Vec<_>>()
                .join("");
            (
                text,
                usage(&v, &["usage", "input_tokens"], &["usage", "output_tokens"])?,
            )
        }
        ProviderKind::Gemini => {
            let cand = v.get("candidates").and_then(|c| c.at(0)).ok_or_else(|| {
                let reason = v
                    .path(&["promptFeedback", "blockReason"])
                    .and_then(Value::as_str)
                    .unwrap_or("none");
                format!("no candidates (blockReason {reason})")
            })?;
            match cand.get("finishReason").and_then(Value::as_str) {
                Some("STOP") => {}
                Some(r) => return Err(format!("generation ended early: finishReason={r}")),
                None => return Err("no finishReason".into()),
            }
            let text: String = cand
                .path(&["content", "parts"])
                .and_then(Value::as_array)
                .ok_or("no content parts")?
                .iter()
                .filter(|p| p.get("thought") != Some(&Value::Bool(true)))
                .filter_map(|p| p.get("text").and_then(Value::as_str))
                .collect::<Vec<_>>()
                .join("");
            // Thinking tokens bill as output; count them when the API reports them.
            let (i, o) = usage(
                &v,
                &["usageMetadata", "promptTokenCount"],
                &["usageMetadata", "candidatesTokenCount"],
            )?;
            let thoughts = v
                .path(&["usageMetadata", "thoughtsTokenCount"])
                .and_then(Value::as_u64)
                .unwrap_or(0);
            (text, (i, o.saturating_add(thoughts)))
        }
        ProviderKind::Mock => return Err("mock has no HTTP response".into()),
    };
    if text.trim().is_empty() {
        return Err("empty answer".into());
    }
    Ok(ProviderResponse {
        text,
        input_tokens,
        output_tokens,
    })
}

/// Sends one HTTP request; returns (status, body).
pub trait Transport {
    fn post(&self, req: &HttpRequest, timeout: Duration) -> Result<(u16, String), String>;
}

/// `curl` driven entirely through a config on stdin: URL, headers (including the key) and
/// body never reach argv.
pub struct CurlTransport;

/// Quote a value for a curl config file.
fn curl_quote(s: &str) -> String {
    let mut out = String::from("\"");
    for c in s.chars() {
        match c {
            '\\' => out.push_str("\\\\"),
            '"' => out.push_str("\\\""),
            '\n' => out.push_str("\\n"),
            '\r' => out.push_str("\\r"),
            '\t' => out.push_str("\\t"),
            c => out.push(c),
        }
    }
    out.push('"');
    out
}

pub fn curl_config(req: &HttpRequest, timeout: Duration) -> String {
    let mut cfg = String::new();
    cfg.push_str(&format!("url = {}\n", curl_quote(&req.url)));
    for (k, v) in &req.headers {
        cfg.push_str(&format!("header = {}\n", curl_quote(&format!("{k}: {v}"))));
    }
    cfg.push_str(&format!("data-binary = {}\n", curl_quote(&req.body)));
    cfg.push_str(&format!("max-time = {}\n", timeout.as_secs().max(1)));
    cfg.push_str("max-filesize = 8000000\n");
    cfg.push_str("silent\nshow-error\n");
    cfg.push_str("proto = \"=https\"\n");
    cfg.push_str("write-out = \"\\n%{http_code}\"\n");
    cfg
}

impl Transport for CurlTransport {
    fn post(&self, req: &HttpRequest, timeout: Duration) -> Result<(u16, String), String> {
        let mut child = Command::new("curl")
            .args(["--config", "-"])
            .stdin(Stdio::piped())
            .stdout(Stdio::piped())
            .stderr(Stdio::piped())
            .spawn()
            .map_err(|e| format!("cannot start curl: {e}"))?;
        child
            .stdin
            .take()
            .ok_or("curl stdin unavailable")?
            .write_all(curl_config(req, timeout).as_bytes())
            .map_err(|e| format!("cannot write curl config: {e}"))?;
        let out = child
            .wait_with_output()
            .map_err(|e| format!("curl failed: {e}"))?;
        if !out.status.success() {
            return Err(format!(
                "curl exited with {}: {}",
                out.status,
                String::from_utf8_lossy(&out.stderr).trim()
            ));
        }
        let text = String::from_utf8(out.stdout).map_err(|_| "response is not UTF-8")?;
        let (body, code) = text.rsplit_once('\n').ok_or("no HTTP status from curl")?;
        let code = code
            .trim()
            .parse::<u16>()
            .map_err(|_| "bad HTTP status from curl")?;
        Ok((code, body.to_string()))
    }
}

/// Replace every occurrence of the key before text leaves this module.
pub fn redact(text: &str, key: &str) -> String {
    if key.len() < 8 {
        return text.to_string();
    }
    text.replace(key, "***")
}

/// One partner reachable over HTTP.
pub struct HttpProvider<T: Transport> {
    pub config: ProviderConfig,
    key: String,
    transport: T,
}

impl<T: Transport> HttpProvider<T> {
    pub fn new(config: ProviderConfig, key: String, transport: T) -> Result<Self, String> {
        if key.trim().is_empty() {
            return Err(format!("{} key is empty", config.kind.name()));
        }
        Ok(Self {
            config,
            key,
            transport,
        })
    }

    pub fn complete(&self, system: &str, user: &str) -> Result<ProviderResponse, String> {
        let req = build_request(&self.config, &self.key, system, user);
        let (status, body) = self
            .transport
            .post(&req, self.config.timeout)
            .map_err(|e| redact(&e, &self.key))?;
        let body = redact(&body, &self.key);
        if !(200..300).contains(&status) {
            let detail = json::parse(&body)
                .ok()
                .and_then(|v| api_error(&v))
                .unwrap_or_else(|| body.chars().take(300).collect());
            return Err(format!(
                "{} HTTP {status}: {detail}",
                self.config.kind.name()
            ));
        }
        parse_response(self.config.kind, &body)
            .map_err(|e| format!("{}: {e}", self.config.kind.name()))
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::cell::RefCell;
    use std::collections::HashMap;

    fn cfg(kind: ProviderKind) -> ProviderConfig {
        ProviderConfig {
            kind,
            model: "test-model".into(),
            max_output_tokens: 1000,
            price_in_micros_per_mtok: 4_000_000,
            price_out_micros_per_mtok: 20_000_000,
            timeout: Duration::from_secs(5),
        }
    }

    #[test]
    fn config_needs_model_and_price_except_anthropic_defaults() {
        let empty = |_: &str| None;
        let a = ProviderConfig::from_lookup(ProviderKind::Anthropic, empty).unwrap();
        assert_eq!(a.model, "claude-opus-5-5");
        assert_eq!(a.price_in_micros_per_mtok, 4_000_000);
        assert!(ProviderConfig::from_lookup(ProviderKind::OpenAi, empty)
            .unwrap_err()
            .contains("KARTAL_OPENAI_MODEL"));

        let env: HashMap<&str, &str> = [
            ("KARTAL_GEMINI_MODEL", "g-model"),
            ("KARTAL_GEMINI_PRICE_IN", "1000000"),
            ("KARTAL_GEMINI_PRICE_OUT", "8000000"),
            ("KARTAL_GEMINI_MAX_OUTPUT", "4000"),
        ]
        .into();
        let g = ProviderConfig::from_lookup(ProviderKind::Gemini, |k| {
            env.get(k).map(|v| v.to_string())
        })
        .unwrap();
        assert_eq!((g.model.as_str(), g.max_output_tokens), ("g-model", 4000));

        let bad: HashMap<&str, &str> = [
            ("KARTAL_GEMINI_MODEL", "m"),
            ("KARTAL_GEMINI_PRICE_IN", "abc"),
        ]
        .into();
        assert!(ProviderConfig::from_lookup(ProviderKind::Gemini, |k| bad
            .get(k)
            .map(|v| v.to_string()))
        .is_err());
    }

    #[test]
    fn worst_case_cost_bounds_input_by_bytes_and_output_by_max_tokens() {
        let c = cfg(ProviderKind::OpenAi);
        // 1000 bytes in at $4/M = 4000 µ$; 1000 out at $20/M = 20000 µ$.
        assert_eq!(
            c.worst_case_cost_micros(&"x".repeat(600), &"y".repeat(400)),
            24_000
        );
        // Anthropic adds a 25 % margin for a possible refusal fallback.
        assert_eq!(
            cfg(ProviderKind::Anthropic).worst_case_cost_micros(&"x".repeat(600), &"y".repeat(400)),
            30_000
        );
        let r = ProviderResponse {
            text: "t".into(),
            input_tokens: 1,
            output_tokens: 1,
        };
        assert_eq!(c.actual_cost_micros(&r), 4 + 20, "rounded up, never down");
    }

    #[test]
    fn requests_carry_model_prompt_and_key_in_the_right_place() {
        for kind in [
            ProviderKind::OpenAi,
            ProviderKind::Anthropic,
            ProviderKind::Gemini,
        ] {
            let r = build_request(&cfg(kind), "sk-secret-123", "SYS \"q\"", "görev\nsatır");
            let body = json::parse(&r.body).expect("body is valid JSON");
            assert!(!r.body.contains("sk-secret-123"), "key never in the body");
            assert!(r.headers.iter().any(|(_, v)| v.contains("sk-secret-123")));
            assert!(r.url.starts_with("https://"));
            let text = format!("{body:?}");
            assert!(
                text.contains("SYS \\\"q\\\"") && text.contains("görev\\nsatır"),
                "{kind:?}"
            );
        }
        let a = build_request(&cfg(ProviderKind::Anthropic), "k", "s", "u");
        let v = json::parse(&a.body).unwrap();
        assert_eq!(v.get("fallbacks").and_then(Value::as_str), Some("default"));
        assert_eq!(
            v.path(&["output_config", "effort"]).and_then(Value::as_str),
            Some("high")
        );
        assert!(a
            .headers
            .contains(&("anthropic-version".into(), "2026-10-21".into())));
        let g = build_request(&cfg(ProviderKind::Gemini), "k", "s", "u");
        assert!(g.url.ends_with("/models/test-model:generateContent"));
    }

    #[test]
    fn parses_successful_responses() {
        let o = r#"{"choices":[{"finish_reason":"stop","message":{"role":"assistant","content":"KARAR: KABUL"}}],"usage":{"prompt_tokens":12,"completion_tokens":5}}"#;
        let r = parse_response(ProviderKind::OpenAi, o).unwrap();
        assert_eq!(
            (r.text.as_str(), r.input_tokens, r.output_tokens),
            ("KARAR: KABUL", 12, 5)
        );

        let a = r###"{"content":[{"type":"thinking","thinking":""},{"type":"text","text":"## Sorun\n"},{"type":"text","text":"x"}],"stop_reason":"end_turn","usage":{"input_tokens":30,"output_tokens":400}}"###;
        let r = parse_response(ProviderKind::Anthropic, a).unwrap();
        assert_eq!((r.text.as_str(), r.output_tokens), ("## Sorun\nx", 400));

        let g = r#"{"candidates":[{"finishReason":"STOP","content":{"parts":[{"text":"plan","thought":true},{"text":"KARAR: RET"}]}}],"usageMetadata":{"promptTokenCount":9,"candidatesTokenCount":3,"thoughtsTokenCount":7}}"#;
        let r = parse_response(ProviderKind::Gemini, g).unwrap();
        assert_eq!((r.text.as_str(), r.output_tokens), ("KARAR: RET", 10));
    }

    #[test]
    fn partial_refused_or_unpriced_answers_are_errors() {
        let cut = r#"{"choices":[{"finish_reason":"length","message":{"content":"half"}}],"usage":{"prompt_tokens":1,"completion_tokens":1}}"#;
        assert!(parse_response(ProviderKind::OpenAi, cut)
            .unwrap_err()
            .contains("length"));

        let refusal = r#"{"content":[],"stop_reason":"refusal","stop_details":{"type":"refusal","category":"cyber"},"usage":{"input_tokens":1,"output_tokens":0}}"#;
        assert!(parse_response(ProviderKind::Anthropic, refusal)
            .unwrap_err()
            .contains("cyber"));

        let blocked = r#"{"promptFeedback":{"blockReason":"SAFETY"}}"#;
        assert!(parse_response(ProviderKind::Gemini, blocked)
            .unwrap_err()
            .contains("SAFETY"));

        let no_usage = r#"{"content":[{"type":"text","text":"x"}],"stop_reason":"end_turn"}"#;
        assert!(parse_response(ProviderKind::Anthropic, no_usage)
            .unwrap_err()
            .contains("usage"));

        let err = r#"{"error":{"type":"invalid_request_error","message":"bad model"}}"#;
        assert_eq!(
            parse_response(ProviderKind::Anthropic, err).unwrap_err(),
            "bad model"
        );
    }

    #[test]
    fn curl_config_quotes_everything_and_restricts_protocol() {
        let req = HttpRequest {
            url: "https://example.test/x".into(),
            headers: vec![("x-api-key".into(), "k\"ey".into())],
            body: "{\"a\":\"b\\\\c\"}".into(),
        };
        let c = curl_config(&req, Duration::from_secs(30));
        assert!(c.contains("header = \"x-api-key: k\\\"ey\"\n"));
        assert!(c.contains("data-binary = \"{\\\"a\\\":\\\"b\\\\\\\\c\\\"}\"\n"));
        assert!(c.contains("proto = \"=https\"") && c.contains("max-time = 30"));
    }

    struct FakeTransport {
        reply: (u16, String),
        seen: RefCell<Vec<HttpRequest>>,
    }
    impl Transport for FakeTransport {
        fn post(&self, req: &HttpRequest, _: Duration) -> Result<(u16, String), String> {
            self.seen.borrow_mut().push(req.clone());
            Ok(self.reply.clone())
        }
    }

    #[test]
    fn http_errors_are_reported_without_the_key() {
        let key = "sk-live-abcdefgh";
        let t = FakeTransport {
            reply: (
                401,
                format!(r#"{{"error":{{"message":"invalid key {key}"}}}}"#),
            ),
            seen: RefCell::new(vec![]),
        };
        let p = HttpProvider::new(cfg(ProviderKind::OpenAi), key.into(), t).unwrap();
        let e = p.complete("s", "u").unwrap_err();
        assert!(e.contains("HTTP 401") && !e.contains(key), "{e}");
        assert!(HttpProvider::new(cfg(ProviderKind::OpenAi), " ".into(), CurlTransport).is_err());
    }
}
