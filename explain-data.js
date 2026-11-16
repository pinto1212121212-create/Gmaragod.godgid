// 🖼️ הסברים מאוירים (explain/<שם>.jpg) לסוגיות המסובכות. מפתח: 'ref:קטע' → שם הקובץ בלי סיומת.
// נטען בדף הלימוד (taanit.html) ובעץ (tree.html). איור חדש: מוסיפים קובץ ל־explain/ ושורה כאן.
const EXPLAIN = {
  '2a:1': '2a-mishna', '2a:2': '2a-mishna', '2a:4': '2a-gevurot',
  '2b:2': '2b-lulav', '2b:3': '2b-lulav', '2b:4': '2b-lulav',
  '2b:8': '2b-mayim', '2b:9': '2b-mayim', '2b:10': '2b-mayim', '3a:1': '2b-mayim',
  '3a:2': '3a-nisuch', '3a:3': '3a-nisuch', '3a:4': '3a-mi', '3a:5': '3a-mi',
  '3b:3': '3b-machzirin', '4a:7': '4a-ein', '4b:1': '4a-ein', '4b:2': '4b-ramin',
  '4b:3': '4b-ramin', '4b:4': '4b-ramin', '4b:5': '4b-ramin', '4b:6': 'yosef-4b', '4b:7': 'rabba-4b',
  '4b:8': '4b-halacha', '4b:9': '4b-trei', '5a:0': '4b-trei',
  '5a:1': '5a-yoel', '5a:2': '5a-yoel', '5a:3': '5a-yoel', '5a:4': '5a-yoel',
  '6a:1': '6a-yoreh', '6a:2': '6a-yoreh', '6a:3': '6a-yoreh', '6a:4': '6a-revios',
  '6b:1': '6b-sheniya', '6b:2': '6b-sheniya', '6b:3': '6b-sheniya', '6b:4': '6b-sheniya', '6b:5': '6b-kelala', '6b:6': '6b-kelala', '6b:7': '6b-kelala', '6b:8': '6b-bracha',
  '5b:1': '5b-shmuel', '5b:2': '5b-shmuel', '5b:3': '5b-shmuel', '5b:4': '5b-yaakov',
  '8a:1': '8a-barzel', '8a:2': '8a-barzel', '8a:3': '8a-barzel', '8a:4': '8a-barzel', '8a:5': '8a-barzel', '8a:6': '8a-barzel', '8a:7': '8a-tefila', '8a:8': '8a-tefila', '8a:9': '8a-tefila', '8a:10': '8a-tefila',
  '7b:3': '7b-neetzarin', '7b:4': '7b-neetzarin', '7b:5': '7b-neetzarin', '7b:6': '7b-neetzarin', '7b:7': '7b-neetzarin', '7b:8': '7b-neetzarin',
  '7a:1': '7a-gadol', '7a:2': '7a-gadol', '7a:3': '7a-hagun', '7a:4': '7a-hagun', '7a:5': '7a-hagun', '7a:9': '7a-hagun', '7a:6': '7a-meshalim', '7a:7': '7a-meshalim', '7a:8': '7a-meshalim', '7a:10': '7a-meshalim', '7a:11': '7a-meshalim',
};
const EXPLAIN_TITLE = {
  '2a-mishna': 'מאימתי מזכירין — המשנה', '2a-gevurot': 'למה ״גבורות״ גשמים', '2b-lulav': 'מלולב או מניסוך?',
  '2b-mayim': '״הרי כאן מים״: ריב״ב ור׳ עקיבא', '3a-nisuch': 'ניסוך המים כל שבעה — של מי?', '3a-mi': 'הי ר׳ יהושע? הי בן בתירה?',
  '3b-machzirin': 'מתי מחזירים את מי שטעה', '4a-ein': '״אין שואלין״ — מאן תנא?', '4b-ramin': 'ר׳ יהודה נגד ר׳ יהודה: רב חסדא ועולא',
  'yosef-4b': 'רב יוסף: ״שליח צבור ראשון״', 'rabba-4b': 'רבה: ״זמן שחיטת הפסח״', '4b-halacha': 'ר׳ יהודה או רבן גמליאל?',
  '4b-trei': 'תרי יומי בחוץ לארץ', '5a-yoel': '״יורה בניסן?!״ והנס בימי יואל', '6a-yoreh': 'יורה ומלקוש', '6a-revios': 'שלוש רביעות', '6b-sheniya': 'רביעה שנייה — למה?', '6b-kelala': 'מתי גשם הוא קללה', '6b-bracha': 'הברכה על הגשם', '7a-gadol': 'כמה גדול יום הגשמים', '7b-neetzarin': 'למה הגשמים נעצרים', '8a-barzel': 'אם קהה הברזל · אם ישוך הנחש', '8a-tefila': 'תפילה, אמונה ויסורים', '5b-shmuel': 'זקן שמואל בגיל 52', '5b-yaakov': 'יעקב אבינו לא מת', '7a-hagun': '״אם הגון הוא״', '7a-meshalim': 'ברזל, אש, עץ ומים',
};
// כרטיס פתיחה + מסך מלא (משותף לשני הדפים)
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
