"""Blender (bpy 4.2) script: realistic VISUAL model of the 1997 Tofas Kartal S estate (VEH-01).

    <bpy-python> tools/blender/kartal_body.py build/blender/params.json build/blender/kartal_studio.glb [preview.png]

Shape: subdivision-surface lower body and greenhouse lofted from stations whose key dimensions
come from params.json (spec + placeholder assumptions, see tools/blender/export_params.py);
design cues from the owner's photos (E-022..E-028): S-series front with rectangular headlamps
and black grille, deep black wrap-around bumpers, tall vertical tail lamps, body-colour roof
rails, dark tinted glass, black pressed-steel wheels with 4 nuts, 185/65 R14 tires.
This is a VISUAL model: shapes between the parameterised stations are artistic, not measured.
Coordinates: VCS in metres (X rearward from the front axle, Y right, Z up).
"""
import json
import math
import sys

import bpy

args = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]
P = json.load(open(args[0]))
OUT = args[1]
PREVIEW = args[2] if len(args) > 2 else None
mm = 0.001
pr, gh, V = P["profile"], P["greenhouse"], P["values"]
XN, XT, HW = pr["x_nose"] * mm, pr["x_tail"] * mm, pr["half_width"] * mm
XF, XR = pr["x_front"] * mm, pr["x_rear"] * mm
SILL, BELT = V["body_profile.sill_z"] * mm, V["body_profile.belt_z"] * mm
NT, NB, RB = V["body_profile.nose_top_z"] * mm, V["body_profile.nose_bottom_z"] * mm, V["body_profile.rear_bottom_z"] * mm
COWL, XB, XC = V["body_profile.cowl_x"] * mm, V["body_profile.b_pillar_x"] * mm, V["body_profile.c_pillar_x"] * mm
ZR, HR, HB = gh["z_roof"] * mm, gh["half_roof"] * mm, gh["half_belt"] * mm
XWT, XRR, XBR = gh["x_roof_front"] * mm, gh["x_roof_rear"] * mm, gh["x_belt_rear"] * mm
BZ, BH = V["body_profile.bumper_bottom_z"] * mm, V["body_profile.bumper_height"] * mm
RAILS = V["dimensions.overall_height_roof_rails"] * mm
WHEELS = {k: [c * mm for c in v] for k, v in P["wheels"].items()}
TIRE_R, TIRE_W, RIM_R = P["tire"]["od"] / 2 * mm, P["tire"]["width"] * mm, P["tire"]["rim_r"] * mm

# ------------------------------------------------------------------------------ scene / materials
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene


def srgb(c):
    return ((c + 0.055) / 1.055) ** 2.4 if c > 0.04045 else c / 12.92


