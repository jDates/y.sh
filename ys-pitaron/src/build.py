import os, sys, json, shutil, html
OUT = sys.argv[1] if len(sys.argv) > 1 else "dist"
DOMAIN = os.environ.get("DOMAIN", "https://example.co.il").rstrip("/")
GA4, GTM, GSC = (os.environ.get(k, "") for k in ("GA4_ID", "GTM_ID", "GSC_VERIFY"))
NAME, PHONE, TEL, WA = "י.ש פתרון", "054-6567142", "+972546567142", "https://wa.me/972546567142"
TAG = "כל פתרונות התקשורת והטכנולוגיה במקום אחד"
E = html.escape

I = {  # אייקונים (stroke, 24x24)
 "cam": '<path d="M3 8h13v8H3zM16 11l5-3v8l-5-3"/>', "door": '<rect x="6" y="3" width="12" height="18" rx="1"/><circle cx="14.5" cy="12" r="1"/>',
 "home": '<path d="M3 11l9-8 9 8M5 10v10h14V10"/><path d="M10 20v-5h4v5"/>', "wifi": '<path d="M2 9a15 15 0 0 1 20 0M5 12.5a10 10 0 0 1 14 0M8.5 16a5 5 0 0 1 7 0"/><circle cx="12" cy="19.5" r="1"/>',
 "net": '<rect x="9" y="3" width="6" height="5"/><rect x="3" y="16" width="6" height="5"/><rect x="15" y="16" width="6" height="5"/><path d="M12 8v4M6 16v-4h12v4"/>', "music": '<path d="M9 18V5l11-2v13"/><circle cx="6.5" cy="18" r="2.5"/><circle cx="17.5" cy="16" r="2.5"/>',
 "fire": '<path d="M12 22c4 0 7-3 7-7 0-3-2-5-3-8-2 2-3 3-4 3 0-3-1-5-3-7-1 4-4 6-4 12 0 4 3 7 7 7z"/>', "tool": '<path d="M14 6a4 4 0 0 0 5 5l-9 9a2.8 2.8 0 0 1-4-4l9-9a4 4 0 0 0-1-1z"/>',
 "chat": '<path d="M4 5h16v11H9l-5 4z"/>', "alarm": '<path d="M12 3l8 3v6c0 5-4 8-8 9-4-1-8-4-8-9V6z"/><path d="M12 8v5M12 16v.5"/>', "wa": '<path d="M3 21l1.5-5A9 9 0 1 1 8 19.5z"/>'}
def ic(k, c="ic"): return f'<svg class="{c}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{I[k]}</svg>'

