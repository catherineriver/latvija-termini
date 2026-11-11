# Latvian texts for the 17 events, in the same order as sorted(build.E)
CAT = {"Декларация":"Deklarācija","Налог на недвижимость":"Nekustamā īpašuma nodoklis","Рабочие дни":"Darba dienas","Школы и садики":"Skolas un bērnudārzi"}
NIN = "Ceturtā daļa no gada nodokļa summas (likumā noteiktie termiņi: 31. marts, 15. maijs, 15. augusts, 15. novembris). {n} Par nokavējumu tiek aprēķināta nokavējuma nauda 0,05% dienā."
NOWORK = "{w} Pēc Labklājības ministrijas informācijas (2026. gada oktobrī) darba dienas 2027. gadā netiek pārceltas: Ministru kabineta rīkojums nav pieņemts. Darba devējs brīvdienu var noteikt pēc saviem ieskatiem."
EV = [
("NĪN: jāatnāk paziņojumam par 2027. gada nodokli",
 "Pašvaldība paziņo nodokļa summu līdz 15. februārim (e-adresē, e-pastā vai pa pastu). Ja paziņojums nav saņemts, īpašniekam mēneša laikā rakstveidā jāinformē pašvaldība. Rīgā: pip.riga.lv, tālr. 80000850."),
("Deklarācija: sākas GID pieņemšana par 2026. gadu (EDS)",
 "No 1. marta EDS var iesniegt gada ienākumu deklarāciju par 2026. gadu. Brīvprātīgo deklarāciju (atmaksa par ārstēšanu, mācībām u. c.) var iesniegt trīs gadu laikā. Ja kopējie ienākumi gadā pārsniedz 105 300 EUR, pieņemšana sākas 1. aprīlī."),
("NĪN: 1. nekustamā īpašuma nodokļa maksājums", NIN.format(n="Var samaksāt uzreiz par visu gadu.")),
("Bērnudārzi (Rīga): sākas grupu komplektēšana 1. septembrim",
 "Pēc iepriekšējo gadu prakses no 1. maija līdz 31. augustam bērnudārzi sūta uzaicinājumus bērniem, kuru vēlamais uzsākšanas datums ir līdz 1. septembrim. Līdz šim datumam pārbaudiet pieteikumu portālā latvija.gov.lv: izvēlētie bērnudārzi, uzsākšanas datums, kontakti. Uz uzaicinājumu jāatbild noteiktā termiņā (iepriekšējos gados — 15 dienās), citādi pieteikums tiek anulēts. Reģistrācija rindā notiek visu gadu. 2027. gada datumus precizējiet iksd.riga.lv."),
("Parasta darba diena (2027. gadā pārcelšanas nav)", NOWORK.format(w="Diena starp svētdienu, 2. maiju, un svētku dienu 4. maiju.")),
("NĪN: 2. nekustamā īpašuma nodokļa maksājums", NIN.format(n="15. maijs 2027 ir sestdiena, termiņš pārceļas uz pirmdienu, 17. maiju.")),
("1. klase (Rīga): pēdējais pieteikuma reģistrācijas termiņš",
 "Skolas veido 1. klases pretendentu sarakstus pēc pieteikumiem, kas reģistrēti līdz 15. maijam (ne vairāk kā piecās skolās). 15. maijs 2027 ir sestdiena: iesniedziet pieteikumu ne vēlāk kā piektdien, 14. maijā. Pēc saraksta izveides skola 5 darba dienu laikā nosūta paziņojumu; uz to jāatbild 10 kalendāro dienu laikā, citādi vieta tiek piedāvāta nākamajam."),
("Deklarācija: pēdējais obligātās GID iesniegšanas termiņš par 2026. gadu",
 "Pēdējā diena tiem, kam deklarācija jāiesniedz obligāti (saimnieciskā darbība, ienākumi ārvalstīs, nodokļa piemaksa u. c.) un kuru 2026. gada ienākumi nepārsniedz 105 300 EUR. Ja ienākumi lielāki — termiņš ir 1. jūlijs."),
("1. klase (Rīga): skolas pabeidz komplektēšanu",
 "Līdz 1. jūnijam skolām jāpabeidz 1. klašu komplektēšana. Sekojiet e-adresei un pastam: uz uzaicinājumu jāatbild 10 kalendāro dienu laikā. Saraksti mainās visu jūniju, kad citi atsakās no vietām."),
("Deklarācija: IIN piemaksas termiņš (vai 1. daļa)",
 "Aprēķinātā nodokļa samaksas termiņš, ja ienākumi līdz 105 300 EUR. Ja summa pārsniedz 640 EUR, to var sadalīt trīs daļās: 23. jūnijs, 23. jūlijs, 23. augusts. 23.–24. jūnijs ir svētku dienas. Parasti šādā gadījumā termiņš pārceļas uz nākamo darba dienu (piektdiena, 25. jūnijs), taču oficiālu apstiprinājumu šim gadam neatradu: drošāk samaksāt iepriekš."),
("Parasta darba diena (2027. gadā pārcelšanas nav)", NOWORK.format(w="Diena pēc Jāņu svētkiem, 23.–24. jūnijā.")),
("Deklarācija: termiņš, ja ienākumi pārsniedz 105 300 EUR",
 "Obligātā GID par 2026. gadu tiem, kuru kopējie ienākumi pārsniedza 105 300 EUR (pieņemšana no 1. aprīļa līdz 1. jūlijam). Nodokļa piemaksa šajā gadījumā — līdz 23. jūlijam (vai trīs daļās: 23. jūlijs, 23. augusts, 23. septembris)."),
("Deklarācija: 2. IIN piemaksas daļa",
 "Otrā daļa, ja maksājamais nodoklis pārsniedz 640 EUR un tiek maksāts trīs daļās (ienākumi līdz 105 300 EUR). Ja ienākumi virs 105 300 EUR — tas ir vienotā maksājuma vai pirmās daļas termiņš."),
("NĪN: 3. nekustamā īpašuma nodokļa maksājums", NIN.format(n="15. augusts 2027 ir svētdiena, termiņš pārceļas uz pirmdienu, 16. augustu.")),
("Deklarācija: 3. IIN piemaksas daļa", "Pēdējā piemaksas daļa, maksājot trīs daļās (ienākumi līdz 105 300 EUR)."),
("NĪN: 4. nekustamā īpašuma nodokļa maksājums", NIN.format(n="Gada pēdējais maksājums.")),
("Parasta darba diena (2027. gadā pārcelšanas nav)", NOWORK.format(w="Diena pēc Proklamēšanas dienas, 18. novembra.")),
]
