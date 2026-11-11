import datetime as dt
D = dt.date
HOL = {D(2026,11,18),D(2026,12,24),D(2026,12,25),D(2026,12,26),D(2026,12,31),D(2027,1,1),D(2027,3,26),D(2027,3,28),D(2027,3,29),D(2027,5,1),D(2027,5,4),D(2027,6,23),D(2027,6,24),D(2027,11,18),D(2027,12,24),D(2027,12,25),D(2027,12,26),D(2027,12,31)}
def ok(d): return d.weekday() < 5 and d not in HOL
def prev_wd(d):
    while not ok(d): d -= dt.timedelta(1)
    return d
RU_GEN = ["января","февраля","марта","апреля","мая","июня","июля","августа","сентября","октября","ноября","декабря"]
RU_NOM = ["январь","февраль","март","апрель","май","июнь","июль","август","сентябрь","октябрь","ноябрь","декабрь"]
RU_WDN = ["понедельник","вторник","среда","четверг","пятница","суббота","воскресенье"]
RU_WDG = ["понедельника","вторника","среды","четверга","пятницы"]
LV_DAT = ["janvārim","februārim","martam","aprīlim","maijam","jūnijam","jūlijam","augustam","septembrim","oktobrim","novembrim","decembrim"]
LV_NOM = ["janvāris","februāris","marts","aprīlis","maijs","jūnijs","jūlijs","augusts","septembris","oktobris","novembris","decembris"]
LV_ACC = ["janvāri","februāri","martu","aprīli","maiju","jūniju","jūliju","augustu","septembri","oktobri","novembri","decembri"]
LV_WDN = ["pirmdiena","otrdiena","trešdiena","ceturtdiena","piektdiena","sestdiena","svētdiena"]
LV_WDD = ["pirmdienai","otrdienai","trešdienai","ceturtdienai","piektdienai"]

def shift(nom):
    """returns (shown_date, ru_note, lv_note)"""
    if ok(nom): return nom, "", ""
    s = prev_wd(nom)
    if nom.weekday() >= 5:
        ru0 = f"{nom.day} {RU_GEN[nom.month-1]} — {RU_WDN[nom.weekday()]}."
        lv0 = f"{nom.day}. {LV_NOM[nom.month-1]} ir {LV_WDN[nom.weekday()]}."
    else:
        ru0 = f"{nom.day} {RU_GEN[nom.month-1]} — праздничный день."
        lv0 = f"{nom.day}. {LV_NOM[nom.month-1]} ir svētku diena."
    ru = f" {ru0} По правилам срок обычно переносится на следующий рабочий день, но надёжнее успеть до {RU_WDG[s.weekday()]}, {s.day} {RU_GEN[s.month-1]}."
    lv = f" {lv0} Parasti termiņš pārceļas uz nākamo darba dienu, taču drošāk paspēt līdz {LV_WDD[s.weekday()]}, {s.day}. {LV_DAT[s.month-1]}."
    return s, ru, lv

CAT_G = ("Самозанятые · общий режим", "Pašnodarbinātie · vispārējā kārtība")
CAT_M = ("Самозанятые · MUN", "Pašnodarbinātie · MUN")
CAT_V = ("PVN", "PVN")
U_G = "https://www.vid.gov.lv/lv/media/29738/download"
U_M = "https://www.vid.gov.lv/lv/media/30731/download"
U_V = "https://www.vid.gov.lv/lv/media/2299/download"
U_X = "https://www.vid.gov.lv/lv/media/1907/download"
EV = []
def add(date, ru, lv, cat, url, alarms):
    EV.append(dict(date=date, title=ru[0], desc=ru[1], lv=lv, cat=cat[0], cat_lv=cat[1], url=url, alarms=alarms))

Q = {1: ("IV квартал 2026", "2026. gada 4. ceturksni"), 4: ("I квартал 2027", "2027. gada 1. ceturksni"),
     7: ("II квартал 2027", "2027. gada 2. ceturksni"), 10: ("III квартал 2027", "2027. gada 3. ceturksni")}
# MUN: switch deadline (still ahead: 2026)
add(D(2026,12,15),
 ("MUN: последний срок заявки на переход на микропредприятие с 2027 года",
  "Чтобы перейти на налог микропредприятия (MUN) с другого режима, заявку нужно подать в VID до 15 декабря предыдущего года. По данным сторонних источников, MUN доступен при обороте до 50 000 EUR в год. Условия проверьте у VID."),
 ("MUN: pēdējais termiņš pieteikumam pāriet uz mikrouzņēmuma nodokli no 2027. gada",
  "Lai no cita režīma pārietu uz mikrouzņēmumu nodokli (MUN), pieteikums VID jāiesniedz līdz iepriekšējā gada 15. decembrim. Pēc trešo pušu avotu datiem MUN pieejams, ja gada apgrozījums nepārsniedz 50 000 EUR. Nosacījumus pārbaudiet VID."),
 CAT_M, U_M, (14, 3, 1))
