//! Fit generated meshes (for example Tripo AI GLB parts) to the Kartal S twin.
//!
//! A generated mesh has an arbitrary size, origin and heading. This crate reads its
//! bounding box from the GLB itself (glTF requires `min`/`max` on every POSITION
//! accessor), turns it so the vehicle front faces glTF +Z (D-003: VCS front = -X),
//! scales it uniformly to one resolved dimension of the twin, places it, and measures
//! how far the other proportions are from the twin's dimensions.
//!
//! Meshes are never edited: the output is a placement (position, quaternion, uniform
//! scale) that a viewer applies. A mesh's shape is a visual estimate, never measurement.

use kartal_agent_orchestrator::json::{self, Value};

pub type Vec3 = [f64; 3];

#[derive(Debug, Clone, Copy, PartialEq)]
pub struct Aabb {
    pub min: Vec3,
    pub max: Vec3,
}

impl Aabb {
    pub fn empty() -> Self {
        Aabb {
            min: [f64::INFINITY; 3],
            max: [f64::NEG_INFINITY; 3],
        }
    }
    pub fn is_empty(&self) -> bool {
        (0..3).any(|i| self.min[i] > self.max[i])
    }
    pub fn add(&mut self, p: Vec3) {
        for (i, v) in p.iter().enumerate() {
            self.min[i] = self.min[i].min(*v);
            self.max[i] = self.max[i].max(*v);
        }
    }
    pub fn size(&self) -> Vec3 {
        [0, 1, 2].map(|i| self.max[i] - self.min[i])
    }
    pub fn centre(&self) -> Vec3 {
        [0, 1, 2].map(|i| 0.5 * (self.max[i] + self.min[i]))
    }
    pub fn corners(&self) -> [Vec3; 8] {
        let (a, b) = (self.min, self.max);
        let mut out = [[0.0; 3]; 8];
        for (k, c) in out.iter_mut().enumerate() {
            *c = [
                if k & 1 == 0 { a[0] } else { b[0] },
                if k & 2 == 0 { a[1] } else { b[1] },
                if k & 4 == 0 { a[2] } else { b[2] },
            ];
        }
        out
    }
}

/// Column-major 4x4 matrix, as glTF stores it.
type Mat4 = [f64; 16];

const IDENTITY: Mat4 = [
    1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0,
];

fn mul(a: &Mat4, b: &Mat4) -> Mat4 {
    let mut r = [0.0; 16];
    for c in 0..4 {
        for row in 0..4 {
            r[c * 4 + row] = (0..4).map(|k| a[k * 4 + row] * b[c * 4 + k]).sum();
        }
    }
    r
}

fn apply(m: &Mat4, p: Vec3) -> Vec3 {
    [0, 1, 2].map(|row| m[row] * p[0] + m[4 + row] * p[1] + m[8 + row] * p[2] + m[12 + row])
}

fn trs(t: Vec3, q: [f64; 4], s: Vec3) -> Mat4 {
    let [x, y, z, w] = q;
    let r = [
        1.0 - 2.0 * (y * y + z * z),
        2.0 * (x * y + z * w),
        2.0 * (x * z - y * w),
        2.0 * (x * y - z * w),
        1.0 - 2.0 * (x * x + z * z),
        2.0 * (y * z + x * w),
        2.0 * (x * z + y * w),
        2.0 * (y * z - x * w),
        1.0 - 2.0 * (x * x + y * y),
    ];
    [
        r[0] * s[0],
        r[1] * s[0],
        r[2] * s[0],
        0.0,
        r[3] * s[1],
        r[4] * s[1],
        r[5] * s[1],
        0.0,
        r[6] * s[2],
        r[7] * s[2],
        r[8] * s[2],
        0.0,
        t[0],
        t[1],
        t[2],
        1.0,
    ]
}

fn num(v: &Value) -> Option<f64> {
    match v {
        Value::Num(n) => Some(*n),
        _ => None,
    }
}

