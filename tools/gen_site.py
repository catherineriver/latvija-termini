import html, datetime as dt
import build  # regenerates the .ics, exposes E
from PIL import Image, ImageDraw, ImageFont

BASE = "https://catherineriver.github.io/latvija-termini/"
ICS = "latvija-termini-2027.ics"
MON = ["января","февраля","марта","апреля","мая","июня","июля","августа","сентября","октября","ноября","декабря"]
MONN = ["Январь","Февраль","Март","Апрель","Май","Июнь","Июль","Август","Сентябрь","Октябрь","Ноябрь","Декабрь"]
WD = ["пн","вт","ср","чт","пт","сб","вс"]
CAT = {"Декларация":"decl","Налог на недвижимость":"nin","Рабочие дни":"work","Школы и садики":"school"}
rows = {}
for e in sorted(build.E, key=lambda x: x["date"]):
    rows.setdefault(e["date"].month, []).append(e)
tl = []
for m, evs in rows.items():
    tl.append(f'<section class="month"><h3>{MONN[m-1]}</h3><ol>')
    for e in evs:
        d = e["date"]
        src = f' <a href="{html.escape(e["url"])}" rel="noopener">источник</a>' if e["url"] else ""
        tl.append(f'<li class="ev {CAT[e["cat"]]}"><div class="date"><b>{d.day}</b><span>{WD[d.weekday()]}</span></div>'
                  f'<div class="body"><div class="tag">{e["cat"]}</div><h4>{html.escape(e["title"])}</h4>'
                  f'<p>{html.escape(e["desc"])}{src}</p></div></li>')
    tl.append('</ol></section>')
timeline = "\n".join(tl)

feed = BASE + ICS
webcal = "webcal://" + feed.split("://")[1]
gcal = "https://calendar.google.com/calendar/r?cid=" + webcal.replace(":", "%3A").replace("/", "%2F")

TITLE = "Календарь жителя Латвии 2027: декларация, налог на недвижимость, школы и садики"
DESC = "Бесплатный календарь-подписка (.ics) со сроками 2027 года: декларация о доходах (GID), налог на недвижимость (NĪN), приём в 1-й класс и садики в Риге, переносы рабочих дней. Для Google, Apple и Outlook."
LD = f'''{{"@context":"https://schema.org","@graph":[
{{"@type":"WebSite","@id":"{BASE}#site","url":"{BASE}","name":"Календарь жителя Латвии","inLanguage":"ru"}},
{{"@type":"WebPage","@id":"{BASE}#page","url":"{BASE}","name":"{TITLE}","description":"{DESC}","inLanguage":"ru","isPartOf":{{"@id":"{BASE}#site"}},"dateModified":"2026-11-11"}},
{{"@type":"DataDownload","name":"Календарь сроков 2027 (iCalendar)","encodingFormat":"text/calendar","contentUrl":"{feed}"}}
]}}'''

