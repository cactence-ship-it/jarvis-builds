// Re-proportion a car mesh along its length (x) and level its pitch, without touching texture/UVs.
// usage: node reprop.mjs IN OUT pitch_deg pivot_x  xs0,xs1,xs2,xs3  xt0,xt1,xt2,xt3
// x is remapped piecewise-linearly so the mesh's front end / front wheel / rear wheel / rear end
// (xs, after the pitch fix) land on the target fractions xt.
// Optional env SHEAR="a,b": removes a plan-view shear, z -= a + b*x (x after remapping), so the
// centre line of a mesh generated from oblique photos becomes straight.
import { NodeIO } from '@gltf-transform/core';
import { ALL_EXTENSIONS } from '@gltf-transform/extensions';
const [,, IN, OUT, pitch, pivot, xsS, xtS] = process.argv;
const xs = xsS.split(',').map(Number), xt = xtS.split(',').map(Number);
const a = Number(pitch) * Math.PI / 180, c = Math.cos(a), s = Math.sin(a), px = Number(pivot);
const n = xs.length - 1;
const [sa, sb] = (process.env.SHEAR || '0,0').split(',').map(Number);
const map = x => { // xs ascending, any number of knots; linear extrapolation outside
  for (let i = 0; i < n; i++) if (x <= xs[i + 1] || i === n - 1) return xt[i] + (x - xs[i]) * (xt[i + 1] - xt[i]) / (xs[i + 1] - xs[i]);
};
const io = new NodeIO().registerExtensions(ALL_EXTENSIONS);
const doc = await io.read(IN);
const done = new Set();
for (const mesh of doc.getRoot().listMeshes()) for (const prim of mesh.listPrimitives()) {
  const pos = prim.getAttribute('POSITION'); if (done.has(pos)) continue; done.add(pos);
  const v = [0, 0, 0];
  for (let i = 0; i < pos.getCount(); i++) {
    pos.getElement(i, v);
    const x = (v[0] - px) * c - v[1] * s + px, y = (v[0] - px) * s + v[1] * c;  // rotate about z (pitch)
    const xm = map(x);
    pos.setElement(i, [xm, y, v[2] - (sa + sb * xm)]);
  }
}
await io.write(OUT, doc);
console.log('ok');
