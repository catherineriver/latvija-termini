import html, json, os, sys
import datetime as dt
sys.path.insert(0, os.path.dirname(__file__))
import build, lv, ics, selfemployed, actions
from PIL import Image, ImageDraw, ImageFont
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT); os.makedirs("lv", exist_ok=True)
BASE = "https://catherineriver.github.io/latvija-termini/"
ICS = {"ru": "latvija-termini-2027.ics", "lv": "latvija-termini-2027-lv.ics"}
EVS = sorted(build.E, key=lambda x: x["date"])
def A(a, i): return None if a is None else (a[i], a[2])
RUEV = [dict(e, uid_key=e["title"], act=A(a, 0)) for e, a in zip(EVS, actions.MAIN)]
LVEV = [dict(e, title=t, desc=d, cat=lv.CAT[e["cat"]], uid_key=e["title"], act=A(a, 1)) for e, (t, d), a in zip(EVS, lv.EV, actions.MAIN)]
SE = selfemployed.EV
SERU = [dict(e, uid_key=e["title"], act=A(actions.EDS, 0)) for e in SE]
SELV = [dict(e, title=e["lv"][0], desc=e["lv"][1], cat=e["cat_lv"], uid_key=e["title"], act=A(actions.EDS, 1)) for e in SE]
SEICS = {"ru": "selfemployed-2027.ics", "lv": "selfemployed-2027-lv.ics"}
CATCLS = {"Декларация": "decl", "Налог на недвижимость": "nin", "Рабочие дни": "work", "Школы и садики": "school",
          "Самозанятые · общий режим": "se", "Самозанятые · MUN": "mun", "PVN": "vat"}