def mat(name, rgb, metal=0.0, rough=0.5, coat=0.0, alpha=1.0, emit=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    col = tuple(srgb(c) for c in rgb) + (1.0,)
    b.inputs["Base Color"].default_value = col
    b.inputs["Metallic"].default_value = metal
    b.inputs["Roughness"].default_value = rough
    if coat:
        b.inputs["Coat Weight"].default_value = coat
        b.inputs["Coat Roughness"].default_value = 0.03
    if emit:
        b.inputs["Emission Color"].default_value = col
        b.inputs["Emission Strength"].default_value = emit
    if alpha < 1.0:
        b.inputs["Alpha"].default_value = alpha
        m.blend_method = "BLEND"
        if hasattr(m, "surface_render_method"):
            m.surface_render_method = "BLENDED"
    return m


M = {
    "paint": mat("paint_turquoise_metallic", (0.12, 0.62, 0.61), metal=0.55, rough=0.3, coat=1.0),
    "glass": mat("glass_dark_tint", (0.02, 0.03, 0.035), rough=0.02, alpha=0.86),
    "frame": mat("black_window_frame", (0.02, 0.02, 0.022), rough=0.35),
    "plastic": mat("black_plastic", (0.035, 0.035, 0.038), rough=0.62),
    "rubber": mat("tire_rubber", (0.025, 0.025, 0.027), rough=0.86),
    "steel": mat("rim_black_steel", (0.03, 0.03, 0.032), metal=0.6, rough=0.38),
    "chrome": mat("chrome", (0.92, 0.92, 0.93), metal=1.0, rough=0.1),
    "lens": mat("headlamp_lens", (0.9, 0.93, 0.95), rough=0.02, alpha=0.35),
    "amber": mat("indicator_amber", (0.95, 0.45, 0.02), rough=0.12, alpha=0.9),
    "red": mat("tail_red", (0.62, 0.02, 0.02), rough=0.12, alpha=0.92),
    "redd": mat("tail_dark_band", (0.12, 0.01, 0.01), rough=0.15),
    "plate": mat("plate_blank", (0.88, 0.88, 0.86), rough=0.4),
    "gap": mat("panel_gap", (0.004, 0.004, 0.004), rough=0.8),
    "seat": mat("seat_beige", (0.62, 0.48, 0.28), rough=0.9),
    "interior": mat("interior_dark", (0.03, 0.03, 0.03), rough=0.7),
    "wheelbeige": mat("steering_wheel_beige", (0.85, 0.78, 0.62), rough=0.5),
}


def link(obj):
    bpy.context.collection.objects.link(obj)
    return obj


def mesh_obj(name, verts, faces, mats, mat_idx=None):
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.update()
    ob = link(bpy.data.objects.new(name, me))
    for m_ in mats:
        me.materials.append(M[m_])
    if mat_idx:
        for i, k in enumerate(mat_idx):
            me.polygons[i].material_index = k
    return ob


def apply_mods(ob):
    with bpy.context.temp_override(object=ob, active_object=ob, selected_objects=[ob], selected_editable_objects=[ob]):
        for m_ in list(ob.modifiers):
            bpy.ops.object.modifier_apply(modifier=m_.name)


def smooth(ob, angle=None):
    for p in ob.data.polygons:
        p.use_smooth = True
    if angle is not None:
        with bpy.context.temp_override(object=ob, active_object=ob, selected_objects=[ob], selected_editable_objects=[ob]):
            bpy.ops.object.shade_smooth_by_angle(angle=angle)


def subsurf(ob, level=2):
    m_ = ob.modifiers.new("subd", "SUBSURF")
    m_.levels = m_.render_levels = level
    apply_mods(ob)
    smooth(ob)


def rbox(name, x0, x1, y0, y1, z0, z1, m_, bevel=0.01, segs=3):
    """Box with bevelled edges (rounded); coordinate pairs may be given in any order."""
    x0, x1 = sorted((x0, x1))
    y0, y1 = sorted((y0, y1))
    z0, z1 = sorted((z0, z1))
    if min(x1 - x0, y1 - y0, z1 - z0) < 1e-4:
        return None
    bpy.ops.mesh.primitive_cube_add(size=1, location=((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2))
    ob = bpy.context.active_object
    ob.name = name
    ob.scale = (x1 - x0, y1 - y0, z1 - z0)
    with bpy.context.temp_override(object=ob, active_object=ob, selected_objects=[ob], selected_editable_objects=[ob]):
        bpy.ops.object.transform_apply(scale=True)
    if bevel:
        b = ob.modifiers.new("bevel", "BEVEL")
        b.width = min(bevel, (x1 - x0) / 2.2, (y1 - y0) / 2.2, (z1 - z0) / 2.2)
        b.segments = segs
        apply_mods(ob)
    ob.data.materials.append(M[m_])
    smooth(ob, math.radians(35))
    return ob


def cyl(name, loc, r, depth, axis, m_, verts=48, rot=None):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=depth, location=loc)
    ob = bpy.context.active_object
    ob.name = name
    ob.rotation_euler = rot or {"X": (0, math.pi / 2, 0), "Y": (math.pi / 2, 0, 0), "Z": (0, 0, 0)}[axis]
    ob.data.materials.append(M[m_])
    smooth(ob, math.radians(40))
    return ob


def boolean(target, cutter, op="DIFFERENCE"):
    """Boolean via the evaluated depsgraph (the operator path used a stale cutter transform and
    emptied the body)."""
    me = None
    for solver in ("EXACT", "FAST"):        # EXACT can collapse on aligned geometry: fall back
        m_ = target.modifiers.new("bool", "BOOLEAN")
        m_.operation, m_.object, m_.solver = op, cutter, solver
        if solver == "EXACT":
            m_.use_hole_tolerant = True
        bpy.context.view_layer.update()
        ev = target.evaluated_get(bpy.context.evaluated_depsgraph_get())
        me = bpy.data.meshes.new_from_object(ev)
        target.modifiers.clear()
        if me.polygons:
            break
    target.data = me
    bpy.data.objects.remove(cutter, do_unlink=True)
    if not me.polygons:
        raise RuntimeError(f"boolean emptied {target.name}")


# ------------------------------------------------------------------------------ lower body
def ztop(x):
    return NT + (BELT - NT) * (x - XN) / (COWL - XN) if x < COWL else BELT


def zbot(x):
    if x < XN + 0.15:
        return NB + (SILL - NB) * max(x - XN, 0) / 0.15
    if x > XT - 0.15:
        return SILL + (RB - SILL) * min(x - (XT - 0.15), 0.15) / 0.15
    return SILL


def half_ring(x, zb, zt, hw):
    h = zt - zb
    return [(0.0, zb), (hw * 0.72, zb), (hw - 0.035, zb + 0.025), (hw, zb + 0.16 * h), (hw + 0.006, zb + 0.5 * h),
            (hw - 0.004, zt - 0.06), (hw - 0.045, zt - 0.004), (hw * 0.55, zt + 0.012), (0.0, zt + 0.016)]


stations = [  # x, width inset, top drop, bottom lift - support stations keep the S-series nose and tail crisp
    (XN - 0.012, 0.022, 0.014, 0.015), (XN - 0.004, 0.008, 0.004, 0.004), (XN + 0.03, 0.0, 0.0, 0.0), (XN + 0.12, 0.0, 0.0, 0.0), (XN + 0.45, 0, 0, 0),
    (-0.40, 0, 0, 0), (0.0, 0, 0, 0), (0.40, 0, 0, 0), (COWL - 0.1, 0, 0, 0), (COWL, 0, 0, 0), (XB, 0, 0, 0),
    ((XB + XC) / 2, 0, 0, 0), (XC, 0, 0, 0), (2.49, 0, 0, 0), (2.80, 0, 0, 0), (3.15, 0, 0, 0),
    (XT - 0.12, 0.0, 0.0, 0.0), (XT - 0.03, 0.0, 0.0, 0.0), (XT + 0.004, 0.008, 0.004, 0.004), (XT + 0.012, 0.022, 0.014, 0.015)]
stations = sorted(stations)                  # rings must advance along X (an unsorted list folded the surface)
assert all(b[0] - a[0] > 0.002 for a, b in zip(stations, stations[1:])), "body stations unsorted or duplicated"
verts, faces = [], []
n_ring = None
for x, dw, dt, db in stations:
    hr = half_ring(x, zbot(x) + db, ztop(x) - dt, HW - dw)
    ring = [(x, -y, z) for y, z in reversed(hr[1:])] + [(x, y, z) for y, z in hr[:-1]]
    ring = ring[:-0 or None]
    if n_ring is None:
        n_ring = len(ring)
    verts += ring
ns = len(stations)
for s in range(ns - 1):
    for i in range(n_ring):
        a, b = s * n_ring + i, s * n_ring + (i + 1) % n_ring
        faces.append((a, b, b + n_ring, a + n_ring))
faces.append(tuple(reversed(range(n_ring))))
faces.append(tuple(range((ns - 1) * n_ring, ns * n_ring)))
body = mesh_obj("BDY-001_body", verts, faces, ["paint"])
subsurf(body, 2)
for k, (x, y, z) in WHEELS.items():   # wheel arches (cutter nudged 1.3 mm off the body stations)
    s = 1 if y > 0 else -1
    boolean(body, cyl(f"arch_cut_{k}", (x + 0.0013, s * (HW + 0.02 - 0.14), z + 0.0007), TIRE_R + 0.05, 0.30, "Y", "paint", verts=64))
    liner = cyl(f"{k}_wheel_well", (x, s * (HW - 0.17), z), TIRE_R + 0.045, 0.24, "Y", "interior", verts=64)
    boolean(liner, cyl("liner_in", (x, s * (HW - 0.17), z), TIRE_R + 0.03, 0.3, "Y", "interior", verts=64))


# ------------------------------------------------------------------------------ greenhouse
rows = [  # half width, z, x at the front end, x at the rear end
    (HB, BELT, COWL + 0.02, XBR),
    (HB - 0.018, BELT + 0.07, COWL + (XWT - COWL) * 0.13, XBR - 0.01),
    (HR + 0.03, ZR - 0.075, XWT - 0.06, XRR + 0.06),
    (HR - 0.03, ZR - 0.012, XWT - 0.005, XRR + 0.01),
    (HR * 0.55, ZR + 0.01, XWT + 0.02, XRR - 0.01),
    (0.0, ZR + 0.014, XWT + 0.025, XRR - 0.015)]


# Stations across the glass: A and D pillars follow the window outline (fraction u of each row),
# B and C pillars stand at a fixed x (near-vertical, as in photos E-026), clamped inside each row.
us = [("u", 0.0), ("u", 0.035), ("x", XB - 0.028), ("x", XB + 0.028), ("x", XC - 0.02), ("x", XC + 0.02),
      ("u", 0.955), ("u", 1.0)]
gverts = []
nr = 2 * len(rows) - 1                        # points across (LH edge -> roof centre -> RH edge)
for kind, val in us:
    pts = []
    # LH beltline -> roof centre -> RH beltline
    order = [(-1, r_) for r_ in rows] + [(1, r_) for r_ in reversed(rows[:-1])]
    for side, (hw_, z, xf, xr) in order:
        x = xf + (xr - xf) * val if kind == "u" else min(max(val, xf + 0.06), xr - 0.06)
        pts.append((x, side * hw_, z))
    gverts += pts
for i in range(nr):                           # stations must stay ordered along x in every row
    xs = [gverts[k * nr + i][0] for k in range(len(us))]
    assert all(b_ - a_ > 0.005 for a_, b_ in zip(xs, xs[1:])), f"greenhouse stations out of order in row {i}: {xs}"
gfaces, gmat = [], []
for i in range(len(us) - 1):
    for j in range(nr - 1):
        a, b = i * nr + j, i * nr + j + 1
        gfaces.append((a, a + nr, b + nr, b))
        side_row = min(j, nr - 2 - j)         # 0,1 = side window band (from either edge)
        if side_row <= 1:
            pillar = i in (0, 2, 4, 6)
            dark = i in (2, 4)
            gmat.append(1 if not pillar else (2 if dark else 0))
        else:
            gmat.append(0)
front_cap = [k * 1 for k in range(nr)]
rear_cap = [(len(us) - 1) * nr + k for k in range(nr)]
gfaces.append(tuple(reversed(front_cap)))
gmat.append(1)
gfaces.append(tuple(rear_cap))
gmat.append(1)
green = mesh_obj("BDY-002_greenhouse", gverts, gfaces, ["paint", "glass", "frame"], gmat)
subsurf(green, 2)

# ------------------------------------------------------------------------------ panel gaps, trim
def gap_v(x, z0, z1, side):
    rbox("gap", x - 0.0015, x + 0.0015, side * (HW + 0.002) - 0.002, side * (HW + 0.002) + 0.002, z0, z1, "gap", bevel=0)


for s in (-1, 1):
    for x in (COWL - 0.03, XB, XC):
        gap_v(x, SILL + 0.06, BELT - 0.05, s)
    rbox("side_moulding", -0.05 + TIRE_R + 0.08, 2.49 - TIRE_R - 0.08, s * HW - 0.012, s * HW + 0.012, SILL + 0.045, SILL + 0.10, "plastic", 0.006)
    xm = COWL + 0.16
    rbox("mirror", xm, xm + 0.13, s * (HW + 0.02), s * (HW + 0.12), BELT + 0.02, BELT + 0.12, "plastic", 0.03)
    rbox("mirror_glass", xm + 0.128, xm + 0.132, s * (HW + 0.03), s * (HW + 0.11), BELT + 0.03, BELT + 0.11, "chrome", 0)
    for x in (XB - 0.17, XC - 0.15):
        rbox("door_handle", x, x + 0.11, s * HW - 0.004, s * HW + 0.014, BELT - 0.105, BELT - 0.075, "plastic", 0.006)
    # body-colour roof rails with feet (photos E-026)
    y = s * (HR - 0.07)
    rbox("roof_rail", XWT + 0.15, XRR - 0.08, y - 0.013, y + 0.013, RAILS - 0.03, RAILS, "paint", 0.012)
    for x in (XWT + 0.17, XRR - 0.10):
        rbox("rail_foot", x - 0.04, x + 0.04, y - 0.016, y + 0.016, ZR - 0.01, RAILS - 0.02, "paint", 0.01)
rbox("fuel_flap", 2.85, 2.97, -HW - 0.002, -HW + 0.001, 0.74, 0.86, "gap", 0.02)
rbox("fuel_cap", 2.865, 2.955, -HW - 0.004, -HW - 0.001, 0.755, 0.845, "paint", 0.03)

# ------------------------------------------------------------------------------ front: bumper, grille, lamps
fz0, fz1 = NT - 0.20, NT - 0.04
rbox("EXT-001_front_bumper", XF, XN + 0.13, -HW + 0.005, HW - 0.005, BZ, BZ + BH, "plastic", 0.035)
for s in (-1, 1):
    rbox("bumper_wrap", XN + 0.05, XN + 0.32, s * HW - 0.025 if s > 0 else -HW - 0.012, s * HW + 0.012 if s > 0 else -HW + 0.025, BZ, BZ + BH, "plastic", 0.03)
rbox("bumper_intake", XF - 0.004, XF + 0.01, -0.42, 0.42, BZ + 0.035, BZ + 0.07, "gap", 0.01)
rbox("plate_front", XF - 0.012, XF - 0.002, -0.26, 0.26, BZ + 0.07, BZ + 0.18, "plate", 0.005)
rbox("grille_panel", XN - 0.026, XN - 0.005, -(HW - 0.43), HW - 0.43, fz0 + 0.01, fz1 - 0.01, "plastic", 0.01)
for k in range(6):
    z = fz0 + 0.025 + k * (fz1 - fz0 - 0.05) / 5
    rbox("grille_slat", XN - 0.034, XN - 0.024, -(HW - 0.45), HW - 0.45, z - 0.004, z + 0.004, "frame", 0.002)
rbox("badge", XN - 0.04, XN - 0.032, -0.035, 0.035, (fz0 + fz1) / 2 - 0.035, (fz0 + fz1) / 2 + 0.035, "chrome", 0.012)
for s in (-1, 1):
    y0, y1 = sorted((s * (HW - 0.42), s * (HW - 0.155)))
    rbox("LGT_headlamp_bezel", XN - 0.028, XN - 0.004, y0 - 0.008, y1 + 0.008, fz0 - 0.008, fz1 + 0.008, "plastic", 0.008)
    rbox("LGT_headlamp_reflector", XN - 0.032, XN - 0.02, y0, y1, fz0, fz1, "chrome", 0.006)
    rbox("LGT_headlamp_lens", XN - 0.04, XN - 0.033, y0 + 0.004, y1 - 0.004, fz0 + 0.004, fz1 - 0.004, "lens", 0.004)
    y0, y1 = sorted((s * (HW - 0.145), s * (HW - 0.03)))
    rbox("LGT_indicator", XN - 0.03, XN + 0.01, y0, y1, fz0, fz1, "amber", 0.01)
# wipers
for y0, y1 in ((-0.62, -0.08), (0.06, 0.52)):
    rbox("wiper", COWL - 0.02, COWL + 0.005, y0, y1, BELT + 0.012, BELT + 0.024, "plastic", 0.003)

# ------------------------------------------------------------------------------ rear: tailgate, lamps, bumper
rbox("EXT-002_rear_bumper", XT - 0.11, XR, -HW + 0.005, HW - 0.005, BZ, BZ + BH, "plastic", 0.035)
for s in (-1, 1):
    rbox("bumper_wrap_r", XT - 0.30, XT - 0.04, s * HW - 0.025 if s > 0 else -HW - 0.012, s * HW + 0.012 if s > 0 else -HW + 0.025, BZ, BZ + BH, "plastic", 0.03)
    y0, y1 = sorted((s * (HW - 0.22), s * (HW - 0.025)))
    rbox("LGT_tail_lamp", XT - 0.01, XT + 0.03, y0, y1, RB + 0.12, BELT - 0.08, "red", 0.012)
    rbox("LGT_tail_band", XT + 0.028, XT + 0.034, y0 + 0.01, y1 - 0.01, RB + 0.27, RB + 0.33, "redd", 0.004)
    gap_y = s * (HW - 0.235)
    rbox("tailgate_gap", XT + 0.011, XT + 0.015, gap_y - 0.0015, gap_y + 0.0015, RB + 0.05, BELT - 0.02, "gap", 0)
rbox("tailgate_handle", XT + 0.015, XT + 0.045, -0.33, 0.33, RB + 0.17, RB + 0.21, "plastic", 0.01)
rbox("plate_rear", XT + 0.016, XT + 0.026, -0.26, 0.26, RB + 0.04, RB + 0.155, "plate", 0.005)
rbox("rear_wiper", XT - 0.02, XT + 0.03, -0.02, 0.36, BELT + 0.04, BELT + 0.055, "plastic", 0.004)

# ------------------------------------------------------------------------------ wheels
def revolve(name, profile, m_, steps=72):
    """Profile [(r, y)] in the XY plane revolved about the local Y axis (the wheel axis)."""
    me = bpy.data.meshes.new(name)
    vs = [(r, y, 0.0) for r, y in profile]
    me.from_pydata(vs, [(i, i + 1) for i in range(len(vs) - 1)] + [(len(vs) - 1, 0)], [])
    ob = link(bpy.data.objects.new(name, me))
    sc = ob.modifiers.new("screw", "SCREW")
    sc.axis, sc.steps, sc.render_steps, sc.angle = "Y", steps, steps, 2 * math.pi
    sc.use_merge_vertices = True
    sc.use_normal_calculate = True
    apply_mods(ob)
    ob.data.materials.append(M[m_])
    smooth(ob, math.radians(30))
    return ob


W2 = TIRE_W / 2
tire_prof = [(RIM_R + 0.004, -W2 + 0.02), (RIM_R + 0.03, -W2 + 0.006), (TIRE_R - 0.07, -W2), (TIRE_R - 0.03, -W2 + 0.012),
             (TIRE_R - 0.006, -W2 + 0.04), (TIRE_R, -W2 + 0.05), (TIRE_R, -0.045), (TIRE_R - 0.008, -0.04), (TIRE_R - 0.008, -0.03),
             (TIRE_R, -0.025), (TIRE_R, 0.0 - 0.004), (TIRE_R - 0.008, -0.002), (TIRE_R - 0.008, 0.006), (TIRE_R, 0.008),
             (TIRE_R, 0.035), (TIRE_R - 0.008, 0.038), (TIRE_R - 0.008, 0.048), (TIRE_R, 0.05), (TIRE_R, W2 - 0.05),
             (TIRE_R - 0.006, W2 - 0.04), (TIRE_R - 0.03, W2 - 0.012), (TIRE_R - 0.07, W2), (RIM_R + 0.03, W2 - 0.006),
             (RIM_R + 0.004, W2 - 0.02)]
rim_prof = [(RIM_R + 0.016, -0.075), (RIM_R + 0.016, -0.068), (RIM_R - 0.004, -0.066), (RIM_R - 0.006, -0.03),
            (RIM_R - 0.03, -0.02), (RIM_R - 0.03, 0.03), (RIM_R - 0.006, 0.04), (RIM_R - 0.004, 0.066),
            (RIM_R + 0.016, 0.068), (RIM_R + 0.016, 0.075), (RIM_R - 0.01, 0.073), (RIM_R - 0.012, 0.045),
            (0.13, 0.04), (0.09, 0.05), (0.05, 0.05), (0.05, 0.035), (0.09, 0.035), (0.13, 0.025),
            (RIM_R - 0.04, 0.022), (RIM_R - 0.012, -0.06), (RIM_R + 0.0, -0.072)]
for k, (x, y, z) in WHEELS.items():
    s = 1 if y > 0 else -1
    for name, prof, m_ in ((f"WHL_{k}_tire", tire_prof, "rubber"), (f"WHL_{k}_rim", rim_prof, "steel")):
        ob = revolve(name, prof if s > 0 else [(r, -yy) for r, yy in prof], m_)
        ob.location = (x, y, z)
    face = y + s * 0.052
    for i in range(4):
        a = math.radians(45 + 90 * i)
        cyl("lug_nut", (x + 0.05 * math.cos(a), face + s * 0.006, z + 0.05 * math.sin(a)), 0.0095, 0.018, "Y", "chrome", verts=6)
        b = math.radians(90 * i)
        v = cyl("vent_hole", (x + 0.105 * math.cos(b), face - s * 0.006, z + 0.105 * math.sin(b)), 0.018, 0.004, "Y", "gap", verts=24)
        v.scale = (1.0, 1.0, 1.0)
        v.rotation_euler = (math.pi / 2, b, 0)
        v.scale = (2.0, 1.0, 1.0)
    cyl("hub_cap", (x, face + s * 0.008, z), 0.032, 0.02, "Y", "steel", verts=32)
    cyl("valve", (x, face - s * 0.02, z + RIM_R - 0.03), 0.004, 0.03, "Y", "rubber", verts=8)

# ------------------------------------------------------------------------------ interior seen through the glass
rbox("INT_dashboard", COWL - 0.02, COWL + 0.26, -HB + 0.04, HB - 0.04, 0.70, BELT + 0.02, "interior", 0.03)
for s in (-1, 1):
    y0, y1 = sorted((s * 0.18, s * 0.66))
    rbox("INT_front_seat", 1.38, 1.86, y0, y1, 0.38, 0.52, "seat", 0.05)
    rbox("INT_front_back", 1.76, 1.88, y0 + 0.03, y1 - 0.03, 0.52, 1.07, "seat", 0.05)
    rbox("INT_headrest", 1.79, 1.87, (y0 + y1) / 2 - 0.12, (y0 + y1) / 2 + 0.12, 1.08, 1.24, "seat", 0.04)
rbox("INT_rear_bench", 2.30, 2.76, -0.54, 0.54, 0.40, 0.51, "seat", 0.05)
rbox("INT_rear_back", 2.65, 2.77, -0.54, 0.54, 0.51, 1.00, "seat", 0.05)
bpy.ops.mesh.primitive_torus_add(major_radius=0.17, minor_radius=0.016, location=(1.15, -0.37, 0.87),
                                 rotation=(0, math.radians(-56), 0))
bpy.context.active_object.name = "INT_steering_wheel"
bpy.context.active_object.data.materials.append(M["wheelbeige"])
smooth(bpy.context.active_object)

# ------------------------------------------------------------------------------ export + optional preview
for ob in bpy.context.scene.objects:
    ob.select_set(ob.type == "MESH")
bpy.ops.export_scene.gltf(filepath=OUT, export_format="GLB", use_selection=True, export_apply=True, export_yup=True)
print("exported", OUT, "mesh objects", sum(1 for o in bpy.context.scene.objects if o.type == "MESH"))

if PREVIEW:
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = 64
    sc.cycles.use_denoising = True
    sc.render.resolution_x, sc.render.resolution_y = 1600, 900
    sc.view_settings.view_transform = "AgX" if "AgX" in [v.name for v in bpy.types.ColorManagedViewSettings.bl_rna.properties["view_transform"].enum_items] else "Filmic"
    world = bpy.data.worlds.new("studio")
    sc.world = world
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.012, 0.013, 0.015, 1)
    world.node_tree.nodes["Background"].inputs["Strength"].default_value = 1.0
    bpy.ops.mesh.primitive_plane_add(size=40, location=(1.4, 0, 0))
    fl = bpy.context.active_object
    fl.data.materials.append(mat("floor", (0.06, 0.065, 0.07), rough=0.35))
    for loc, size, power, rot in (((1.4, 0, 5.5), 6, 1500, (0, 0, 0)), ((-2.5, -4.5, 2.2), 3, 900, (math.radians(70), 0, math.radians(-30))),
                                  ((5.5, 4, 2.5), 3, 700, (math.radians(70), 0, math.radians(140))), ((1.4, 6, 1.6), 5, 500, (math.radians(-75), 0, 0))):
        bpy.ops.object.light_add(type="AREA", location=loc, rotation=rot)
        lt = bpy.context.active_object.data
        lt.size, lt.energy = size, power
    bpy.ops.object.camera_add(location=(-4.6, -4.9, 1.25))
    cam = bpy.context.active_object
    cam.data.lens = 50
    sc.camera = cam
    target = bpy.data.objects.new("target", None)
    link(target)
    target.location = (1.35, 0, 0.62)
    tc = cam.constraints.new("TRACK_TO")
    tc.target, tc.track_axis, tc.up_axis = target, "TRACK_NEGATIVE_Z", "UP_Y"
    sc.render.filepath = PREVIEW
    bpy.ops.render.render(write_still=True)
    print("rendered", PREVIEW)
