// 📲 Service worker: האתר נפתח גם בלי אינטרנט, ונטען מהר.
// קוד ונתונים (html/js/css): קודם מהרשת (תמיד הגרסה החדשה), ואם אין רשת — מהשמור.
// תמונות (צילומי דף, איורים, אייקונים): קודם מהשמור, כי הן כמעט לא משתנות; מתעדכנות ברקע.
// שינוי גדול במבנה, או שינוי של תמונה קיימת (חיתוך מחדש, שינוי מספור קטעים)? מעלים את VERSION — אחרת הטלפון יציג את התמונה הישנה מהשמור.
const VERSION = 'v23';
const CORE = ['./', 'index.html', 'taanit.html', 'tree.html', 'words.html', 'theme.css', 'vip.css', 'prefs.js', 'loader.js', 'explain.js',
  'data/common.js', 'data/taanit/index.js', 'data/taanit/words.js', 'manifest.webmanifest', 'icons/icon-192.png'];
// רשימת הדפים הבנויים — מהמפה של המסכת (MAS), כך שאין צורך לעדכן כאן כשמוסיפים דף
let PAGES = []; try { importScripts('data/taanit/index.js'); PAGES = MAS.refs; } catch (e) {}
self.addEventListener('install', e => {
  e.waitUntil(caches.open('core-' + VERSION).then(c => c.addAll(CORE)).then(() => self.skipWaiting()));
  caches.open('img-' + VERSION).then(c => Promise.all(PAGES.map(p => c.add('taanit-img/' + p + '-full.jpg').catch(() => {}))));
  // התוכן של כל דף (taanit-data/ + data/<מסכת>/) — נשמר מראש ברקע, כדי שכל הדפים ייפתחו גם בלי אינטרנט
  caches.open('core-' + VERSION).then(c => Promise.all(PAGES.flatMap(p => ['taanit-data/' + p + '.js', 'data/taanit/' + p + '.js']).map(u => c.add(u).catch(() => {}))));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => !k.endsWith(VERSION)).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});
self.addEventListener('fetch', e => {
  const r = e.request, u = new URL(r.url);
  if (r.method !== 'GET' || u.origin !== location.origin || r.cache === 'no-store') return;
  if (/\.(jpe?g|png|webp)$/i.test(u.pathname)) {
    e.respondWith(caches.open('img-' + VERSION).then(async c => {
      const hit = await c.match(r);
      const hit2 = hit || await c.match(r, { ignoreSearch: true });   // ניסיון חוזר עם ?r=
      const net = fetch(r).then(res => { if (res.ok) c.put(new Request(u.origin + u.pathname), res.clone()); return res; })
        .catch(() => hit2 || caches.match(r, { ignoreSearch: true }).then(m => m || Response.error()));
      return hit2 || net;
    }));
    return;
  }
  e.respondWith(fetch(r).then(res => {
    if (res.ok) { const cp = res.clone(); caches.open('core-' + VERSION).then(c => c.put(r, cp)); }
    return res;
  }).catch(() => caches.match(r, { ignoreSearch: true }).then(m => m || caches.match('index.html'))));
});