T = {
"ru": dict(lang="ru", locale="ru_RU", path="", prefix="", other="lv", other_label="Latviski",
 months=["Январь","Февраль","Март","Апрель","Май","Июнь","Июль","Август","Сентябрь","Октябрь","Ноябрь","Декабрь"],
 wd=["пн","вт","ср","чт","пт","сб","вс"], src="источник", srcw="Источник",
 site="Календарь жителя Латвии",
 title="Календарь жителя Латвии 2027: декларация, налог на недвижимость, школы и садики",
 desc="Бесплатный календарь-подписка (.ics) со сроками 2027 года: декларация о доходах (GID), налог на недвижимость (NĪN), приём в 1-й класс и садики в Риге, переносы рабочих дней. Есть отдельный календарь для самозанятых. Для Google, Apple и Outlook.",
 eyebrow="Latvija · 2026–2027 · бесплатно", h1="Все сроки жителя Латвии в вашем календаре",
 lead="Декларация о доходах, налог на недвижимость, приём в школу и садик, рабочие дни. Подпишитесь один раз: сроки и напоминания появятся в Google, Apple или Outlook календаре.",
 b_g="Добавить в Google Календарь", b_a="Apple / Outlook", b_d="Скачать .ics",
 meta="{n} событий · сверено с официальными источниками 11 ноября 2026",
 h_in="Что внутри", cards=[("Декларация (GID)","Открытие приёма, дедлайн 1 июня и 1 июля, три срока доплаты IIN."),("Налог на недвижимость","Уведомление до 15 февраля и четыре платежа с учётом выходных."),("Школы и садики (Рига)","Регистрация в 1-й класс, комплектование, сроки ответа на приглашение."),("Рабочие дни","В 2027 году переносов нет, но спорные дни отмечены.")],
 h_sub="Как подписаться", s_g=("Google Календарь","Откроется окно «Добавить календарь»."), s_a=("Apple, Outlook","Ссылка webcal откроет приложение календаря."), s_o=("Любое другое приложение","Вставьте адрес в «Подписка по URL»:"), s_btn="Подписаться",
 note="<b>Про напоминания.</b> Apple Календарь показывает напоминания из подписки (за 30, 14, 7, 3 и 1 день до важных сроков). Google Календарь их из подписки не берёт: включите уведомления в настройках этого календаря или импортируйте файл .ics.",
 h_cal="Календарь по месяцам", h_faq="Частые вопросы",
 faq=[("Это официальный календарь?","Нет. Это неофициальная сводка по открытым источникам: VID, Министерство финансов, Рижская дума, likumi.lv. Перед важными действиями проверяйте срок у источника, ссылки есть в каждом событии. Это не налоговая и не юридическая консультация."),
 ("Почему школы и садики только по Риге?","Сроки приёма устанавливает каждое самоуправление. Рижские правила я проверил, остальные города можно добавить по запросу."),
 ("Даты на школы и садики точные?","Для 1-го класса даты взяты из действующих рижских правил (регистрация до 15 мая, комплектование до 1 июня). Для садиков указана практика прошлых лет, график на 2027 год ещё не опубликован. Календарь стоит обновить весной."),
 ("Почему нет техосмотра?","Срок техосмотра зависит от вашей машины, а общей даты для всех нет. Проверить свой можно на e.csdd.lv."),
 ("Календарь обновится сам?","Да, если вы подписались по ссылке: приложение периодически перезагружает файл. Если сроки изменятся, файл будет обновлён.")],
 foot='Неофициальный проект. Данные: {l}. Обновлено 11.11.2026. <a href="https://github.com/catherineriver/latvija-termini" rel="noopener">Код на GitHub</a>.',
 calname="Дедлайны жителя Латвии 2026–2027", caldesc="Декларация, налог на недвижимость, рабочие дни, школы и садики (Рига). Сверено 11.11.2026.",
 og=("LATVIJA · 2027 · БЕСПЛАТНО",["Все сроки жителя","Латвии в вашем","календаре"],"Декларация · Налог на недвижимость · Школы и садики","Подписка .ics для календаря"),
 events=RUEV),
"lv": dict(lang="lv", locale="lv_LV", path="lv/", prefix="../", other="ru", other_label="По-русски",
 months=["Janvāris","Februāris","Marts","Aprīlis","Maijs","Jūnijs","Jūlijs","Augusts","Septembris","Oktobris","Novembris","Decembris"],
 wd=["pr","ot","tr","ce","pk","se","sv"], src="avots", srcw="Avots",
 site="Latvijas iedzīvotāja kalendārs",
 title="Latvijas iedzīvotāja kalendārs 2027: deklarācija, nekustamā īpašuma nodoklis, skolas un bērnudārzi",
 desc="Bezmaksas kalendāra abonements (.ics) ar 2027. gada termiņiem: gada ienākumu deklarācija (GID), nekustamā īpašuma nodoklis (NĪN), pieteikšanās 1. klasē un bērnudārzos Rīgā, pārceltās darba dienas. Ir atsevišķs kalendārs pašnodarbinātajiem. Google, Apple un Outlook kalendāram.",
 eyebrow="Latvija · 2026–2027 · bez maksas", h1="Visi Latvijas iedzīvotāja termiņi jūsu kalendārā",
 lead="Ienākumu deklarācija, nekustamā īpašuma nodoklis, pieteikšanās skolā un bērnudārzā, darba dienas. Abonējiet vienreiz: termiņi un atgādinājumi parādīsies Google, Apple vai Outlook kalendārā.",
 b_g="Pievienot Google kalendāram", b_a="Apple / Outlook", b_d="Lejupielādēt .ics",
 meta="{n} notikumi · pārbaudīts pēc oficiālajiem avotiem 2026. gada 11. novembrī",
 h_in="Kas iekšā", cards=[("Deklarācija (GID)","Pieņemšanas sākums, termiņi 1. jūnijā un 1. jūlijā, trīs IIN piemaksas termiņi."),("Nekustamā īpašuma nodoklis","Paziņojums līdz 15. februārim un četri maksājumi, ņemot vērā brīvdienas."),("Skolas un bērnudārzi (Rīga)","Pieteikšana 1. klasē, komplektēšana, atbildes termiņi uz uzaicinājumu."),("Darba dienas","2027. gadā pārcelšanas nav, bet strīdīgās dienas ir atzīmētas.")],
 h_sub="Kā abonēt", s_g=("Google kalendārs","Atvērsies logs “Pievienot kalendāru”."), s_a=("Apple, Outlook","Webcal saite atvērs kalendāra lietotni."), s_o=("Jebkura cita lietotne","Ielīmējiet adresi sadaļā “Abonēt pēc URL”:"), s_btn="Abonēt",
 note="<b>Par atgādinājumiem.</b> Apple kalendārs rāda atgādinājumus no abonementa (30, 14, 7, 3 un 1 dienu pirms svarīgiem termiņiem). Google kalendārs tos no abonementa neņem: ieslēdziet paziņojumus šī kalendāra iestatījumos vai importējiet .ics failu.",
 h_cal="Kalendārs pa mēnešiem", h_faq="Biežāk uzdotie jautājumi",
 faq=[("Vai šis ir oficiāls kalendārs?","Nē. Tas ir neoficiāls apkopojums no atvērtiem avotiem: VID, Finanšu ministrija, Rīgas dome, likumi.lv. Pirms svarīgām darbībām pārbaudiet termiņu avotā, saites ir katrā notikumā. Šī nav nodokļu vai juridiska konsultācija."),
 ("Kāpēc skolas un bērnudārzi tikai Rīgā?","Uzņemšanas termiņus nosaka katra pašvaldība. Rīgas noteikumus esmu pārbaudījis, citas pilsētas var pievienot pēc pieprasījuma."),
 ("Vai skolu un bērnudārzu datumi ir precīzi?","1. klasei datumi ņemti no spēkā esošajiem Rīgas noteikumiem (reģistrācija līdz 15. maijam, komplektēšana līdz 1. jūnijam). Bērnudārziem norādīta iepriekšējo gadu prakse, 2027. gada grafiks vēl nav publicēts. Pavasarī kalendārs jāatjaunina."),
 ("Kāpēc nav tehniskās apskates?","Tehniskās apskates termiņš ir atkarīgs no jūsu automašīnas, tāpēc kopīga datuma nav. Savu termiņu var pārbaudīt e.csdd.lv."),
 ("Vai kalendārs atjaunosies pats?","Jā, ja abonējāt pēc saites: lietotne periodiski pārlādē failu. Ja termiņi mainīsies, fails tiks atjaunināts.")],
 foot='Neoficiāls projekts. Dati: {l}. Atjaunināts 11.11.2026. <a href="https://github.com/catherineriver/latvija-termini" rel="noopener">Kods GitHub</a>.',
 calname="Latvijas iedzīvotāja termiņi 2026–2027", caldesc="Deklarācija, nekustamā īpašuma nodoklis, darba dienas, skolas un bērnudārzi (Rīga). Pārbaudīts 11.11.2026.",
 og=("LATVIJA · 2027 · BEZ MAKSAS",["Visi Latvijas","iedzīvotāja termiņi","jūsu kalendārā"],"Deklarācija · NĪN · Skolas un bērnudārzi","Kalendāra abonements .ics"),
 events=LVEV),
}
SEXT = {
"ru": dict(se_h="Календарь для самозанятых",
 se_lead="Отдельная подписка с квартальными отчётами и взносами VSAOI, сроками MUN и декларациями PVN. Подпишитесь на неё в дополнение к основному календарю: годовая декларация (GID) и налог IIN уже есть в нём.",
 se_note="Параметры (VSAOI 31,07% от базы не менее 780 EUR, IIN 25,5% и 33%) взяты из материалов VID за 2026 год, на 2027 год они могут измениться. С 2026 года обязательных минимальных взносов нет, а заранее сообщать VID ожидаемый доход больше не нужно. Если срок выпадает на выходной или праздник, событие стоит на последнем рабочем дне до него: по правилам срок обычно переносится вперёд, но надёжнее успеть заранее.",
 se_more="Показать все сроки ({n})", se_calname="Дедлайны самозанятых Латвии 2026–2027", se_caldesc="Квартальные отчёты и VSAOI, MUN, PVN. Сверено 11.11.2026.",
 card_se=("Самозанятые","Отдельный календарь: отчёты и взносы, MUN, PVN, ссылки на EDS."), actw="Где подать или оплатить",
 b_se="", sheet_a=("Календарь жителя","Декларация, налог на недвижимость, школы и садики в Риге, рабочие дни. Событий: {n}."), sheet_b=("Календарь самозанятого","Квартальные отчёты и VSAOI, MUN, PVN. Событий: {n}."), f_all="Все", past_show="Показать прошедшие", past_hide="Скрыть прошедшие", copy="Копировать", copied="Скопировано", next_l="Ближайший срок", next_in="через {n} дн.", next_today="сегодня", next_tom="завтра", go=""),
"lv": dict(se_h="Kalendārs pašnodarbinātajiem",
 se_lead="Atsevišķs abonements ar ceturkšņa ziņojumiem un VSAOI, MUN termiņiem un PVN deklarācijām. Abonējiet to papildus galvenajam kalendāram: gada deklarācija (GID) un IIN tajā jau ir.",
 se_note="Parametri (VSAOI 31,07% no bāzes ne mazāk kā 780 EUR, IIN 25,5% un 33%) ņemti no VID 2026. gada materiāliem, 2027. gadā tie var mainīties. Kopš 2026. gada obligāto minimālo iemaksu nav, un gaidāmos ienākumus iepriekš VID vairs nav jāpaziņo. Ja termiņš iekrīt brīvdienā vai svētku dienā, notikums ir pēdējā darba dienā pirms tās: parasti termiņš pārceļas uz priekšu, taču drošāk paspēt iepriekš.",
 se_more="Rādīt visus termiņus ({n})", se_calname="Latvijas pašnodarbināto termiņi 2026–2027", se_caldesc="Ceturkšņa ziņojumi un VSAOI, MUN, PVN. Pārbaudīts 11.11.2026.",
 card_se=("Pašnodarbinātie","Atsevišķs kalendārs: ziņojumi un iemaksas, MUN, PVN, saites uz EDS."), actw="Kur iesniegt vai samaksāt",
 b_se="", sheet_a=("Iedzīvotāja kalendārs","Deklarācija, nekustamā īpašuma nodoklis, skolas un bērnudārzi Rīgā, darba dienas. Notikumu: {n}."), sheet_b=("Pašnodarbinātā kalendārs","Ceturkšņa ziņojumi un VSAOI, MUN, PVN. Notikumu: {n}."), f_all="Visi", past_show="Rādīt pagājušos", past_hide="Slēpt pagājušos", copy="Kopēt", copied="Nokopēts", next_l="Tuvākais termiņš", next_in="pēc {n} d.", next_today="šodien", next_tom="rīt", go="")}
