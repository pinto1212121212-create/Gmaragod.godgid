// בדיקת האתר בדפדפן ברוחב טלפון. הרצה מתיקיית הריפו:
//   node .claude/tools/check.js            (צילומי מסך נשמרים ב־.claude/out/)
// בודק: שגיאות JS, תמונות שלא נטענו, גלילה אופקית, שלכל שלב עם מיקום יש הדגשה בצילום,
// ושכל הדפים (בית, תענית, עץ, זבחים) נטענים.
const { chromium } = require('playwright');
const http = require('http'), fs = require('fs'), path = require('path');
const root = process.cwd(), out = path.join(root, '.claude', 'out');
fs.mkdirSync(out, { recursive: true });
const srv = http.createServer((q, r) => {
  let f = path.join(root, decodeURIComponent(q.url.split('?')[0].split('#')[0])); if (f.endsWith('/')) f += 'index.html';
  fs.readFile(f, (e, d) => { if (e) { r.writeHead(404); r.end(); return; }
    r.writeHead(200, { 'Content-Type': f.endsWith('.html') ? 'text/html; charset=utf-8' : f.endsWith('.js') ? 'text/javascript' : 'image/jpeg' }); r.end(d); });
}).listen(8799);
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 412, height: 915 } });
  const errs = []; p.on('pageerror', e => errs.push(p.url().split('/').pop() + ': ' + e.message)); p.on('requestfailed', r => errs.push('לא נטען: ' + r.url()));
  const U = 'http://localhost:8799/';
  for (const f of ['', 'taanit.html', 'tree.html', 'zevachim.html']) {
    await p.goto(U + f); await p.waitForTimeout(800);
    await p.evaluate(() => { try { localStorage.setItem('gemara:help', '1'); } catch (e) {} });
    const w = await p.evaluate(() => document.documentElement.scrollWidth); if (w > 412) errs.push(`גלילה אופקית ב־${f || 'index'}: ${w}px`);
    await p.screenshot({ path: path.join(out, `page-${f || 'index'}.png`) });
  }
  await p.goto(U + 'taanit.html'); await p.waitForTimeout(700);
  let ok = 0, miss = [];
  const refs = await p.evaluate(() => Object.keys(BEAT_LOC));
  for (const r of refs) {
    const n = await p.evaluate(r => amudim[r].scenes.length, r);
    for (let si = 0; si < n; si++) {
      const nb = await p.evaluate(([r, si]) => { goToRef(r); state.sceneIdx = si; renderScenes(); return (amudim[r].scenes[si].beats || []).length; }, [r, si]);
      for (let bi = 0; bi < nb; bi++) {
        if (!await p.evaluate(([r, si, bi]) => !!beatLoc(r, si, bi), [r, si, bi])) continue;
        await p.evaluate(bi => { focusBeat = bi; showLoc(); }, bi); await p.waitForTimeout(60);
        (await p.evaluate(() => document.querySelectorAll('.src-hl').length)) ? ok++ : miss.push(`${r}:${si}:${bi}`);
      }
    }
  }
  console.log(`שלבים עם הדגשה: ${ok}. בלי הדגשה: ${miss.length ? miss.join(' ') : 'אין'}`);
  // עץ הסוגיה: לכל צומת הדגשה משלו. שני צמתים עם אותן מילים = שלב שמערבב שני דברים → לפצל (split_beat.py)
  await p.goto(U + 'tree.html'); await p.waitForTimeout(700);
  const dup = await p.evaluate(() => { const bad = [];
    for (const ref in TREE) { let seq = 0; const seen = {}; const flat = [];
      const w = n => { n.seq = ++seq; flat.push(n); (n.k || []).forEach(w); }; TREE[ref].roots.forEach(w);
      if (TREE_CX[ref] && TREE_CX[ref].length !== flat.length) bad.push(`${ref}: TREE_CX ${TREE_CX[ref].length} ≠ ${flat.length} צמתים`);
      for (const n of flat) { const sp = beatOf(ref, n); if (!sp) continue; const k = `${n.s}:${sp}`;
        if (seen[k]) bad.push(`${ref}: צמתים ${seen[k]} ו־${n.seq} עם אותה הדגשה`); else seen[k] = n.seq; } }
    return bad; });
  console.log(`עץ: ${dup.length ? dup.join(' | ') : 'לכל צומת הדגשה משלו ✓'}`);
  // 👥 people-data.js: כל מספר צומת קיים, כל on מצביע על משפט שקיים, ולכל קושיה יש מצב
  const pbad = await p.evaluate(() => { const bad = [];
    for (const ref in (typeof PEOPLE !== 'undefined' ? PEOPLE : {})) {
      const cnt = r => { let c = 0; const w = n => { c++; (n.k || []).forEach(w); }; (TREE[r] ? TREE[r].roots : []).forEach(w); return c; };
      const okSeq = x => { const [r, q] = typeof x === 'number' ? [ref, x] : String(x).split(':'); return TREE[r] && +q >= 1 && +q <= cnt(r); };
      for (const pp of PEOPLE[ref]) {
        if (!pp.id || !pp.n || !pp.c || !pp.holds) bad.push(`${ref}/${pp.id || pp.n}: חסר id/n/c/holds`);
        try { if (pp.al) new RegExp(pp.al); } catch (e) { bad.push(`${ref}/${pp.id}: al לא תקין`); }
        (pp.says || []).forEach(s => { if (!okSeq(s[0])) bad.push(`${ref}/${pp.id}: says ${s[0]} לא קיים`); });
        (pp.vs || []).forEach(v => { if (!okSeq(v.k)) bad.push(`${ref}/${pp.id}: קושיה ${v.k} לא קיימת`);
          (v.on || []).forEach(o => { if (!(pp.says || [])[o - 1]) bad.push(`${ref}/${pp.id}: on ${o} אין משפט כזה`); });
          [].concat(v.fix == null ? [] : v.fix).forEach(x => { if (!okSeq(x)) bad.push(`${ref}/${pp.id}: fix ${x} לא קיים`); });
          if (!['ok', 'fell', 'info', 'open'].includes(v.st)) bad.push(`${ref}/${pp.id}: קושיה ${v.k} בלי st`); });
      } }
    return bad; });
  console.log(`אנשים: ${pbad.length ? pbad.join(' | ') : 'הכל תקין ✓'}`);
  errs.push(...pbad);
  errs.push(...dup);
  console.log(errs.length ? 'שגיאות:\n' + errs.join('\n') : 'אין שגיאות ✓');
  await b.close(); srv.close();
})();