# שירותים עם עמוד ייעודי
SERVICES = [
 dict(slug="security-cameras", icon="cam", name="מצלמות אבטחה", title="התקנת מצלמות אבטחה לבית ולעסק", desc="התקנת מצלמות אבטחה לבית ולעסק: תכנון, התקנה והגדרת צפייה מרחוק מהנייד. קבלו הצעת מחיר בוואטסאפ.",
  h1="התקנת מצלמות אבטחה לבית ולעסק",
  intro="מערכת מצלמות טובה מתחילה בתכנון: אילו אזורים צריך לכסות, מה רמת התאורה, איפה עוברים הכבלים ואיך רוצים לצפות בתמונה. אנחנו מתאימים את המערכת למקום ולא להפך.",
  who=["בעלי בתים פרטיים ודירות","עסקים, חנויות ומשרדים","מחסנים, חניונים ושטחים פתוחים","ועדי בתים שרוצים כיסוי למקומות משותפים"],
  problems=["חוסר ידיעה מה מתרחש בנכס כשאתם לא שם","כיסוי חלקי או זוויות מות","צפייה מרחוק שלא עובדת או איטית","הקלטות שנמחקות או לא נשמרות כמו שצריך"],
  benefits=["תכנון זוויות וכיסוי לפי הנכס","התקנה מסודרת של כבלים וציוד","הגדרת צפייה מהנייד","הסבר על שימוש בהקלטות והתראות"],
  faq=[("כמה מצלמות צריך?","זה תלוי בגודל הנכס ובנקודות הכניסה. לאחר שיחה קצרה או הערכה במקום אפשר להמליץ על כיסוי מתאים."),("אפשר לצפות מהנייד?","כן, ניתן להגדיר צפייה מרחוק באפליקציה. נכוון אתכם בהגדרה."),("האם אפשר לשלב עם אזעקה?","ברוב המקרים אפשר, בהתאם לציוד הקיים. נבדוק לפי המקרה.")]),
 dict(slug="alarm-systems", icon="alarm", name="מערכות אזעקה וגילוי אש", title="התקנת מערכות אזעקה וגלאי אש", desc="התקנת מערכות אזעקה וגלאי אש לבית ולעסק. ייעוץ, התקנה והסבר שימוש. פנו אלינו בוואטסאפ.",
  h1="התקנת מערכות אזעקה וגילוי אש",
  intro="אזעקה וגילוי אש הם שכבת הגנה על הנכס ועל האנשים בו. אנחנו עוזרים לבחור, להתקין ולהסביר את המערכת, כדי שתדעו בדיוק מה קורה כשהיא מופעלת.",
  who=["בתים ודירות","עסקים ומשרדים","מחסנים ומבני מסחר"],
  problems=["נכס שנשאר ריק לאורך שעות או ימים","חשש מפני פריצה או התראת אש מאוחרת","מערכת ישנה שנותנת התראות שווא"],
  benefits=["התאמת חיישנים ונקודות כיסוי לנכס","התקנה נקייה והסבר הפעלה","אפשרות שילוב עם מצלמות ובית חכם, לפי הציוד"],
  faq=[("האם גלאי אש חייבים לעמוד בתקן?","בעסקים יש דרישות דין ורשויות. מומלץ לוודא מול הגורם הרלוונטי; אפשר להתייעץ איתנו לפני."),("מה ההבדל בין אזעקה למצלמות?","אזעקה מתריעה על אירוע, מצלמות מראות מה קרה. הן משלימות זו את זו.")]),
 dict(slug="intercom", icon="door", name="אינטרקום וכניסה לבניינים", title="התקנת אינטרקום ומערכות כניסה", desc="התקנת אינטרקום ומערכות כניסה לבתים משותפים, בניינים ועסקים. תכנון והתקנה. צרו קשר בוואטסאפ.",
  h1="התקנת אינטרקום ומערכות כניסה",
  intro="אינטרקום הוא הדלת הקדמית של הבניין. אנחנו מתקינים ומחליפים מערכות כניסה כך שהדיירים והאורחים יקבלו כניסה נוחה ובטוחה.",
  who=["בתים משותפים וועדי בתים","בניינים משרדיים","בתים פרטיים עם שער או דלת כניסה"],
  problems=["אינטרקום ישן שלא עובד או לא נשמע","צורך בפתיחת דלת מרחוק או מהנייד","כניסה לא מבוקרת לבניין"],
  benefits=["החלפה או התקנה חדשה","התאמה למספר הדירות והכבלים הקיימים","הסבר שימוש לדיירים"],
  faq=[("אפשר להחליף אינטרקום ישן בלי לשבור קירות?","לעיתים כן, תלוי בתשתית הקיימת. נבדוק לפני התקנה."),("אפשר פתיחה מהטלפון?","קיימות מערכות שתומכות בכך. נבחר לפי צרכים ותקציב.")]),
 dict(slug="smart-home", icon="home", name="בית חכם ואוטומציה", title="התקנת בית חכם ואוטומציה", desc="התקנת בית חכם ואוטומציה: תאורה, מיזוג, תריסים ושליטה מהנייד. ייעוץ והתקנה. צרו קשר בוואטסאפ.",
  h1="התקנת בית חכם ואוטומציה",
  intro="בית חכם הוא לא גאדג'טים, אלא הרגלים שהופכים לנוחים: תאורה, תריסים, מיזוג ואבטחה שעובדים יחד. מתחילים ממה שחשוב לכם ובונים משם.",
  who=["בתים חדשים בתכנון","דירות וקבלנים שרוצים שדרוג","עסקים שרוצים שליטה מרכזית"],
  problems=["מכשירים רבים עם אפליקציות נפרדות","בזבוז חשמל והפעלה ידנית","רצון לשליטה מרחוק"],
  benefits=["תכנון לפי השימוש היומיומי","חיבור בין מערכות קיימות, לפי תאימות","אפשרות הרחבה בעתיד"],
  faq=[("אפשר להתחיל בקטן?","כן. אפשר להתחיל מתחום אחד, כמו תאורה, ולהרחיב."),("צריך שינוי בתשתית?","תלוי במערכת. לעיתים אפשר לעבוד עם התשתית הקיימת.")]),
 dict(slug="wifi-network", icon="wifi", name="WiFi וקליטת אינטרנט", title="פתרונות WiFi ושיפור קליטת אינטרנט", desc="שיפור קליטת אינטרנט ופתרונות WiFi לבית ולעסק: כיסוי מלא, ציוד ורשת יציבה. צרו קשר בוואטסאפ.",
  h1="פתרונות WiFi ושיפור קליטת אינטרנט",
  intro="אינטרנט איטי בבית או בעסק לא תמיד אומר שהחבילה חלשה. לעיתים הבעיה היא מיקום הנתב, חומרי בנייה או רשת שלא תוכננה. אנחנו מאתרים את הסיבה ומתקנים אותה.",
  who=["בתים וקומות מרובות","משרדים וחנויות","עסקים עם עמדות ומדפסות מרובות"],
  problems=["אזורים בלי קליטה","ניתוקים ואיטיות בשעות עומס","רשת אחת לכל המכשירים בלי הפרדה"],
  benefits=["מיפוי כיסוי והצעת פתרון","התקנת נקודות גישה וכבילה במידת הצורך","הגדרת רשת יציבה ומאובטחת"],
  faq=[("כמה נקודות WiFi צריך?","תלוי בשטח ובקירות. בדיקה קצרה תיתן תשובה מדויקת."),("עדיף כבל או אלחוט?","כבל יציב יותר. לרוב משלבים: כבל לנקודות קבועות ו-WiFi לשאר.")]),
 dict(slug="communication", icon="net", name="תקשורת, רשתות ומחשבים", title="התקנות תקשורת, רשתות ומחשבים", desc="התקנות תקשורת ורשתות מחשבים, טכנאי מחשבים וציוד היקפי לבית ולעסק. ייעוץ והתקנה בוואטסאפ.",
  h1="התקנות תקשורת, רשתות מחשבים וציוד",
  intro="תשתית תקשורת מסודרת חוסכת תקלות. אנחנו מתקינים כבילה, ארונות תקשורת, עמדות מחשב וציוד היקפי כך שהכול ירוץ יציב ומסודר.",
  who=["משרדים ועסקים קטנים","בתים עם חדר עבודה","מי שמקים או משדרג עמדות"],
  problems=["כבלים לא מסודרים ותקלות חוזרות","עמדות מחשב שלא מוגדרות נכון","צורך בהרחבת תשתית"],
  benefits=["כבילה ותקשורת מסודרות","התקנת מחשבים וציוד היקפי","בסיס מוכן להוספת מצלמות או WiFi"],
  faq=[("אתם מתקינים גם מחשבים?","כן, התקנת מחשבים וציוד היקפי נמצאת בתחומי הפעילות שלנו."),("אפשר לשדרג תשתית קיימת?","בדרך כלל כן, אחרי בדיקה של המצב הקיים.")]),
]
# שירותים בעמוד הבית בלי עמוד ייעודי כרגע
EXTRA = [("music","מערכות שמע ומוזיקה","שמע לבית ולעסק, בשילוב עם רשת ובית חכם."),("tool","התקנות ופתרונות נוספים","פתרונות טכנולוגיים לבית ולעסק לפי צורך.")]
# אפשרויות הצ'אט (ניתן לערוך)
CHAT = [
 ("cam","מצלמות אבטחה ואזעקות","מצלמות ואזעקות: תכנון, התקנה וצפייה מהנייד.","security-cameras","מצלמות אבטחה"),
 ("door","אינטרקום ומערכות כניסה","אינטרקום ומערכות כניסה לבניינים ולעסקים.","intercom","אינטרקום"),
 ("home","בית חכם","בית חכם: תאורה, תריסים ושליטה מהנייד.","smart-home","בית חכם"),
 ("wifi","אינטרנט ופתרונות WiFi","שיפור קליטה, נקודות גישה ורשת יציבה.","wifi-network","WiFi ואינטרנט"),
 ("net","מחשבים ורשתות תקשורת","כבילה, רשתות, התקנת מחשבים וציוד היקפי.","communication","מחשבים ותקשורת"),
 ("music","מערכות שמע ומוזיקה","מערכות שמע ומוזיקה לבית ולעסק.","","מערכות שמע"),
 ("fire","מערכות גילוי אש","גלאי אש ומערכות גילוי אש.","alarm-systems","גילוי אש"),
 ("tool","התקנות ופתרונות נוספים","התקנות תקשורת ותשתיות ופתרונות טכנולוגיים נוספים.","communication","התקנות ופתרונות נוספים"),
 ("chat","אני רוצה לדבר עם נציג","","","שיחה עם נציג"),
]
FAQ = [("באילו אזורים אתם פועלים?","אנחנו עובדים בפריסה ארצית. כתבו לנו בוואטסאפ לתיאום מתי מגיעים אליכם."),("איך מקבלים הצעת מחיר?","שולחים הודעה בוואטסאפ או מתקשרים, מתארים מה צריך, ונחזור עם הצעה או תיאום ביקור."),("האם אפשר לשלב כמה שירותים יחד?","כן. מצלמות, WiFi, אינטרקום ובית חכם מתחברים לתשתית אחת, וכך חוסכים עבודה כפולה.")]
LOCAL = {"@type":"LocalBusiness","@id":DOMAIN+"/#business","name":NAME,"telephone":TEL,"url":DOMAIN+"/","slogan":TAG,"areaServed":"IL"}  # הוסיפו address/openingHours כשיהיו פרטים אמיתיים