page = f'''<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{TITLE}</title>
<meta name="description" content="{DESC}">
<link rel="canonical" href="{BASE}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="theme-color" content="#8c2b35">
<meta property="og:type" content="website">
<meta property="og:locale" content="ru_RU">
<meta property="og:site_name" content="Календарь жителя Латвии">
<meta property="og:title" content="{TITLE}">
<meta property="og:description" content="{DESC}">
<meta property="og:url" content="{BASE}">
<meta property="og:image" content="{BASE}og.png">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="alternate" type="text/calendar" title="Календарь сроков 2027" href="{ICS}">
<script type="application/ld+json">{LD}</script>
<style>
:root{{--ink:#241c1d;--mut:#6b5f60;--bg:#faf6f1;--card:#fff;--line:#e8dfd6;--red:#8c2b35;--red2:#a63a45;
--decl:#8c2b35;--nin:#1f6f63;--work:#7a6a2a;--school:#34508f}}
*{{box-sizing:border-box}}html{{scroll-behavior:smooth}}
body{{margin:0;font:17px/1.6 ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif;color:var(--ink);background:var(--bg)}}
a{{color:var(--red)}}
.wrap{{max-width:920px;margin:0 auto;padding:0 20px}}
header.hero{{background:var(--red);color:#fff;padding:64px 0 56px;position:relative;overflow:hidden}}
header.hero:after{{content:"";position:absolute;left:0;right:0;bottom:0;height:10px;background:#fff;opacity:.9;clip-path:inset(0)}}
.eyebrow{{letter-spacing:.14em;text-transform:uppercase;font-size:13px;opacity:.85}}
h1{{font:700 clamp(30px,5.4vw,52px)/1.1 Georgia,"Times New Roman",serif;margin:.4em 0 .4em;letter-spacing:-.01em}}
.lead{{font-size:19px;max-width:640px;opacity:.95;margin:0 0 28px}}
.cta{{display:flex;gap:12px;flex-wrap:wrap}}
.btn{{display:inline-block;padding:13px 22px;border-radius:10px;font-weight:600;text-decoration:none;border:2px solid #fff}}
.btn.p{{background:#fff;color:var(--red)}}.btn.s{{color:#fff}}
.btn:hover{{transform:translateY(-1px)}}
.meta{{margin-top:18px;font-size:14px;opacity:.85}}
main{{padding:40px 0 20px}}
h2{{font:700 28px/1.2 Georgia,serif;margin:2em 0 .6em}}
.cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:14px}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:18px}}
.card b{{display:block;margin-bottom:4px}}
.card span{{color:var(--mut);font-size:15px}}
.sub{{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px}}
.sub .card a.btn{{margin-top:10px;border-color:var(--red);color:var(--red);padding:9px 16px}}
code{{background:#f1e9e0;padding:2px 6px;border-radius:6px;font-size:14px;word-break:break-all}}
.month h3{{font:700 22px Georgia,serif;margin:1.6em 0 .5em;color:var(--red)}}
ol{{list-style:none;margin:0;padding:0;display:grid;gap:12px}}
.ev{{display:flex;gap:16px;background:var(--card);border:1px solid var(--line);border-left:5px solid var(--c,#999);border-radius:12px;padding:16px}}
.ev.decl{{--c:var(--decl)}}.ev.nin{{--c:var(--nin)}}.ev.work{{--c:var(--work)}}.ev.school{{--c:var(--school)}}
.date{{min-width:52px;text-align:center}}.date b{{display:block;font:700 30px/1 Georgia,serif}}.date span{{color:var(--mut);font-size:14px}}
.tag{{font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--c)}}
.ev h4{{margin:.1em 0 .3em;font-size:18px}}.ev p{{margin:0;color:#4a4041;font-size:15.5px}}
.note{{background:#fff7e6;border:1px solid #f0d9a8;border-radius:12px;padding:16px 18px;font-size:15.5px}}
details{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px 18px;margin:10px 0}}
summary{{cursor:pointer;font-weight:600}}
footer{{border-top:1px solid var(--line);margin-top:48px;padding:28px 0 48px;color:var(--mut);font-size:14px}}
@media(max-width:520px){{.ev{{flex-direction:column;gap:6px}}.date{{text-align:left;display:flex;gap:8px;align-items:baseline}}}}
</style>
</head>
<body>
<header class="hero"><div class="wrap">
<div class="eyebrow">Latvija · 2027 · бесплатно</div>
<h1>Все сроки жителя Латвии в вашем календаре</h1>
<p class="lead">Декларация о доходах, налог на недвижимость, приём в школу и садик, рабочие дни. Подпишитесь один раз: сроки и напоминания появятся в Google, Apple или Outlook календаре.</p>
<div class="cta"><a class="btn p" href="{gcal}" rel="noopener">Добавить в Google Календарь</a><a class="btn s" href="{webcal}">Apple / Outlook</a><a class="btn s" href="{ICS}" download>Скачать .ics</a></div>
<div class="meta">{len(build.E)} событий · сверено с официальными источниками 11 ноября 2026</div>
</div></header>
<main class="wrap">
<h2>Что внутри</h2>
<div class="cards">
<div class="card"><b>Декларация (GID)</b><span>Открытие приёма, дедлайн 1 июня и 1 июля, три срока доплаты IIN.</span></div>
<div class="card"><b>Налог на недвижимость</b><span>Уведомление до 15 февраля и четыре платежа с учётом выходных.</span></div>
<div class="card"><b>Школы и садики (Рига)</b><span>Регистрация в 1-й класс, комплектование, сроки ответа на приглашение.</span></div>
<div class="card"><b>Рабочие дни</b><span>В 2027 году переносов нет, но спорные дни отмечены.</span></div>
</div>

<h2>Как подписаться</h2>
<div class="sub">
<div class="card"><b>Google Календарь</b><span>Откроется окно «Добавить календарь».</span><br><a class="btn" href="{gcal}" rel="noopener">Подписаться</a></div>
<div class="card"><b>Apple, Outlook</b><span>Ссылка webcal откроет приложение календаря.</span><br><a class="btn" href="{webcal}">Подписаться</a></div>
<div class="card"><b>Любое другое приложение</b><span>Вставьте адрес в «Подписка по URL»:</span><br><code>{feed}</code></div>
</div>
<p class="note"><b>Про напоминания.</b> Apple Календарь показывает напоминания из подписки (за 30, 14, 7, 3 и 1 день до важных сроков). Google Календарь их из подписки не берёт: включите уведомления в настройках этого календаря или импортируйте файл .ics.</p>

<h2>Календарь 2027 по месяцам</h2>
{timeline}

<h2>Частые вопросы</h2>
<details><summary>Это официальный календарь?</summary><p>Нет. Это неофициальная сводка по открытым источникам: VID, Министерство финансов, Рижская дума, likumi.lv. Перед важными действиями проверяйте срок у источника, ссылки есть в каждом событии. Это не налоговая и не юридическая консультация.</p></details>
<details><summary>Почему школы и садики только по Риге?</summary><p>Сроки приёма устанавливает каждое самоуправление. Рижские правила я проверил, остальные города можно добавить по запросу.</p></details>
<details><summary>Даты на школы и садики точные?</summary><p>Для 1-го класса даты взяты из действующих рижских правил (регистрация до 15 мая, комплектование до 1 июня). Для садиков указана практика прошлых лет, график на 2027 год ещё не опубликован. Календарь стоит обновить весной.</p></details>
<details><summary>Почему нет техосмотра?</summary><p>Срок техосмотра зависит от вашей машины, а общей даты для всех нет. Проверить свой можно на e.csdd.lv.</p></details>
<details><summary>Календарь обновится сам?</summary><p>Да, если вы подписались по ссылке: приложение периодически перезагружает файл. Если сроки изменятся, я обновлю файл, и изменения придут к вам.</p></details>

</main>
<footer><div class="wrap">Неофициальный проект. Данные: <a href="https://www.vid.gov.lv/lv/gada-ienakumu-deklaracija" rel="noopener">VID</a>, <a href="https://pip.riga.lv" rel="noopener">Rīgas pašvaldība</a>, <a href="https://likumi.lv/ta/id/341736" rel="noopener">likumi.lv</a>. Обновлено 11.11.2026. <a href="https://github.com/catherineriver/latvija-termini" rel="noopener">Код на GitHub</a>.</div></footer>
</body></html>
'''
open("index.html","w",encoding="utf-8").write(page)