fn nums<const N: usize>(v: Option<&Value>) -> Option<[f64; N]> {
    let a = v?.as_array()?;
    if a.len() != N {
        return None;
    }
    let mut out = [0.0; N];
    for (o, x) in out.iter_mut().zip(a) {
        *o = num(x)?;
    }
    Some(out)
}

fn index(v: Option<&Value>) -> Option<usize> {
    v.and_then(Value::as_u64).map(|n| n as usize)
}

/// The JSON chunk of a binary glTF (GLB 2.0) file.
pub fn glb_json(bytes: &[u8]) -> Result<Value, String> {
    let u32_at = |o: usize| -> Result<u32, String> {
        bytes
            .get(o..o + 4)
            .map(|b| u32::from_le_bytes([b[0], b[1], b[2], b[3]]))
            .ok_or_else(|| "file too short for a GLB header".to_string())
    };
    if bytes.get(0..4) != Some(b"glTF") {
        return Err("not a GLB file (magic is not 'glTF')".into());
    }
    if u32_at(4)? != 2 {
        return Err("only glTF 2.0 GLB files are supported".into());
    }
    let len = u32_at(12)? as usize;
    if u32_at(16)? != 0x4E4F_534A {
        return Err("first GLB chunk is not JSON".into());
    }
    let chunk = bytes
        .get(20..20 + len)
        .ok_or("JSON chunk runs past the end of the file")?;
    let text = std::str::from_utf8(chunk).map_err(|_| "JSON chunk is not UTF-8")?;
    json::parse(text.trim_end_matches([' ', '\0'])).map_err(|e| format!("GLB JSON: {e}"))
}

/// World-space bounding box of everything the default scene draws.
pub fn scene_bounds(gltf: &Value) -> Result<Aabb, String> {
    let empty: Vec<Value> = Vec::new();
    let nodes = gltf
        .get("nodes")
        .and_then(Value::as_array)
        .unwrap_or(&empty);
    let meshes = gltf
        .get("meshes")
        .and_then(Value::as_array)
        .unwrap_or(&empty);
    let accessors = gltf
        .get("accessors")
        .and_then(Value::as_array)
        .unwrap_or(&empty);
    let scene_i = index(gltf.get("scene")).unwrap_or(0);
    let roots: Vec<usize> = match gltf.get("scenes").and_then(|s| s.at(scene_i)) {
        Some(s) => s
            .get("nodes")
            .and_then(Value::as_array)
            .unwrap_or(&empty)
            .iter()
            .filter_map(|v| index(Some(v)))
            .collect(),
        None => (0..nodes.len()).collect(),
    };

    let mut bb = Aabb::empty();
    let mut stack: Vec<(usize, Mat4, usize)> =
        roots.into_iter().map(|n| (n, IDENTITY, 0)).collect();
    while let Some((ni, parent, depth)) = stack.pop() {
        if depth > 64 {
            return Err("node hierarchy deeper than 64 (cycle?)".into());
        }
        let node = nodes.get(ni).ok_or(format!("node {ni} does not exist"))?;
        let local = match nums::<16>(node.get("matrix")) {
            Some(m) => m,
            None => trs(
                nums::<3>(node.get("translation")).unwrap_or([0.0; 3]),
                nums::<4>(node.get("rotation")).unwrap_or([0.0, 0.0, 0.0, 1.0]),
                nums::<3>(node.get("scale")).unwrap_or([1.0; 3]),
            ),
        };
        let world = mul(&parent, &local);
        if let Some(mi) = index(node.get("mesh")) {
            let mesh = meshes.get(mi).ok_or(format!("mesh {mi} does not exist"))?;
            for prim in mesh
                .get("primitives")
                .and_then(Value::as_array)
                .unwrap_or(&empty)
            {
                let Some(ai) = index(prim.path(&["attributes", "POSITION"])) else {
                    continue;
                };
                let acc = accessors
                    .get(ai)
                    .ok_or(format!("accessor {ai} does not exist"))?;
                let (Some(mn), Some(mx)) = (nums::<3>(acc.get("min")), nums::<3>(acc.get("max")))
                else {
                    return Err(format!(
                        "POSITION accessor {ai} has no min/max (required by glTF)"
                    ));
                };
                for c in (Aabb { min: mn, max: mx }).corners() {
                    bb.add(apply(&world, c));
                }
            }
        }
        for child in node
            .get("children")
            .and_then(Value::as_array)
            .unwrap_or(&empty)
        {
            if let Some(ci) = index(Some(child)) {
                stack.push((ci, world, depth + 1));
            }
        }
    }
    if bb.is_empty() {
        return Err("the scene draws no mesh".into());
    }
    Ok(bb)
}

