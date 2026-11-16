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
    v.querySelector('.ex-z').onclick = () => v.classList.toggle('zoom');
    document.addEventListener('keydown', e => { if (e.key === 'Escape' && v.classList.contains('on')) closeExplain(); });
  }
  v.querySelector('.ex-h').textContent = '🖼️ ' + (EXPLAIN_TITLE[n] || 'הסבר מאויר');
  v.querySelector('img').src = `explain/${n}.jpg`;
  v.classList.remove('zoom'); v.querySelector('.ex-scroll').scrollTop = 0;
  v.classList.add('on'); document.documentElement.classList.add('ex-open');
}
function closeExplain() { const v = document.getElementById('exView'); if (v) v.classList.remove('on'); document.documentElement.classList.remove('ex-open'); }
