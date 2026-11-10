// 🖼️ הסברים מאוירים (explain/<שם>.jpg) לסוגיות המסובכות. מפתח: 'ref:קטע' → שם הקובץ בלי סיומת.
// נטען בדף הלימוד (taanit.html) ובעץ (tree.html). איור חדש: מוסיפים קובץ ל־explain/ ושורה כאן.
const EXPLAIN = {
  '2a:1': '2a-mishna', '2a:2': '2a-mishna', '2a:4': '2a-gevurot',
  '2b:2': '2b-lulav', '2b:3': '2b-lulav', '2b:4': '2b-lulav',
  '2b:8': '2b-mayim', '2b:9': '2b-mayim', '2b:10': '2b-mayim', '3a:1': '2b-mayim',
  '3a:2': '3a-nisuch', '3a:3': '3a-nisuch', '3a:4': '3a-mi', '3a:5': '3a-mi',
  '3b:3': '3b-machzirin', '4a:7': '4a-ein',
  '4b:3': '4b-ramin', '4b:4': '4b-ramin', '4b:5': '4b-ramin', '4b:6': 'yosef-4b', '4b:7': 'rabba-4b',
  '4b:8': '4b-halacha', '4b:9': '4b-trei', '5a:0': '4b-trei',
  '5a:1': '5a-yoel', '5a:2': '5a-yoel', '5a:3': '5a-yoel', '5a:4': '5a-yoel',
  '6a:1': '6a-yoreh', '6a:2': '6a-yoreh', '6a:3': '6a-yoreh', '6a:4': '6a-revios',
};
const EXPLAIN_TITLE = {
  '2a-mishna': 'מאימתי מזכירין — המשנה', '2a-gevurot': 'למה ״גבורות״ גשמים', '2b-lulav': 'מלולב או מניסוך?',
  '2b-mayim': '״הרי כאן מים״: ריב״ב ור׳ עקיבא', '3a-nisuch': 'ניסוך המים כל שבעה — של מי?', '3a-mi': 'הי ר׳ יהושע? הי בן בתירה?',
  '3b-machzirin': 'מתי מחזירים את מי שטעה', '4a-ein': '״אין שואלין״ — מאן תנא?', '4b-ramin': 'ר׳ יהודה נגד ר׳ יהודה: רב חסדא ועולא',
  'yosef-4b': 'רב יוסף: ״שליח צבור ראשון״', 'rabba-4b': 'רבה: ״זמן שחיטת הפסח״', '4b-halacha': 'ר׳ יהודה או רבן גמליאל?',
  '4b-trei': 'תרי יומי בחוץ לארץ', '5a-yoel': '״יורה בניסן?!״ והנס בימי יואל', '6a-yoreh': 'יורה ומלקוש', '6a-revios': 'שלוש רביעות',
};
// כרטיס פתיחה + מסך מלא (משותף לשני הדפים)
function explainCard(ref, si) {
  const n = EXPLAIN[`${ref}:${si}`]; if (!n) return '';
  return `<button type="button" class="ex-card" onclick="openExplain('${n}')"><span class="ex-thumb"><img src="explain/${n}.jpg" loading="lazy" alt=""></span><span class="ex-t"><b>🖼️ הסבר מאויר</b><small>${EXPLAIN_TITLE[n] || ''} · כל הסוגיה צעד אחר צעד</small></span><span class="ex-go">פתח ◀</span></button>`;
}
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