/// Which way the model's front points, in the model's own glTF axes (Y is up).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Front {
    PosZ,
    NegZ,
    PosX,
    NegX,
}

impl Front {
    pub fn parse(s: &str) -> Option<Front> {
        Some(match s {
            "+z" => Front::PosZ,
            "-z" => Front::NegZ,
            "+x" => Front::PosX,
            "-x" => Front::NegX,
            _ => return None,
        })
    }
    /// Yaw (about +Y, radians) that turns this front onto glTF +Z.
    pub fn yaw(self) -> f64 {
        use std::f64::consts::FRAC_PI_2;
        match self {
            Front::PosZ => 0.0,
            Front::NegZ => 2.0 * FRAC_PI_2,
            Front::PosX => -FRAC_PI_2,
            Front::NegX => FRAC_PI_2,
        }
    }
}

pub fn yaw_quat(yaw: f64) -> [f64; 4] {
    [0.0, (yaw / 2.0).sin(), 0.0, (yaw / 2.0).cos()]
}

fn rot_y(p: Vec3, yaw: f64) -> Vec3 {
    let (s, c) = yaw.sin_cos();
    [p[0] * c + p[2] * s, p[1], -p[0] * s + p[2] * c]
}

fn rotated(bb: &Aabb, yaw: f64) -> Aabb {
    let mut out = Aabb::empty();
    for c in bb.corners() {
        out.add(rot_y(c, yaw));
    }
    out
}

/// VCS millimetres (X rearward, Y right, Z up) to glTF metres (D-003).
pub fn vcs_to_gltf(p: Vec3) -> Vec3 {
    [-p[1] / 1000.0, p[2] / 1000.0, -p[0] / 1000.0]
}

/// A target box in VCS millimetres, converted to a glTF box.
pub fn vcs_box(x: [f64; 2], y: [f64; 2], z: [f64; 2]) -> Aabb {
    let mut bb = Aabb::empty();
    for p in [[x[0], y[0], z[0]], [x[1], y[1], z[1]]] {
        bb.add(vcs_to_gltf(p));
    }
    bb
}

#[derive(Debug, Clone, PartialEq)]
pub struct Instance {
    pub name: String,
    pub position: Vec3,
    pub quaternion: [f64; 4],
    pub scale: f64,
}