for m in (1, 4, 7, 10):
    qr, ql = Q[m]
    # general regime: report 17th, VSAOI payment 23rd
    s, nr, nl = shift(D(2027, m, 17))
    add(s, (f"Самозанятые: отчёт за {qr} (pašnodarbinātā ziņojums)",
            f"Квартальный отчёт самозанятого в EDS: подать до 17 {RU_GEN[m-1]}.{nr} Взносы VSAOI нужно заплатить до 23-го числа. Общий режим."),
           (f"Pašnodarbinātā ziņojums par {ql}",
            f"Pašnodarbinātā ceturkšņa ziņojums EDS jāiesniedz līdz 17. {LV_DAT[m-1]}.{nl} VSAOI jāsamaksā līdz 23. datumam. Vispārējā kārtība."),
           CAT_G, U_G, (3, 1))
    if m == 1:
        s2 = D(2027, 1, 25)
        pr = " 23 января — суббота; VID указывает срок оплаты 25 января."
        pl = " 23. janvāris ir sestdiena; VID kā termiņu norāda 25. janvāri."
    else:
        s2, pr, pl = shift(D(2027, m, 23))
    add(s2, (f"Самозанятые: оплата VSAOI за {qr}",
             f"Взносы VSAOI самозанятого платятся на единый налоговый счёт до 23 {RU_GEN[m-1]}.{pr} Ставка 31,07% от месячной базы, не менее 780 EUR при доходе от 780 EUR в месяц (параметры 2026 года, на 2027 год уточняйте). Обязательных минимальных взносов с 2026 года нет."),
            (f"Pašnodarbinātie: VSAOI maksājums par {ql}",
             f"Pašnodarbinātā VSAOI jāsamaksā vienotajā nodokļu kontā līdz 23. {LV_DAT[m-1]}.{pl} Likme 31,07% no mēneša bāzes, ne mazāk kā 780 EUR, ja ienākumi no 780 EUR mēnesī (2026. gada parametri, 2027. gadam precizējiet). Obligāto minimālo iemaksu kopš 2026. gada nav."),
            CAT_G, U_G, (3, 1))
    # MUN: declaration 15th, payment 23rd
    s3, nr3, nl3 = shift(D(2027, m, 15))
    add(s3, (f"MUN: декларация за {qr}",
             f"Квартальная декларация плательщика налога микропредприятия в EDS: до 15 {RU_GEN[m-1]}.{nr3} Налог (25%: 20% IIN и 80% VSAOI) платится до 23-го числа."),
            (f"MUN: deklarācija par {ql}",
             f"Mikrouzņēmuma nodokļa maksātāja ceturkšņa deklarācija EDS jāiesniedz līdz 15. {LV_DAT[m-1]}.{nl3} Nodoklis (25%: 20% IIN un 80% VSAOI) jāsamaksā līdz 23. datumam."),
            CAT_M, U_M, (3, 1))
    s4, pr4, pl4 = shift(D(2027, m, 23))
    add(s4, (f"MUN: оплата налога за {qr}",
             f"Налог микропредприятия платится на единый налоговый счёт до 23 {RU_GEN[m-1]}.{pr4}"),
            (f"MUN: nodokļa maksājums par {ql}",
             f"Mikrouzņēmuma nodoklis jāsamaksā vienotajā nodokļu kontā līdz 23. {LV_DAT[m-1]}.{pl4}"),
            CAT_M, U_M, (3, 1))
# min tax
add(D(2027,7,23),
    ("Самозанятые: минимальный налог 50 EUR (если применимо)",
     "Если IIN, рассчитанный с дохода от хозяйственной деятельности, не превышает 50 EUR, до 23 июля нужно заплатить минимальный налог 50 EUR. Платить не нужно, например, если вы платили VSAOI за себя как самозанятый. Полный список исключений смотрите в материале VID."),
    ("Pašnodarbinātie: minimālais nodoklis 50 EUR (ja attiecas)",
     "Ja no saimnieciskās darbības ienākuma aprēķinātais IIN nepārsniedz 50 EUR, līdz 23. jūlijam jāsamaksā minimālais nodoklis 50 EUR. Nav jāmaksā, piemēram, ja veiktas VSAOI par sevi kā pašnodarbinātu personu. Pilns izņēmumu saraksts ir VID materiālā."),
    CAT_G, U_X, (7, 1))
# VAT monthly
for yy, m in [(2026, 11), (2026, 12)] + [(2027, k) for k in range(1, 13)]:
    pm, py = (12, yy - 1) if m == 1 else (m - 1, yy)
    s, nr, nl = shift(D(yy, m, 20))
    add(s, (f"PVN: декларация за {RU_NOM[pm-1]} {py} (оплата до 23-го)",
            f"Декларация PVN подаётся в EDS в течение 20 дней после окончания налогового периода (до 20 {RU_GEN[m-1]}).{nr} Налог платится до 23-го числа следующего месяца. Относится к зарегистрированным плательщикам PVN. Если у вас квартальный период, подавайте только в январе, апреле, июле и октябре."),
           (f"PVN: deklarācija par {py}. gada {LV_ACC[pm-1]} (samaksa līdz 23. datumam)",
            f"PVN deklarācija EDS jāiesniedz 20 dienu laikā pēc taksācijas perioda beigām (līdz 20. {LV_DAT[m-1]}).{nl} Nodoklis jāsamaksā līdz nākamā mēneša 23. datumam. Attiecas uz reģistrētiem PVN maksātājiem. Ja jums ceturkšņa periods, iesniedziet tikai janvārī, aprīlī, jūlijā un oktobrī."),
           CAT_V, U_V, (2,))
EV.sort(key=lambda e: e["date"])
