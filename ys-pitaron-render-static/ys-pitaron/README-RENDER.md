# י.ש פתרון — גרסה לפריסה כאתר סטטי ב-Render

הפרויקט מוכן לפריסה כ-**Render Static Site**. אין צורך בשרת Docker פעיל, במסד נתונים או בניהול תעודות SSL.
Render מגיש את האתר ב-HTTPS ומנהל את תעודת ה-SSL אוטומטית.

## פריסה ראשונה

1. חלצו את קובץ ה-ZIP.
2. העלו את כל התיקייה `ys-pitaron` למאגר חדש ב-GitHub (כולל `render.yaml`, `src/` ו-`README.md`).
3. היכנסו ל-https://dashboard.render.com/ ובחרו **New → Blueprint**.
4. חברו את מאגר GitHub שבו נמצא הפרויקט.
5. Render יזהה את `render.yaml`. אשרו יצירת Static Site בשם `ys-pitaron-site`.
6. בסיום הפריסה תקבלו כתובת בסגנון `https://ys-pitaron-site.onrender.com`.

## הגדרת כתובת האתר עבור SEO

לאחר ש-Render יצר את האתר:
1. העתיקו את כתובת `onrender.com` המדויקת שהוקצתה לכם.
2. פתחו את השירות ב-Render → **Environment** (או Build & Deploy → Environment, לפי הממשק).
3. הוסיפו משתנה Build Environment בשם `DOMAIN` עם הערך של כתובת האתר, למשל `https://ys-pitaron-site.onrender.com` — החליפו בכתובת האמיתית שלכם.
4. שמרו והפעילו **Manual Deploy → Deploy latest commit**.

המשתנה `DOMAIN` משמש לכתובות canonical, למפת האתר `sitemap.xml`, ל-robots.txt ולנתוני Schema. אל תשאירו את כתובת הדוגמה אם קיבלתם כתובת אחרת.

## הוספת תמונות לפרויקטים

הוסיפו תמונות לתיקייה:
`src/assets/projects/`

שמות מומלצים: `01-camera-installation.webp`, `02-wifi-network.webp` וכדומה.
האתר בונה את גלריית הפרויקטים אוטומטית מתמונות מסוג JPG/JPEG/PNG/WEBP/AVIF וגם מקובצי MP4 שנמצאים בתיקייה. שם הקובץ הופך לכיתוב בתצוגה (מספרים ומקפים בתחילת השם מוסרים).

כדי להוסיף סרטוני YouTube, ערכו את `src/assets/projects/videos.txt` והוסיפו שורה לכל סרטון בפורמט:
`https://www.youtube.com/watch?v=VIDEO_ID|כיתוב לסרטון`

## הוספת קישורים

אפשר לערוך את קובצי המקור שבתיקיית `src/`. קישורים ושירותים קיימים נוצרים בקובץ `src/build.py`.
לאחר כל שינוי העלו commit ל-GitHub; Render יבנה ויפרסם את האתר מחדש.

## פרטי קשר

מספר הטלפון וקישור WhatsApp מוגדרים כרגע בקובץ `src/build.py`:
`054-6567142` ו-`+972546567142`.
אם צריך לשנות אותם, עדכנו את הערכים בקובץ לפני הפריסה.

## בדיקה מקומית (אופציונלי)

נדרשת Python 3:
```bash
python src/build.py dist
```
האתר שנוצר נמצא בתיקייה `dist/`. אפשר לפתוח `dist/index.html` או להגיש את התיקייה עם שרת סטטי מקומי.

## הערות

- אין במסלול הזה צורך ב-Docker או ב-Docker Compose. שמרנו את קובצי Docker המקוריים בארכיון למקרה שתרצו לחזור לאירוח עצמי.
- Render Static Site לא נכנס למצב שינה כמו שירות Web Service חינמי.
- שם האתר ב-Render עשוי להיות תפוס. אם Render מציע שם אחר, השתמשו בכתובת שהוקצתה בפועל גם בערך `DOMAIN`.
- כתובת `onrender.com` חינמית. דומיין פרטי הוא אופציונלי בלבד.