def wa(t): return WA + "?text=" + __import__("urllib.parse").parse.quote(t)
def head(title, desc, path, extra=""):
    g = ""
    if GSC: g += f'<meta name="google-site-verification" content="{E(GSC)}">'
    if GTM: g += f"<script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':Date.now(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],j=d.createElement(s);j.async=1;j.src='https://www.googletagmanager.com/gtm.js?id='+i;f.parentNode.insertBefore(j,f)}})(window,document,'script','dataLayer','{GTM}')</script>"
    elif GA4: g += f"<script async src='https://www.googletagmanager.com/gtag/js?id={GA4}'></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','{GA4}')</script>"
    u = DOMAIN + path
    return f'''<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title><meta name="description" content="{E(desc)}"><link rel="canonical" href="{u}"><meta name="theme-color" content="#000000">
<meta property="og:type" content="website"><meta property="og:locale" content="he_IL"><meta property="og:site_name" content="{NAME}"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{u}">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="/assets/style.css">{g}{extra}</head><body>'''
def ld(*o): return '<script type="application/ld+json">' + json.dumps(list(o) if len(o) > 1 else o[0], ensure_ascii=False) + "</script>"
def header():
    nav = "".join(f'<a href="/{s["slug"]}">{s["name"]}</a>' for s in SERVICES[:4])
    return f'<a class="skip" href="#main">דלגו לתוכן</a><header class="top"><a class="logo" href="/"><b>י.ש</b> פתרון</a><nav aria-label="ראשי">{nav}<a href="/#contact">צור קשר</a></nav><a class="btn sm" href="tel:{TEL}">{PHONE}</a></header>'