#[derive(Debug, Clone, PartialEq)]
pub struct AxisCheck {
    pub axis: &'static str,
    pub fitted_m: f64,
    pub target_m: f64,
    /// (fitted - target) / target
    pub deviation: f64,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub enum Status {
    Consistent,
    Warn,
    Inconsistent,
}

impl Status {
    pub fn as_str(self) -> &'static str {
        match self {
            Status::Consistent => "CONSISTENT",
            Status::Warn => "WARN",
            Status::Inconsistent => "INCONSISTENT",
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq)]
pub struct Limits {
    pub warn: f64,
    pub fail: f64,
}

impl Default for Limits {
    fn default() -> Self {
        // Beyond 3 % a proportion is visibly off at car scale (about 130 mm on the length);
        // beyond 8 % the mesh is a different shape and should be regenerated.
        Limits {
            warn: 0.03,
            fail: 0.08,
        }
    }
}

pub fn status_of(checks: &[AxisCheck], lim: Limits) -> Status {
    checks
        .iter()
        .map(|c| {
            let d = c.deviation.abs();
            if d > lim.fail {
                Status::Inconsistent
            } else if d > lim.warn {
                Status::Warn
            } else {
                Status::Consistent
            }
        })
        .max()
        .unwrap_or(Status::Consistent)
}

#[derive(Debug, Clone, PartialEq)]
pub struct Fit {
    pub instances: Vec<Instance>,
    pub checks: Vec<AxisCheck>,
}

fn check(axis: &'static str, fitted: f64, target: f64) -> AxisCheck {
    AxisCheck {
        axis,
        fitted_m: fitted,
        target_m: target,
        deviation: (fitted - target) / target,
    }
}

/// Fit a model into a glTF target box: turn it front-to-+Z, scale it uniformly so that
/// its length (Z) matches, centre it on X/Z and stand it on the box floor (Y min).
/// Width (X) and height (Y) are not forced: their deviations are the consistency check.
pub fn fit_by_length(model: &Aabb, front: Front, target: &Aabb, name: &str) -> Result<Fit, String> {
    fit_by_length_anchored(model, front, target, target, name, Anchor::Floor)
}

/// Vertical anchor: a whole car stands on the ground; a body without wheels hangs from
/// the roof line, because its underbody height (ground clearance) is not known.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Anchor {
    Floor,
    Roof,
}

/// `target` places and scales the mesh (body length, ground, centre line); `check` holds
/// the overall sizes the mesh is compared with. They differ for a whole car: its mesh
/// includes mirrors and roof rails, which the body box does not.
pub fn fit_by_length_anchored(
    model: &Aabb,
    front: Front,
    target: &Aabb,
    check_box: &Aabb,
    name: &str,
    anchor: Anchor,
) -> Result<Fit, String> {
    let yaw = front.yaw();
    let r = rotated(model, yaw);
    let size = r.size();
    if size.iter().any(|v| *v <= 0.0) {
        return Err("model bounding box is flat in at least one axis".into());
    }
    let ts = target.size();
    let s = ts[2] / size[2];
    let rc = r.centre();
    let tc = target.centre();
    let y = match anchor {
        Anchor::Floor => target.min[1] - s * r.min[1],
        Anchor::Roof => target.max[1] - s * r.max[1],
    };
    let position = [tc[0] - s * rc[0], y, tc[2] - s * rc[2]];
    let cs = check_box.size();
    let mut checks = vec![check("width", s * size[0], cs[0])];
    if anchor == Anchor::Floor {
        checks.push(check("height", s * size[1], cs[1]));
    }
    Ok(Fit {
        instances: vec![Instance {
            name: name.to_string(),
            position,
            quaternion: yaw_quat(yaw),
            scale: s,
        }],
        checks,
    })
}

