//! meshfit: place generated GLB parts (e.g. from Tripo AI) on the Kartal S twin.
//!
//!   meshfit inspect FILE.glb
//!   meshfit fit --params build/blender/params.json --parts assembly/tripo_parts.json \
//!               --dir refs/derived/tripo --out build/tripo/placements.json
//!
//! Exit codes: 0 every present part CONSISTENT, 1 a WARN, 2 an INCONSISTENT part,
//! 3 a part file missing or unreadable, 64 usage error.

use kartal_agent_orchestrator::json::{self, quote, Value};
use kartal_meshfit::*;
use std::path::{Path, PathBuf};

const USAGE: &str = "usage:
  meshfit inspect FILE.glb
  meshfit fit --params PARAMS.json --parts PARTS.json --dir GLB_DIR --out PLACEMENTS.json";

fn read_json(path: &Path) -> Result<Value, String> {
    let text = std::fs::read_to_string(path).map_err(|e| format!("{}: {e}", path.display()))?;
    json::parse(&text).map_err(|e| format!("{}: {e}", path.display()))
}

fn bounds_of(path: &Path) -> Result<Aabb, String> {
    let bytes = std::fs::read(path).map_err(|e| format!("{}: {e}", path.display()))?;
    scene_bounds(&glb_json(&bytes)?)
}

fn f(v: Option<&Value>, what: &str) -> Result<f64, String> {
    match v {
        Some(Value::Num(n)) => Ok(*n),
        _ => Err(format!("params.json: {what} missing or not a number")),
    }
}

fn v3(v: Option<&Value>, what: &str) -> Result<Vec3, String> {
    let a = v
        .and_then(Value::as_array)
        .ok_or(format!("params.json: {what} missing"))?;
    if a.len() != 3 {
        return Err(format!("params.json: {what} is not a 3-vector"));
    }
    Ok([f(a.first(), what)?, f(a.get(1), what)?, f(a.get(2), what)?])
}

fn inspect(path: &Path) -> i32 {
    match bounds_of(path) {
        Ok(b) => {
            let s = b.size();
            let longest = if s[0] >= s[2] { "x" } else { "z" };
            println!("file={}", path.display());
            println!("min={:.4},{:.4},{:.4}", b.min[0], b.min[1], b.min[2]);
            println!("max={:.4},{:.4},{:.4}", b.max[0], b.max[1], b.max[2]);
            println!("size={:.4},{:.4},{:.4}", s[0], s[1], s[2]);
            println!(
                "longest_horizontal_axis={longest} (the car front is +{longest} or -{longest})"
            );
            0
        }
        Err(e) => {
            eprintln!("{e}");
            3
        }
    }
}

fn fmt3(v: Vec3) -> String {
    format!("[{:.6},{:.6},{:.6}]", v[0], v[1], v[2])
}