for k, t in T.items():
    t.update(SEXT[k]); t["se_events"] = SERU if k == "ru" else SELV
    ics.write_ics(t["events"], ICS[k], t["calname"], t["caldesc"], t["srcw"], t["actw"])
    ics.write_ics(t["se_events"], SEICS[k], t["se_calname"], t["se_caldesc"], t["srcw"], t["actw"])

def dlabel(d, t):
    return f"{d.day} {selfemployed.RU_GEN[d.month-1]}" if t["other"] == "lv" else f"{d.day}. {selfemployed.LV_NOM[d.month-1]}"

def timeline(base, loc, t):
    tl = []; last = None
    for ev, e in zip(base, loc):
        d = e["date"]
        if (d.year, d.month) != last:
            if last: tl.append("</ol></section>")
            yr = f" {d.year}"
            tl.append(f'<section class="month"><h3>{t["months"][d.month-1]}{yr}</h3><ol>'); last = (d.year, d.month)
        s = f' <a href="{html.escape(e["url"])}" rel="noopener">{t["src"]}</a>' if e["url"] else ""
        a = f'<p class="where"><a href="{html.escape(e["act"][1])}" rel="noopener">{html.escape(e["act"][0])}</a></p>' if e.get("act") else ""
        tl.append(f'<li class="ev {CATCLS[ev["cat"]]}" data-date="{d.isoformat()}" data-dl="{dlabel(d, t)}"><div class="date"><b>{d.day:02d}.{d.month:02d}</b><span>{t["wd"][d.weekday()]}</span></div><div class="body"><p class="tag"><i></i>{html.escape(e["cat"])}</p><h4>{html.escape(e["title"])}</h4><p>{html.escape(e["desc"])}{s}</p>{a}</div></li>')
    tl.append("</ol></section>")
    return "".join(tl)