def footer():
    ls = "".join(f'<a href="/{s["slug"]}">{s["name"]}</a>' for s in SERVICES)
    return f'<footer><div class="wrap fgrid"><div><b>{NAME}</b><p>{TAG}.</p><a href="tel:{TEL}">{PHONE}</a></div><nav aria-label="שירותים">{ls}</nav></div><p class="copy">© {NAME}. כל הזכויות שמורות ל Claude & ChatGPT.</p></footer><a class="fwa" href="{wa("שלום, הגעתי דרך האתר של י.ש פתרון ואשמח לפרטים.")}" target="_blank" rel="noopener" aria-label="שלחו הודעה בוואטסאפ">{ic("wa")}</a>'
def write(p, s):
    f = os.path.join(OUT, p); os.makedirs(os.path.dirname(f), exist_ok=True); open(f, "w", encoding="utf-8").write(s)
def li(a): return "".join(f"<li>{E(x)}</li>" for x in a)
def cta(topic): return f'<a class="btn" href="{wa("שלום, הגעתי דרך האתר של י.ש פתרון ואני מעוניין לקבל פרטים בנושא "+topic+".")}" target="_blank" rel="noopener">{ic("wa")} קבלת הצעת מחיר בוואטסאפ</a>'

if os.path.exists(OUT): shutil.rmtree(OUT)
shutil.copytree(os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets"), os.path.join(OUT, "assets"))
if os.path.exists(os.path.join(OUT, "assets", "projects", "videos.txt")): os.remove(os.path.join(OUT, "assets", "projects", "videos.txt"))
write("assets/config.js", "window.SITE=" + json.dumps({"wa": WA, "chat": [{"i": c[0], "l": c[1], "r": c[2], "u": ("/" + c[3]) if c[3] else "/#services", "t": c[4], "svg": I[c[0]]} for c in CHAT]}, ensure_ascii=False) + ";")

# עמוד הבית
cards = "".join(f'<a class="card" href="/{s["slug"]}">{ic(s["icon"])}<h3>{s["name"]}</h3><p>{E(s["desc"].split(":")[0] if ":" in s["desc"] else s["name"])}</p></a>' for s in SERVICES)
cards += "".join(f'<div class="card">{ic(k)}<h3>{n}</h3><p>{d}</p></div>' for k, n, d in EXTRA)
faq = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in FAQ)
home_t = "י.ש פתרון | מתח נמוך, מצלמות אבטחה, תקשורת ובית חכם"
home_d = "י.ש פתרון: התקנת מצלמות אבטחה, אינטרקום, בית חכם, WiFi, רשתות תקשורת, מחשבים ומערכות אזעקה לבית ולעסק. פנו אלינו בוואטסאפ."
sch = ld({"@context":"https://schema.org","@graph":[LOCAL,{"@type":"Organization","@id":DOMAIN+"/#org","name":NAME,"url":DOMAIN+"/","telephone":TEL},{"@type":"WebSite","@id":DOMAIN+"/#site","url":DOMAIN+"/","name":NAME,"inLanguage":"he"},
  {"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in FAQ]}]+
  [{"@type":"Service","name":s["h1"],"url":f'{DOMAIN}/{s["slug"]}',"provider":{"@id":DOMAIN+"/#business"},"areaServed":"IL"} for s in SERVICES]})
import re
from urllib.parse import quote
PDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "projects")
pj = ""
for f in sorted(os.listdir(PDIR)) if os.path.isdir(PDIR) else []:
    if not f.lower().endswith((".webp", ".jpg", ".jpeg", ".png", ".avif", ".mp4")): continue
    cap = re.sub(r"^\d+[-_ ]*", "", os.path.splitext(f)[0]).replace("-", " ").replace("_", " ").strip()
    u = "/assets/projects/" + quote(f)
    if f.lower().endswith(".mp4"): pj += f'<figure class="pj"><video src="{u}" controls preload="none" playsinline></video><span>{E(cap)}</span></figure>'
    else: pj += f'<a class="pj" href="{u}" target="_blank" rel="noopener"><img src="{u}" alt="{E(cap or "עבודה של " + NAME)}" loading="lazy" decoding="async"><span>{E(cap)}</span></a>'
YT = re.compile(r"(?:youtu\.be/|youtube\.com/(?:shorts/|embed/|live/)|[?&]v=)([A-Za-z0-9_-]{11})")
vf = os.path.join(PDIR, "videos.txt")
for ln in open(vf, encoding="utf-8").read().splitlines() if os.path.exists(vf) else []:
    ln = ln.strip()
    if not ln or ln.startswith("#"): continue
    link, _, cap = ln.partition("|"); m = YT.search(link); cap = cap.strip()
    if m: pj += f'<button type="button" class="pj yt" data-id="{m[1]}" aria-label="נגן סרטון: {E(cap or "עבודה של " + NAME)}"><img src="https://i.ytimg.com/vi/{m[1]}/hqdefault.jpg" alt="{E(cap or "סרטון עבודה של " + NAME)}" loading="lazy" decoding="async"><i aria-hidden="true"></i><span>{E(cap)}</span></button>'
projects_html = f'<div class="pw"><button type="button" class="pa pl" aria-label="גלילה שמאלה">‹</button><div class="pgrid" tabindex="0" aria-label="גלריית עבודות">{pj}</div><button type="button" class="pa pr" aria-label="גלילה ימינה">›</button></div>' if pj else '<p class="note">אנחנו מעלים לכאן תמונות עבודות והמלצות אמיתיות של לקוחות. בינתיים, כתבו לנו בצ\'אט ונשמח לספר מה אפשר לעשות במקום שלכם.</p>'
send = '<svg viewBox="0 0 24 24" width="22" height="22" fill="currentColor" aria-hidden="true"><path d="M3 20l18-8L3 4v6l12 2-12 2z" transform="scale(-1,1) translate(-24,0)"/></svg>'
write("index.html", head(home_t, home_d, "/", sch) + header() + f'''<main id="main"><section class="wa" id="chat" aria-label="צ'אט קבלת פנים"><div class="wa-h"><div class="av">י.ש</div><h1><b>{NAME}</b><small>{TAG}</small></h1></div><div class="wa-b" id="cb" role="log" aria-live="polite"></div><div class="wa-f"><input id="wi" placeholder="הקלידו הודעה" aria-label="הודעה לשליחה בוואטסאפ" maxlength="300"><button id="ws" aria-label="שליחה בוואטסאפ">{send}</button></div></section>
<section class="wrap sec" id="services"><h2>השירותים שלנו</h2><div class="grid">{cards}</div></section>
<section class="wrap sec"><h2>פרויקטים והמלצות</h2>{projects_html}</section>
<section class="wrap sec"><h2>שאלות נפוצות</h2><div class="faq">{faq}</div></section>
<section class="wrap sec cta" id="contact"><h2>צור קשר</h2><p>כתבו לנו בצ'אט בראש העמוד, או בוואטסאפ מהכפתור הצף.</p></section></main>''' + footer() + '<script src="/assets/config.js"></script><script src="/assets/app.js" defer></script></body></html>')

urls = [""]
for s in SERVICES:
    p = "/" + s["slug"]; urls.append(p)
    bc = ld({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"בית","item":DOMAIN+"/"},{"@type":"ListItem","position":2,"name":s["name"],"item":DOMAIN+p}]},
      {"@context":"https://schema.org","@type":"Service","name":s["h1"],"description":s["desc"],"url":DOMAIN+p,"provider":{"@type":"LocalBusiness","name":NAME,"telephone":TEL,"url":DOMAIN+"/"},"areaServed":"IL"},
      {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in s["faq"]]})
    rel = "".join(f'<a href="/{o["slug"]}">{o["name"]}</a>' for o in SERVICES if o is not s)
    write(s["slug"] + ".html", head(f'{s["title"]} | {NAME}', s["desc"], p, bc) + header() + f'''<main id="main" class="wrap page"><nav class="bc" aria-label="פירורי לחם"><a href="/">בית</a> / <span>{s["name"]}</span></nav><h1>{s["h1"]}</h1><p class="lead">{s["intro"]}</p>
<div class="two"><section><h2>למי זה מתאים</h2><ul>{li(s["who"])}</ul></section><section><h2>אילו בעיות אנחנו פותרים</h2><ul>{li(s["problems"])}</ul></section></div>
<section><h2>היתרונות</h2><ul>{li(s["benefits"])}</ul></section><section><h2>שאלות נפוצות</h2><div class="faq">{"".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q,a in s["faq"])}</div></section>
<section class="cta"><h2>רוצים לשמוע עוד?</h2><div class="row">{cta(s["name"])}<a class="btn ghost" href="tel:{TEL}">{PHONE}</a></div></section><section><h2>שירותים נוספים</h2><div class="rel">{rel}</div></section></main>''' + footer() + "</body></html>")
write("404.html", head("העמוד לא נמצא | " + NAME, "העמוד לא נמצא", "/404", '<meta name="robots" content="noindex">') + header() + '<main id="main" class="wrap page"><h1>העמוד לא נמצא</h1><p class="lead">חזרו לעמוד הבית ובחרו שירות.</p><a class="btn" href="/">לעמוד הבית</a></main>' + footer() + "</body></html>")
write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join(f"<url><loc>{DOMAIN}{u or '/'}</loc></url>" for u in urls) + "</urlset>")
write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n")
write(
    "google225e77db2b1a5cda.html",
    "google-site-verification: google225e77db2b1a5cda.html\n"
)
print("built", len(urls), "pages ->", OUT)