fn fit(params: &Path, parts: &Path, dir: &Path, out: &Path) -> i32 {
    let run = || -> Result<(String, i32), String> {
        let p = read_json(params)?;
        let cfg = read_json(parts)?;
        let prof = p.get("profile").ok_or("params.json: no profile")?;
        let (x0, x1) = (
            f(prof.get("x_front"), "profile.x_front")?,
            f(prof.get("x_rear"), "profile.x_rear")?,
        );
        let hw = f(prof.get("half_width"), "profile.half_width")?;
        let h = f(prof.get("height"), "profile.height")?;
        let car_box = vcs_box([x0, x1], [-hw, hw], [0.0, h]);
        // A whole-car mesh includes mirrors and roof rails: compare it with those sizes.
        let mp = f(
            p.path(&["values", "body_profile.mirror_protrusion"]),
            "values.body_profile.mirror_protrusion",
        )?;
        let rails = f(
            p.path(&["values", "dimensions.overall_height_roof_rails"]),
            "values.dimensions.overall_height_roof_rails",
        )?;
        let car_check = vcs_box([x0, x1], [-(hw + mp), hw + mp], [0.0, rails]);
        let basis = |key: &str| {
            p.path(&["provenance", key])
                .and_then(Value::as_str)
                .unwrap_or("UNTRACKED")
                .to_string()
        };
        let car_basis = format!(
            "length {}, width {} + mirrors {}, height with roof rails {}",
            basis("dimensions.overall_length"),
            basis("dimensions.overall_width_body"),
            basis("body_profile.mirror_protrusion"),
            basis("dimensions.overall_height_roof_rails")
        );
        let tire = p.get("tire").ok_or("params.json: no tire")?;
        let od = f(tire.get("od"), "tire.od")?;
        let tw = f(tire.get("width"), "tire.width")?;
        let mut centres = Vec::new();
        for k in ["FL", "FR", "RL", "RR"] {
            centres.push((
                k.to_string(),
                v3(p.path(&["wheels", k]), &format!("wheels.{k}"))?,
            ));
        }
        let lim = Limits::default();
        let empty = Vec::new();
        let mut worst = 0;
        let mut entries = Vec::new();
        for part in cfg.get("parts").and_then(Value::as_array).unwrap_or(&empty) {
            let id = part
                .get("id")
                .and_then(Value::as_str)
                .ok_or("parts.json: part without id")?;
            let file = part
                .get("file")
                .and_then(Value::as_str)
                .ok_or(format!("{id}: no file"))?;
            let kind = part.get("kind").and_then(Value::as_str).unwrap_or("car");
            let path: PathBuf = dir.join(file);
            if !path.exists() {
                println!("part {id}: MISSING {}", path.display());
                worst = worst.max(3);
                entries.push(format!(
                    "{{\"id\":{},\"file\":{},\"status\":\"MISSING\"}}",
                    quote(id),
                    quote(file)
                ));
                continue;
            }
            let model = bounds_of(&path).map_err(|e| format!("{id}: {e}"))?;
            let fitted = match kind {
                "car" | "body" => {
                    let front = part.get("front").and_then(Value::as_str).unwrap_or("+z");
                    let front = Front::parse(front)
                        .ok_or(format!("{id}: front must be +z, -z, +x or -x"))?;
                    let anchor = if kind == "car" {
                        Anchor::Floor
                    } else {
                        Anchor::Roof
                    };
                    let check_box = if kind == "car" { &car_check } else { &car_box };
                    println!("  check basis: {car_basis}");
                    fit_by_length_anchored(&model, front, &car_box, check_box, id, anchor)
                }
                "wheel" => fit_wheel(&model, od, tw, &centres),
                other => Err(format!("unknown kind {other} (car, body, wheel)")),
            }
            .map_err(|e| format!("{id}: {e}"))?;
            let st = status_of(&fitted.checks, lim);
            worst = worst.max(match st {
                Status::Consistent => 0,
                Status::Warn => 1,
                Status::Inconsistent => 2,
            });
            println!("part {id} ({kind}): {}", st.as_str());
            for c in &fitted.checks {
                println!(
                    "  {:<9} fitted {:.3} m, target {:.3} m, deviation {:+.1} %",
                    c.axis,
                    c.fitted_m,
                    c.target_m,
                    100.0 * c.deviation
                );
            }
            let inst: Vec<String> = fitted
                .instances
                .iter()
                .map(|i| {
                    format!(
                        "{{\"name\":{},\"position\":{},\"quaternion\":[{:.9},{:.9},{:.9},{:.9}],\"scale\":{:.9}}}",
                        quote(&i.name),
                        fmt3(i.position),
                        i.quaternion[0],
                        i.quaternion[1],
                        i.quaternion[2],
                        i.quaternion[3],
                        i.scale
                    )
                })
                .collect();
            let checks: Vec<String> = fitted
                .checks
                .iter()
                .map(|c| {
                    format!(
                        "{{\"axis\":{},\"fitted_m\":{:.4},\"target_m\":{:.4},\"deviation\":{:.4}}}",
                        quote(c.axis),
                        c.fitted_m,
                        c.target_m,
                        c.deviation
                    )
                })
                .collect();
            entries.push(format!(
                "{{\"id\":{},\"file\":{},\"kind\":{},\"status\":{},\"instances\":[{}],\"checks\":[{}]}}",
                quote(id),
                quote(file),
                quote(kind),
                quote(st.as_str()),
                inst.join(","),
                checks.join(",")
            ));
        }
        let aabb = |b: &Aabb| format!("{{\"min\":{},\"max\":{}}}", fmt3(b.min), fmt3(b.max));
        let wheels: Vec<String> = centres
            .iter()
            .map(|(n, c)| {
                format!(
                    "{{\"name\":{},\"centre\":{}}}",
                    quote(n),
                    fmt3(vcs_to_gltf(*c))
                )
            })
            .collect();
        let reference = format!(
            "{{\"body_box\":{},\"overall_box\":{},\"wheels\":[{}],\"tire_od_m\":{:.4},\"check_basis\":{}}}",
            aabb(&car_box),
            aabb(&car_check),
            wheels.join(","),
            od / 1000.0,
            quote(&car_basis)
        );
        let doc = format!(
            "{{\"generator\":\"meshfit {}\",\"reference\":{},\"frame\":\"glTF metres; VCS mm to glTF (x,y,z) = (-Y, Z, -X)/1000 (D-003)\",\
             \"representation\":\"visual estimate (generated mesh shape), not measurement\",\"parts\":[{}]}}\n",
            env!("CARGO_PKG_VERSION"),
            reference,
            entries.join(",")
        );
        Ok((doc, worst))
    };
    match run() {
        Ok((doc, worst)) => {
            if let Some(dirp) = out.parent() {
                let _ = std::fs::create_dir_all(dirp);
            }
            if let Err(e) = std::fs::write(out, doc) {
                eprintln!("{}: {e}", out.display());
                return 3;
            }
            println!("wrote {}", out.display());
            worst
        }
        Err(e) => {
            eprintln!("{e}");
            3
        }
    }
}

fn main() {
    let args: Vec<String> = std::env::args().skip(1).collect();
    let code = match args.first().map(String::as_str) {
        Some("inspect") if args.len() == 2 => inspect(Path::new(&args[1])),
        Some("fit") => {
            let get = |flag: &str| {
                args.iter()
                    .position(|a| a == flag)
                    .and_then(|i| args.get(i + 1))
                    .map(PathBuf::from)
            };
            match (get("--params"), get("--parts"), get("--dir"), get("--out")) {
                (Some(p), Some(c), Some(d), Some(o)) => fit(&p, &c, &d, &o),
                _ => {
                    eprintln!("{USAGE}");
                    64
                }
            }
        }
        _ => {
            eprintln!("{USAGE}");
            64
        }
    };
    std::process::exit(code);
}