/// Fit one wheel model to the tire outer diameter and place it at every wheel centre.
/// The axle axis is the model's smallest extent. Right-side instances are turned 180°
/// so the same face points outboard on both sides.
pub fn fit_wheel(
    model: &Aabb,
    outer_diameter_mm: f64,
    width_mm: f64,
    centres_vcs_mm: &[(String, Vec3)],
) -> Result<Fit, String> {
    let sz = model.size();
    let axle = (0..3)
        .min_by(|a, b| sz[*a].total_cmp(&sz[*b]))
        .expect("three axes");
    if axle == 1 {
        return Err(
            "wheel model is flattest along Y (lying on its side); export it standing".into(),
        );
    }
    let others: Vec<f64> = (0..3).filter(|i| *i != axle).map(|i| sz[i]).collect();
    let model_d = 0.5 * (others[0] + others[1]);
    let s = outer_diameter_mm / 1000.0 / model_d;
    // Turn the axle onto glTF X (the VCS lateral axis) first.
    let base_yaw = if axle == 2 {
        std::f64::consts::FRAC_PI_2
    } else {
        0.0
    };
    let c = model.centre();
    let mut instances = Vec::new();
    for (name, p) in centres_vcs_mm {
        let yaw = base_yaw
            + if p[1] > 0.0 {
                std::f64::consts::PI
            } else {
                0.0
            };
        let rc = rot_y(c, yaw);
        let g = vcs_to_gltf(*p);
        instances.push(Instance {
            name: name.clone(),
            position: [g[0] - s * rc[0], g[1] - s * rc[1], g[2] - s * rc[2]],
            quaternion: yaw_quat(yaw),
            scale: s,
        });
    }
    Ok(Fit {
        instances,
        checks: vec![
            check(
                "roundness",
                s * others[0].min(others[1]),
                s * others[0].max(others[1]),
            ),
            check("width", s * sz[axle], width_mm / 1000.0),
        ],
    })
}

#[cfg(test)]
mod tests {
    use super::*;

    fn bb(min: Vec3, max: Vec3) -> Aabb {
        Aabb { min, max }
    }

    fn close(a: f64, b: f64) -> bool {
        (a - b).abs() < 1e-9
    }

    /// Minimal GLB: one node with a TRS transform, one mesh, one POSITION accessor.
    fn glb(json_text: &str) -> Vec<u8> {
        let mut j = json_text.as_bytes().to_vec();
        while j.len() % 4 != 0 {
            j.push(b' ');
        }
        let total = 12 + 8 + j.len();
        let mut out = Vec::new();
        out.extend_from_slice(b"glTF");
        out.extend_from_slice(&2u32.to_le_bytes());
        out.extend_from_slice(&(total as u32).to_le_bytes());
        out.extend_from_slice(&(j.len() as u32).to_le_bytes());
        out.extend_from_slice(&0x4E4F_534Au32.to_le_bytes());
        out.extend_from_slice(&j);
        out
    }

