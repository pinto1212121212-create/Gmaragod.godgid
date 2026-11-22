// 🖼️ הסברים מאוירים (explain/<שם>.jpg) לסוגיות המסובכות. מפתח: 'ref:קטע' → שם הקובץ בלי סיומת.
// נטען בדף הלימוד (taanit.html) ובעץ (tree.html). איור חדש: מוסיפים קובץ ל־explain/ ושורה כאן.
const EXPLAIN = {
  '2a:0': '2a-mishna', '2a:1': '2a-mishna', '2a:3': '2a-gevurot',
  '2b:1': '2b-lulav', '2b:2': '2b-lulav', '2b:3': '2b-lulav',
  '2b:7': '2b-mayim', '2b:8': '2b-mayim', '2b:9': '2b-mayim', '3a:0': '2b-mayim',
  '3a:1': '3a-nisuch', '3a:2': '3a-nisuch', '3a:3': '3a-mi', '3a:4': '3a-mi',
  '3b:2': '3b-machzirin', '4a:6': '4a-ein', '4b:0': '4a-ein', '4b:1': '4b-ramin',
  '4b:2': '4b-ramin', '4b:3': '4b-ramin', '4b:4': '4b-ramin', '4b:5': 'yosef-4b', '4b:6': 'rabba-4b',
  '4b:7': '4b-halacha', '4b:8': '4b-trei', '5a:0': '4b-trei',
  '5a:1': '5a-yoel', '5a:2': '5a-yoel', '5a:3': '5a-yoel', '5a:4': '5a-yoel',
  '6a:1': '6a-yoreh', '6a:2': '6a-yoreh', '6a:3': '6a-yoreh', '6a:4': '6a-revios',
  '6b:0': '6b-sheniya', '6b:1': '6b-sheniya', '6b:2': '6b-sheniya', '6b:3': '6b-sheniya', '6b:4': '6b-kelala', '6b:5': '6b-kelala', '6b:6': '6b-kelala', '6b:7': '6b-bracha',
  '5b:1': '5b-shmuel', '5b:2': '5b-shmuel', '5b:3': '5b-shmuel', '5b:4': '5b-yaakov',
  '10b:0': '10b-derech', '10b:1': '10b-derech', '10b:2': '10b-derech', '10b:3': '10b-derech', '10b:4': '10b-derech', '10b:5': '10b-derech', '10b:6': '10b-derech', '10b:7': '10b-derech',
  '10a:0': '10a-erets', '10a:1': '10a-erets', '10a:2': '10a-erets', '10a:3': '10a-erets', '10a:4': '10a-erets', '10a:5': '10a-erets',
  '10a:6': '10a-shoalin', '10a:7': '10a-shoalin', '10a:8': '10a-shoalin', '10a:9': '10a-shoalin', '10a:10': '10a-shoalin',
  '9b:2': '9b-mayim', '9b:3': '9b-mayim', '9b:4': '9b-mayim', '9b:5': '9b-mayim', '9b:6': '9b-mayim', '9b:7': '9b-mayim', '9b:8': '9b-mayim', '9b:9': '9b-mayim', '9b:10': '9b-mayim', '9b:11': '9b-mayim', '9b:12': '9b-mayim',
  '9a:0': '9a-maaser', '9a:1': '9a-maaser', '9a:2': '9a-maaser', '9a:3': '9a-parnasim', '9a:4': '9a-parnasim', '9a:5': '9a-parnasim', '9a:6': '9a-parnasim', '9a:7': '9a-parnasim', '9a:8': '9a-parnasim', '9a:9': '9a-parnasim',
  '8b:0': '8b-tefila', '8b:1': '8b-tefila', '8b:2': '8b-tefila', '8b:3': '8b-tefila', '8b:4': '8b-tefila', '8b:5': '8b-tefila', '8b:6': '8b-tefila', '8b:7': '8b-tefila', '8b:8': '8b-tefila', '8b:9': '8b-tefila',
  '8a:0': '8a-barzel', '8a:1': '8a-barzel', '8a:2': '8a-barzel', '8a:3': '8a-barzel', '8a:4': '8a-barzel', '8a:5': '8a-barzel', '8a:6': '8a-tefila', '8a:7': '8a-tefila', '8a:8': '8a-tefila', '8a:9': '8a-tefila',
  '7b:2': '7b-neetzarin', '7b:3': '7b-neetzarin', '7b:4': '7b-neetzarin', '7b:5': '7b-neetzarin', '7b:6': '7b-neetzarin', '7b:7': '7b-neetzarin',
  '7a:0': '7a-gadol', '7a:1': '7a-gadol', '7a:2': '7a-hagun', '7a:3': '7a-hagun', '7a:4': '7a-hagun', '7a:8': '7a-hagun', '7a:5': '7a-meshalim', '7a:6': '7a-meshalim', '7a:7': '7a-meshalim', '7a:9': '7a-meshalim', '7a:10': '7a-meshalim',
};
const EXPLAIN_TITLE = {
  '2a-mishna': 'מאימתי מזכירין — המשנה', '2a-gevurot': 'למה ״גבורות״ גשמים', '2b-lulav': 'מלולב או מניסוך?',
  '2b-mayim': '״הרי כאן מים״: ריב״ב ור׳ עקיבא', '3a-nisuch': 'ניסוך המים כל שבעה — של מי?', '3a-mi': 'הי ר׳ יהושע? הי בן בתירה?',
  '3b-machzirin': 'מתי מחזירים את מי שטעה', '4a-ein': '״אין שואלין״ — מאן תנא?', '4b-ramin': 'ר׳ יהודה נגד ר׳ יהודה: רב חסדא ועולא',
  'yosef-4b': 'רב יוסף: ״שליח צבור ראשון״', 'rabba-4b': 'רבה: ״זמן שחיטת הפסח״', '4b-halacha': 'ר׳ יהודה או רבן גמליאל?',
  '4b-trei': 'תרי יומי בחוץ לארץ', '5a-yoel': '״יורה בניסן?!״ והנס בימי יואל', '6a-yoreh': 'יורה ומלקוש', '6a-revios': 'שלוש רביעות', '6b-sheniya': 'רביעה שנייה — למה?', '6b-kelala': 'מתי גשם הוא קללה', '6b-bracha': 'הברכה על הגשם', '7a-gadol': 'כמה גדול יום הגשמים', '7b-neetzarin': 'למה הגשמים נעצרים', '8a-barzel': 'אם קהה הברזל · אם ישוך הנחש', '8a-tefila': 'תפילה, אמונה ויסורים', '8b-tefila': 'על מה מתפללים', '9a-maaser': '״עשר בשביל שתתעשר״', '9a-parnasim': 'מטר ליחיד, פרנסה לרבים', '9b-mayim': 'מאיפה העולם שותה', '10a-erets': 'ארץ ישראל, העננים והעולם', '10a-shoalin': 'מתי מבקשים גשם', '10b-derech': 'יחידים, תענית ודרך', '5b-shmuel': 'זקן שמואל בגיל 52', '5b-yaakov': 'יעקב אבינו לא מת', '7a-hagun': '״אם הגון הוא״', '7a-meshalim': 'ברזל, אש, עץ ומים',
};
// כרטיס פתיחה + מסך מלא (משותף לשני הדפים)
