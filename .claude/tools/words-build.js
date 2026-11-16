// 🔤 בניית מאגר לימוד המילים (רץ ב־build-pack.js, לא בדפדפן). קלט: TX, REFS, clean. פלט: ALL.
// --- בניית המאגר ---
const W = new Map();
function add(w, m, type, key) {
  w = String(w).trim(); m = String(m).trim(); if (!w || !m) return;
  const cw = clean(w), cm = clean(m);
  const core = clean(m.replace(/\([^)]*\)/g, ' ').replace(/[־–—-]/g, ' ')), strip = t => t.replace(/^[והבלמשד](?=\S{2})/, '');
  const same = core === cw || strip(core) === cw || core === strip(cw) || strip(core) === strip(cw) || core.split(' / ').includes(cw);
  if (cw.length < 2 || !cm || same || /\((אמורא|שם|תנא|אמוראים)/.test(m) || /^[\d\s]+$/.test(cw)) return;
  let x = W.get(cw);
  if (!x) { x = { id: cw, w, type, ms: {}, refs: new Set(), keys: [] }; W.set(cw, x); }
  x.ms[m] = (x.ms[m] || 0) + 1;
  if (key) { const r = key.split(':')[0]; x.refs.add(r); if (x.keys.length < 3 && !x.keys.includes(key)) x.keys.push(key); }
  if (type === 'term') x.type = 'term';
}
for (const [key, v] of Object.entries(TX.WBW || {})) for (const p of v.split('|')) {
  const i = p.indexOf('='); if (i < 0) continue;
  const a = p.slice(0, i).trim(), h = p.slice(i + 1).trim(), n = a.split(/\s+/).length;
  if (n <= 4) add(a, h, n > 1 ? 'ph' : 'w', key);
}
// אינדקס מילה → השלב הראשון שבו היא מופיעה (נבנה פעם אחת; קודם חיפשנו בכל WBW לכל מילה במילון — איטי מאוד בטלפון)
const FIRST = new Map();
for (const k of Object.keys(TX.WBW || {})) for (const t of clean(TX.WBW[k].split('|').map(p => p.split('=')[0]).join(' ')).split(' ')) if (t && !FIRST.has(t)) FIRST.set(t, k);
for (const [w, m] of Object.entries(TX.WDICT || {})) {
  const cw = clean(w); if (W.has(cw)) continue;
  add(w, m, 'w', FIRST.get(cw));
}
for (const [t, m] of (TX.KEY_TERMS || [])) { const cw = clean(t); const old = W.get(cw); add(t, m, 'term', old && old.keys[0]); const x = W.get(cw); if (x) { x.type = 'term'; x.ms = { [m]: 99 }; } }
const ALL = [...W.values()].map(x => { x.m = Object.entries(x.ms).sort((a, b) => b[1] - a[1])[0][0]; x.refs = REFS.filter(r => x.refs.has(r)); return x; })
  .filter(x => x.refs.length || x.type === 'term');

