// 🖼️ ההסברים המאוירים — הקוד (משותף לדף הלימוד ולעץ). הנתונים (EXPLAIN, EXPLAIN_TITLE) נטענים לפי דף (loader.js).
function explainCardN(n) {
  return `<button type="button" class="ex-card" onclick="openExplain('${n}')"><span class="ex-thumb"><img src="explain/${n}.jpg" loading="lazy" alt=""></span><span class="ex-t"><b>🖼️ הסבר מאויר</b><small>${EXPLAIN_TITLE[n] || ''} · כל הסוגיה צעד אחר צעד</small></span><span class="ex-go">פתח ◀</span></button>`;
}
function explainCard(ref, si) { const n = EXPLAIN[`${ref}:${si}`]; return n ? explainCardN(n) : ''; }
// בעץ: האיור של הקטע של הצומת, ואחריו האיורים של שאר הקטעים באותה סוגיה (אותו שורש)
function explainNames(ref, node) {
  const roots = (typeof TREE !== 'undefined' && TREE[ref]) ? TREE[ref].roots : [];
  const has = x => x === node || (x.k || []).some(has);
  const root = roots.find(has), ss = [node.s];
  if (root) { const w = x => { ss.push(x.s); (x.k || []).forEach(w); }; w(root); }
  return [...new Set(ss.map(s => EXPLAIN[`${ref}:${s}`]).filter(Boolean))];
}
function explainTree(ref, node) { return explainNames(ref, node).map(explainCardN).join(''); }
function openExplain(n) {
  if (!/^[\w-]+$/.test(n)) return;
  let v = document.getElementById('exView');
  if (!v) {
    v = document.createElement('div'); v.id = 'exView'; v.className = 'ex-view';
    v.innerHTML = '<div class="ex-bar"><button type="button" class="ex-x" aria-label="סגור">✕</button><span class="ex-h"></span><button type="button" class="ex-z" aria-label="הגדלה">🔍</button></div><div class="ex-scroll"><img alt="הסבר מאויר"></div>';
    document.body.appendChild(v);
    v.querySelector('.ex-x').onclick = closeExplain;
    v.querySelector('.ex-z').onclick = () => exZoom(EXZ.z < 1.9 ? 2 : EXZ.z < 2.9 ? 3 : 1);
    exPinchBind(v.querySelector('.ex-scroll'));
    document.addEventListener('keydown', e => { if (e.key === 'Escape' && v.classList.contains('on')) closeExplain(); });
  }
  v.querySelector('.ex-h').textContent = '🖼️ ' + (EXPLAIN_TITLE[n] || 'הסבר מאויר');
  v.querySelector('img').src = `explain/${n}.jpg`;
  exZoom(1); v.querySelector('.ex-scroll').scrollTop = 0;
  v.classList.add('on'); document.documentElement.classList.add('ex-open');
}
function closeExplain() { const v = document.getElementById('exView'); if (v) v.classList.remove('on'); document.documentElement.classList.remove('ex-open'); }

// 🔍 הגדלה בצביטה (שתי אצבעות), הקשה כפולה, או הכפתור 🔍. רק התמונה גדלה, והנקודה שבין האצבעות נשארת במקומה.
const EXZ = { z: 1 };
function exZoom(z, cx, cy) {
  const v = document.getElementById('exView'); if (!v) return;
  const sc = v.querySelector('.ex-scroll'), img = sc.querySelector('img');
  z = Math.max(1, Math.min(4, z));
  const r = sc.getBoundingClientRect();
  if (cx == null) { cx = r.left + r.width / 2; cy = r.top + r.height / 2; }
  const px = sc.scrollLeft + (cx - r.left), py = sc.scrollTop + (cy - r.top), k = z / EXZ.z;
  EXZ.z = z; img.style.width = (z * 100) + '%'; img.style.maxWidth = z > 1 ? 'none' : '';
  sc.scrollLeft = px * k - (cx - r.left); sc.scrollTop = py * k - (cy - r.top);
  v.classList.toggle('zoom', z > 1);
  const b = v.querySelector('.ex-z'); if (b) b.textContent = z > 1 ? Math.round(z * 10) / 10 + '×' : '🔍';
}
function exPinchBind(sc) {
  let d0 = 0, z0 = 1, lastTap = 0;
  const dist = t => Math.hypot(t[0].clientX - t[1].clientX, t[0].clientY - t[1].clientY);
  sc.addEventListener('touchstart', e => {
    if (e.touches.length === 2) { d0 = dist(e.touches); z0 = EXZ.z; e.preventDefault(); }
    else if (e.touches.length === 1) {
      const now = Date.now(), t = e.touches[0];
      if (now - lastTap < 300) { exZoom(EXZ.z > 1 ? 1 : 2.5, t.clientX, t.clientY); e.preventDefault(); lastTap = 0; } else lastTap = now;
    }
  }, { passive: false });
  sc.addEventListener('touchmove', e => {
    if (e.touches.length === 2 && d0) {
      e.preventDefault();
      const t = e.touches; exZoom(z0 * dist(t) / d0, (t[0].clientX + t[1].clientX) / 2, (t[0].clientY + t[1].clientY) / 2);
    }
  }, { passive: false });
  sc.addEventListener('touchend', e => { if (e.touches.length < 2) d0 = 0; });
  // מחשב: Ctrl + גלגלת (וגם צביטה במשטח מגע)
  sc.addEventListener('wheel', e => { if (!e.ctrlKey) return; e.preventDefault(); exZoom(EXZ.z * (e.deltaY < 0 ? 1.15 : 1 / 1.15), e.clientX, e.clientY); }, { passive: false });
}
