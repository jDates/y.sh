(()=>{const S=window.SITE,cb=document.getElementById("cb");if(!cb)return;
const RM=matchMedia("(prefers-reduced-motion:reduce)").matches,sleep=t=>new Promise(r=>setTimeout(r,RM?0:t));
const el=(t,c,h)=>{const e=document.createElement(t);if(c)e.className=c;if(h!=null)e.innerHTML=h;return e};
const scroll=()=>{cb.scrollTop=cb.scrollHeight},esc=s=>s.replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const now=()=>new Date().toLocaleTimeString("he-IL",{hour:"2-digit",minute:"2-digit"});
const KEY="ysChat1";let H=[];try{H=JSON.parse(sessionStorage.getItem(KEY)||"[]")}catch(_){}
const save=e=>{H.push(e);try{sessionStorage.setItem(KEY,JSON.stringify(H))}catch(_){}};
let Q=Promise.resolve();const run=f=>(Q=Q.then(f).catch(()=>{}));
/* בניית בועות */
const mkBot=(t,tm)=>{const m=el("div","msg bot");m.textContent=t;m.append(el("time","",tm));cb.append(m);return m};
const mkMe=(t,tm)=>cb.append(el("div","msg me",esc(t)+"<time>"+tm+' <span class="tk">✓✓</span></time>'));
async function bot(text){const m=el("div","msg bot typing","<i></i><i></i><i></i>");cb.append(m);scroll();await sleep(1400);
 m.className="msg bot";m.textContent="";const n=document.createTextNode("");m.append(n);
 if(RM)n.data=text;else for(const ch of text){n.data+=ch;scroll();await sleep(ch==="\n"?450:42)}
 const tm=now();m.append(el("time","",tm));save({k:"b",t:text,tm});scroll()}
const me=t=>{const tm=now();mkMe(t,tm);save({k:"m",t,tm});scroll()};
const wa=topic=>S.wa+"?text="+encodeURIComponent("שלום, הגעתי דרך האתר של י.ש פתרון ואני מעוניין לקבל פרטים בנושא "+topic+".");
function mkOpts(instant){const g=el("div","opts");S.chat.forEach((c,i)=>{const b=el("button","opt"+(i==8?" wide":""),'<svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'+c.svg+"</svg><span>"+c.l+"</span>");
 if(instant||RM){b.style.animation="none";b.style.opacity=1}else b.style.animationDelay=i*140+"ms";b.onclick=()=>run(()=>pick(c,1));g.append(b)});cb.append(g)}
const opts=()=>{mkOpts();save({k:"o"});scroll()};
const mkActs=h=>{const a=el("div","acts",h);cb.append(a)};
async function pick(c,showMe){if(showMe)me(c.l);await bot(c.r||"בשמחה! כתבו לנו בוואטסאפ או התקשרו, ונחזור אליכם.");
 let h=c.u&&c.r?'<a class="btn ghost" href="'+c.u+'">למידע נוסף</a>':"";
 h+='<a class="btn" target="_blank" rel="noopener" href="'+wa(c.t)+'">קבלת הצעת מחיר בוואטסאפ</a>';mkActs(h);save({k:"a",h});scroll()}
/* הבנת טקסט חופשי – התאמת מילות מפתח (ללא AI חיצוני) */
const KW=[["מצלמ","אבטח","=cctv","פריצ","גנב","אזעק","מעקב","=אזעקה"],["אינטרקום","פעמון","=כניסה","דלת","בניין","ועד","שער","=אינטרקום"],["חכם","אוטומצי","תריס","תאורה","מיזוג","=בית"],["wifi","וויפי","וייפי","אינטרנט","קליט","נתב","ראוטר","סיב","=רשת"],["מחשב","תקשורת","כבל","כבלים","מדפסת","לפטופ","רשתות","טכנאי"],["שמע","מוזיקה","רמקול","סאונד","מגבר"],["=אש","עשן","גלאי","כיבוי","שריפ"],["התקנ","תשתית","תיקון","שדרוג"],["נציג","טלפון","להתקשר","מחיר","הצעה","עלות","דבר","=איש"]];
const HI=["שלום","היי","=הי","אהלן","בוקר","ערב","=hello","=hi","מה נשמע"];
const norm=s=>s.toLowerCase().replace(/[\u0591-\u05C7]/g,"").replace(/[^\u0590-\u05ffa-z0-9\s]/g," ").split(/\s+/).filter(Boolean);
const hit=(w,k)=>k[0]==="="?(w===k.slice(1)||w.slice(1)===k.slice(1)):(w.startsWith(k)||(w.length>3&&w.slice(1).startsWith(k)));
function understand(t){const W=norm(t);let best=-1,sc=0;KW.forEach((L,i)=>{const n=W.filter(w=>L.some(k=>hit(w,k))).length;if(n>sc){sc=n;best=i}});
 if(best>=0)return{c:S.chat[best]};if(W.some(w=>HI.some(k=>hit(w,k))||t.includes("מה נשמע")))return{hi:1};return{}}
function send(){const v=wi.value.trim();if(!v)return;wi.value="";run(async()=>{me(v);const r=understand(v);
 if(r.c)return pick(r.c);
 await bot(r.hi?"שלום! איך אפשר לעזור?":"לא הצלחתי להבין את ההודעה. נא לבחור מהאפשרויות הקיימות:");opts()})}
const wi=document.getElementById("wi");document.getElementById("ws").onclick=send;wi.onkeydown=e=>{if(e.key==="Enter")send()};
/* שחזור שיחה בין עמודים / התחלה חדשה */
if(H.some(e=>e.k==="o")){for(const e of H){if(e.k==="b")mkBot(e.t,e.tm);else if(e.k==="m")mkMe(e.t,e.tm);else if(e.k==="o")mkOpts(1);else if(e.k==="a")mkActs(e.h)}scroll()}
else{H=[];try{sessionStorage.removeItem(KEY)}catch(_){}
 run(async()=>{await sleep(700);await bot("שלום, ברוכים הבאים לי.ש פתרון!");await bot("שמי יוסף שורקי 😊");await bot("אשמח לתת לך שירות בתחומי התקשורת, מתח נמוך, בית חכם, אינטרנט, מחשבים, WiFi, התקנות ועוד.");await bot("מה בדיוק מעניין אותך?");opts()})}
})();
document.addEventListener("click",e=>{const b=e.target.closest&&e.target.closest(".yt");if(!b)return;
 const f=document.createElement("iframe");f.src="https://www.youtube-nocookie.com/embed/"+b.dataset.id+"?autoplay=1&rel=0&playsinline=1";f.allow="autoplay; encrypted-media; picture-in-picture; fullscreen";f.allowFullscreen=true;f.title=b.getAttribute("aria-label");f.style.cssText="width:100%;height:100%;border:0";
 const w=document.createElement("div");w.className="pj";w.append(f);b.replaceWith(w)});
document.addEventListener("click",e=>{const a=e.target.closest&&e.target.closest(".pa");if(!a)return;const g=a.parentNode.querySelector(".pgrid");g.scrollBy({left:(a.classList.contains("pl")?-1:1)*g.clientWidth*.8,behavior:RM0()?"auto":"smooth"})});
function RM0(){return matchMedia("(prefers-reduced-motion:reduce)").matches}
