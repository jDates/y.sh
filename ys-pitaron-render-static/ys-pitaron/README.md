# י.ש פתרון – אתר תדמית + SEO

## הפעלה (פקודה אחת)
    cp .env.example .env        # ערכו דומיין ומזהי Google (אופציונלי)
    docker compose up -d --build
האתר זמין ב-http://localhost:8080

## עדכון
שנו קבצים ב-`src/` (תוכן ב-`src/build.py`, עיצוב ב-`src/assets/`) והריצו שוב `docker compose up -d --build`.

## Nginx Proxy Manager
הוסיפו Proxy Host: דומיין שלכם → Forward Hostname `ys-pitaron`, Port `80` (אותה רשת Docker, או IP של השרת ופורט 8080), הפעילו SSL/Let's Encrypt + Force SSL.
**חשוב:** הגדירו `DOMAIN=https://הדומיין-שלכם` ב-`.env` כדי ש-canonical, sitemap ו-Schema יצביעו נכון.

## Google
- Search Console: `GSC_VERIFY` = ערך content של meta האימות, ואז שלחו את `/sitemap.xml`.
- GA4 / GTM: `GA4_ID` (G-XXXX) או `GTM_ID` (GTM-XXXX).
- Business Profile: חברו ידנית; כשיהיו כתובת/שעות אמיתיות – הוסיפו ל-Schema ב-`build.py` (`LOCAL`).

## מה חסר בכוונה (לא סופק לי)
תמונות עבודה, המלצות, כתובת, שעות, אזורי שירות, שנות ניסיון. לא הומצא דבר. הוסיפו `src/assets/img/` ותמונות WebP, והחליפו את בלוק "פרויקטים" ב-`build.py`.
מילות מפתח: הצעות לבדיקה בלבד, ללא נתוני נפח חיפוש.

## ניהול עתידי
כל התוכן והגדרות הצ'אט נמצאים במבני נתונים (`SERVICES`, `CHAT` ב-`build.py`) – קל לחבר בהמשך CMS/JSON.