JS = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "app.js"), encoding="utf-8").read()
CSS = open(os.path.join(os.path.dirname(__file__), "style.css"), encoding="utf-8").read()
CAT_ALL = {}
def render(k):
    t = T[k]; o = T[t["other"]]
    url = BASE + t["path"]; ourl = BASE + o["path"]
    feed = BASE + ICS[k]; webcal = "webcal://" + feed.split("://")[1]
    gcal = "https://calendar.google.com/calendar/r?cid=" + webcal.replace(":", "%3A").replace("/", "%2F")
    seen = {}
    for ev, e in zip(EVS, t["events"]): seen.setdefault(CATCLS[ev["cat"]], e["cat"])
    chips = "".join(f'<button type="button" class="{c}" data-f="{c}" aria-pressed="false"><i></i>{html.escape(n)}</button>' for c, n in seen.items())
    tl = timeline(EVS, t["events"], t); se_tl = timeline(SE, t["se_events"], t)
    se_feed = BASE + SEICS[k]; se_webcal = "webcal://" + se_feed.split("://")[1]
    se_gcal = "https://calendar.google.com/calendar/r?cid=" + se_webcal.replace(":", "%3A").replace("/", "%2F")
    nx = next((e for e in zip(EVS, t["events"]) if e[0]["date"] >= dt.date.today()), None) or list(zip(EVS, t["events"]))[-1]
    nd = nx[0]["date"]; ndays = (nd - dt.date.today()).days
    nin = t["next_today"] if ndays == 0 else t["next_tom"] if ndays == 1 else t["next_in"].format(n=ndays) if ndays > 1 else ""
    stamp = f'<aside class="stamp" id="next" data-in="{t["next_in"]}" data-today="{t["next_today"]}" data-tom="{t["next_tom"]}"><p class="s1">{t["next_l"]}</p><p class="s2">{dlabel(nd, t)}</p><p class="s3">{html.escape(nx[1]["title"])}</p><p class="s4">{nin}</p></aside>'
    cards = "".join(f'<div class="card"><b>{a}</b><span>{b}</span></div>' for a, b in t["cards"] + [t["card_se"]])
    faq = "".join(f"<div><h3>{q}</h3><p>{a}</p></div>" for q, a in t["faq"])
    links = '<a href="https://www.vid.gov.lv/lv/gada-ienakumu-deklaracija" rel="noopener">VID</a>, <a href="https://pip.riga.lv" rel="noopener">Rīgas pašvaldība</a>, <a href="https://likumi.lv/ta/id/341736" rel="noopener">likumi.lv</a>'
    ld = json.dumps({"@context": "https://schema.org", "@graph": [
        {"@type": "WebSite", "@id": BASE + "#site", "url": BASE, "name": t["site"], "inLanguage": k},
        {"@type": "WebPage", "@id": url + "#page", "url": url, "name": t["title"], "description": t["desc"], "inLanguage": k, "isPartOf": {"@id": BASE + "#site"}, "dateModified": "2026-11-11"},
        {"@type": "DataDownload", "name": t["calname"], "encodingFormat": "text/calendar", "contentUrl": feed, "inLanguage": k}, {"@type": "DataDownload", "name": t["se_calname"], "encodingFormat": "text/calendar", "contentUrl": se_feed, "inLanguage": k}]}, ensure_ascii=False)
    og = "og.png" if k == "ru" else "og-lv.png"
    p = t["prefix"]
    page = f'''<!doctype html>
<html lang="{k}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{t["title"]}</title>
<meta name="description" content="{t["desc"]}">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="ru" href="{BASE}">
<link rel="alternate" hreflang="lv" href="{BASE}lv/">
<link rel="alternate" hreflang="x-default" href="{BASE}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="theme-color" content="#e8ebe4">
<meta property="og:type" content="website">
<meta property="og:locale" content="{t["locale"]}">
<meta property="og:locale:alternate" content="{o["locale"]}">
<meta property="og:site_name" content="{t["site"]}">
<meta property="og:title" content="{t["title"]}">
<meta property="og:description" content="{t["desc"]}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}{og}">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{p}favicon.svg" type="image/svg+xml">
<link rel="alternate" type="text/calendar" title="{t["calname"]}" href="{p}{ICS[k]}">
<script type="application/ld+json">{ld}</script>
<style>{CSS}</style>
</head>
<body>
<svg width="0" height="0" aria-hidden="true" focusable="false"><filter id="rough"><feTurbulence type="fractalNoise" baseFrequency=".8" numOctaves="2" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="1.8"/></filter></svg>
<header class="top"><div class="wrap"><a class="lang" href="{ourl}" hreflang="{t["other"]}" lang="{t["other"]}">{t["other_label"]}</a>
<div class="hero">
<div><h1>{t["h1"]}</h1>
<p class="lead">{t["lead"]}</p>
<p class="meta">{t["meta"].format(n=len(t["events"])).replace(" · ", ", ")}</p></div>
{stamp}
</div></div></header>
<main class="wrap">
<h2>{t["h_sub"]}</h2>
<div class="sheets">
<section class="sheet"><h3>{t["sheet_a"][0]}</h3><div class="in"><p>{t["sheet_a"][1].format(n=len(t["events"]))}</p>
<div class="btns"><a class="btn" href="{gcal}" rel="noopener">{t["b_g"]}</a><a class="btn o" href="{webcal}">{t["b_a"]}</a><a class="dl" href="{p}{ICS[k]}" download>{t["b_d"]}</a></div>
<p class="url"><span>{t["s_o"][1]}</span><code>{feed}</code><button class="copy" type="button" data-url="{feed}" data-ok="{t["copied"]}">{t["copy"]}</button></p></div></section>
<section class="sheet" id="selfemployed-sub"><h3>{t["sheet_b"][0]}</h3><div class="in"><p>{t["sheet_b"][1].format(n=len(t["se_events"]))}</p>
<div class="btns"><a class="btn" href="{se_gcal}" rel="noopener">{t["b_g"]}</a><a class="btn o" href="{se_webcal}">{t["b_a"]}</a><a class="dl" href="{p}{SEICS[k]}" download>{t["b_d"]}</a></div>
<p class="url"><span>{t["s_o"][1]}</span><code>{se_feed}</code><button class="copy" type="button" data-url="{se_feed}" data-ok="{t["copied"]}">{t["copy"]}</button></p></div></section>
</div>
<p class="note">{t["note"]}</p>
<h2>{t["h_cal"]}</h2>
<div id="tools" class="chips" hidden><button type="button" data-f="all" aria-pressed="true">{t["f_all"]}</button>{chips}<button type="button" id="pastbtn" class="pb" data-show="{t["past_show"]}" data-hide="{t["past_hide"]}">{t["past_show"]}</button></div>
<div id="tl">{tl}</div>
<h2 id="selfemployed">{t["se_h"]}</h2>
<p>{t["se_lead"]}</p>
<p class="note">{t["se_note"]}</p>
<details class="all"><summary>{t["se_more"].format(n=len(t["se_events"]))}</summary>{se_tl}</details>
<h2>{t["h_faq"]}</h2>
<div class="faq">{faq}</div>
</main>
<footer><div class="wrap">{t["foot"].format(l=links)}</div></footer>
<script>{JS}</script>
</body></html>
'''
    open(("index.html" if k == "ru" else "lv/index.html"), "w", encoding="utf-8").write(page)
    # OG image
    W, H = 1200, 630
    im = Image.new("RGB", (W, H), "#e8ebe4"); d = ImageDraw.Draw(im)
    F = "/usr/share/fonts/truetype/dejavu/"
    fb = lambda s: ImageFont.truetype(F + "DejaVuSansCondensed-Bold.ttf", s); fs = lambda s: ImageFont.truetype(F + "DejaVuSansCondensed.ttf", s)
    d.rectangle([0, H-14, W, H], fill="#16202a")
    for i, line in enumerate(t["og"][1]): d.text((70, 90+i*100), line, font=fb(88), fill="#16202a")
    d.text((70, 420), t["og"][2], font=fs(30), fill="#4a5560")
    d.rectangle([70, 500, 560, 566], fill="#16202a"); d.text((96, 517), t["og"][3], font=fs(28), fill="#e8ebe4")
    d.rectangle([860, 70, 1130, 210], outline="#9b2335", width=6); d.rectangle([870, 80, 1120, 200], outline="#9b2335", width=2)
    d.text((885, 100), "11.11", font=fb(64), fill="#9b2335")
    im.save(og, optimize=True)
for k in T: render(k)

alts = f'<xhtml:link rel="alternate" hreflang="ru" href="{BASE}"/><xhtml:link rel="alternate" hreflang="lv" href="{BASE}lv/"/><xhtml:link rel="alternate" hreflang="x-default" href="{BASE}"/>'
open("sitemap.xml", "w").write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">'
    f'<url><loc>{BASE}</loc><lastmod>2026-11-11</lastmod>{alts}</url><url><loc>{BASE}lv/</loc><lastmod>2026-11-11</lastmod>{alts}</url></urlset>\n')
print("ok")