open("robots.txt","w").write(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}sitemap.xml\n")
open("sitemap.xml","w").write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>{BASE}</loc><lastmod>2026-11-11</lastmod><changefreq>monthly</changefreq><priority>1.0</priority></url></urlset>\n')
open(".nojekyll","w").write("")
open("favicon.svg","w").write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="12" fill="#8c2b35"/><rect x="10" y="14" width="44" height="40" rx="6" fill="#fff"/><rect x="10" y="14" width="44" height="12" rx="6" fill="#a63a45"/><rect x="16" y="32" width="8" height="8" fill="#8c2b35"/><rect x="28" y="32" width="8" height="8" fill="#ccc"/><rect x="40" y="32" width="8" height="8" fill="#ccc"/><rect x="16" y="44" width="8" height="6" fill="#ccc"/></svg>')
open("404.html","w",encoding="utf-8").write('<!doctype html><meta charset="utf-8"><meta name="robots" content="noindex"><title>Страница не найдена</title><p style="font:18px system-ui;padding:40px">Страница не найдена. <a href="./">Календарь жителя Латвии 2027</a></p>')

# OG image
W,H=1200,630
im=Image.new("RGB",(W,H),"#8c2b35"); d=ImageDraw.Draw(im)
F="/usr/share/fonts/truetype/dejavu/"
fb=lambda s:ImageFont.truetype(F+"DejaVuSerif-Bold.ttf",s); fs=lambda s:ImageFont.truetype(F+"DejaVuSans.ttf",s)
d.rectangle([0,H-14,W,H],fill="#fff")
d.text((70,70),"LATVIJA · 2027 · БЕСПЛАТНО",font=fs(26),fill="#f0c9cd")
for i,t in enumerate(["Все сроки жителя","Латвии в вашем","календаре"]): d.text((70,130+i*88),t,font=fb(74),fill="#fff")
d.text((70,440),"Декларация · Налог на недвижимость · Школы и садики",font=fs(30),fill="#fff")
d.rounded_rectangle([70,500,520,566],radius=14,fill="#fff"); d.text((96,517),"Подписка .ics для календаря",font=fs(28),fill="#8c2b35")
im.save("og.png",optimize=True)
print("ok", len(page))