    const SCENE: &str = r#"{"asset":{"version":"2.0"},"scene":0,"scenes":[{"nodes":[0]}],
        "nodes":[{"translation":[10,0,0],"scale":[2,2,2],"children":[1]},{"mesh":0,"translation":[0,1,0]}],
        "meshes":[{"primitives":[{"attributes":{"POSITION":0}}]}],
        "accessors":[{"count":3,"type":"VEC3","componentType":5126,"min":[-1,0,-2],"max":[1,1,2]}]}"#;

    #[test]
    fn reads_bounds_through_the_node_hierarchy() {
        let v = glb_json(&glb(SCENE)).unwrap();
        let b = scene_bounds(&v).unwrap();
        // child translate (0,1,0), parent scale 2 then translate (10,0,0)
        assert_eq!(b.min, [8.0, 2.0, -4.0]);
        assert_eq!(b.max, [12.0, 4.0, 4.0]);
    }

    #[test]
    fn rejects_non_glb_and_missing_bounds() {
        assert!(glb_json(b"PK\x03\x04zip").is_err());
        let no_minmax = SCENE.replace(r#","min":[-1,0,-2],"max":[1,1,2]"#, "");
        let v = glb_json(&glb(&no_minmax)).unwrap();
        assert!(scene_bounds(&v).unwrap_err().contains("min/max"));
    }

    #[test]
    fn vcs_mapping_matches_d003() {
        // Front wheel centre line at X=0; a point 1000 mm behind it, 500 right, 300 up.
        assert_eq!(vcs_to_gltf([1000.0, 500.0, 300.0]), [-0.5, 0.3, -1.0]);
    }

    #[test]
    fn a_car_facing_plus_x_is_turned_scaled_and_grounded() {
        // A model 8.792 long on X (front +X), 3.284 wide, 2.992 tall, floating at y=5.
        let model = bb([-4.0, 5.0, -1.642], [4.792, 7.992, 1.642]);
        let target = vcs_box([-830.0, 3566.0], [-821.0, 821.0], [0.0, 1496.0]);
        let f = fit_by_length(&model, Front::PosX, &target, "car").unwrap();
        let i = &f.instances[0];
        assert!(close(i.scale, 0.5));
        // apply placement to the model box and compare with the target
        let mut placed = Aabb::empty();
        for c in model.corners() {
            let r = rot_y(c, Front::PosX.yaw());
            placed.add([0, 1, 2].map(|k| i.position[k] + i.scale * r[k]));
        }
        for k in 0..3 {
            assert!((placed.min[k] - target.min[k]).abs() < 1e-9, "min {k}");
            assert!((placed.max[k] - target.max[k]).abs() < 1e-9, "max {k}");
        }
        assert_eq!(status_of(&f.checks, Limits::default()), Status::Consistent);
    }

    #[test]
    fn wrong_proportions_are_flagged() {
        // Same length but 10 % too tall.
        let model = bb([0.0, 0.0, 0.0], [1.642, 1.6456, 4.396]);
        let target = vcs_box([-830.0, 3566.0], [-821.0, 821.0], [0.0, 1496.0]);
        let f = fit_by_length(&model, Front::PosZ, &target, "car").unwrap();
        assert!(close(f.instances[0].scale, 1.0));
        let h = f.checks.iter().find(|c| c.axis == "height").unwrap();
        assert!((h.deviation - 0.1).abs() < 1e-3);
        assert_eq!(
            status_of(&f.checks, Limits::default()),
            Status::Inconsistent
        );
    }

    #[test]
    fn wheels_go_to_every_centre_with_the_right_diameter() {
        // Wheel model 2 units in diameter, 0.6 thick along Z (axle on Z), centred at origin.
        let model = bb([-1.0, -1.0, -0.3], [1.0, 1.0, 0.3]);
        let centres = vec![
            ("FL".to_string(), [0.0, -693.0, 298.05]),
            ("FR".to_string(), [0.0, 693.0, 298.05]),
        ];
        let f = fit_wheel(&model, 596.1, 185.0, &centres).unwrap();
        assert!(close(f.instances[0].scale, 0.5961 / 2.0));
        // centre lands on the wheel centre (model centre is the origin)
        let g = vcs_to_gltf([0.0, -693.0, 298.05]);
        for (k, gk) in g.iter().enumerate() {
            assert!(close(f.instances[0].position[k], *gk));
        }
        // right wheel turned 180 degrees relative to the left one
        let (ql, qr) = (f.instances[0].quaternion, f.instances[1].quaternion);
        let dot: f64 = (0..4).map(|k| ql[k] * qr[k]).sum();
        assert!(dot.abs() < 1e-9, "quaternions differ by 180 deg about Y");
        let w = f.checks.iter().find(|c| c.axis == "width").unwrap();
        assert!((w.fitted_m - 0.6 * 0.29805).abs() < 1e-9);
    }

    #[test]
    fn a_body_without_wheels_hangs_from_the_roof_line() {
        let model = bb([0.0, 0.0, 0.0], [1.642, 1.2, 4.396]);
        let target = vcs_box([-830.0, 3566.0], [-821.0, 821.0], [0.0, 1496.0]);
        let f = fit_by_length_anchored(&model, Front::PosZ, &target, &target, "body", Anchor::Roof)
            .unwrap();
        let i = &f.instances[0];
        assert!(close(i.position[1] + i.scale * 1.2, 1.496));
        assert_eq!(
            f.checks.len(),
            1,
            "height is not checked for a body hung from the roof"
        );
    }

    #[test]
    fn a_wheel_lying_flat_is_refused() {
        let flat = bb([-1.0, -0.3, -1.0], [1.0, 0.3, 1.0]);
        assert!(fit_wheel(&flat, 600.0, 185.0, &[]).is_err());
    }
}
