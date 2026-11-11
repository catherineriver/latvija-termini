import datetime as dt, hashlib
def esc(s): return s.replace("\\","\\\\").replace(";",chr(92)+";").replace(",","\\,").replace("\n","\\n")
def fold(line):
    b=line.encode(); out=[]
    while len(b)>75:
        cut=75
        while (b[cut]&0xC0)==0x80: cut-=1
        out.append(b[:cut].decode()); b=b" "+b[cut:]
    out.append(b.decode()); return "\r\n".join(out)
def write_ics(events, path, name, desc, src_word, act_word="", domain="iedzivotaja-termini.lv"):
    L=["BEGIN:VCALENDAR","VERSION:2.0","PRODID:-//Iedzivotaja termini//LV 2027//"+("LV" if "lv" in path else "RU"),
       "CALSCALE:GREGORIAN","METHOD:PUBLISH","X-WR-CALNAME:"+esc(name),"X-WR-TIMEZONE:Europe/Riga",
       "X-WR-CALDESC:"+esc(desc),"REFRESH-INTERVAL;VALUE=DURATION:P1D","X-PUBLISHED-TTL:P1D"]
    for e in events:
        uid=hashlib.sha1((e["date"].isoformat()+e["uid_key"]).encode()).hexdigest()[:16]+"@"+domain
        act=e.get("act")
        d=e["desc"]
        if act: d+=f"\n\n{act_word}: {act[0]}: {act[1]}"
        if e["url"]: d+=("\n" if act else "\n\n")+f"{src_word}: {e['url']}"
        link=act[1] if act else e["url"]
        L+=["BEGIN:VEVENT",f"UID:{uid}","DTSTAMP:20261111T190000Z",
            f"DTSTART;VALUE=DATE:{e['date']:%Y%m%d}",f"DTEND;VALUE=DATE:{e['date']+dt.timedelta(1):%Y%m%d}",
            "SUMMARY:"+esc(e["title"]),"DESCRIPTION:"+esc(d),"CATEGORIES:"+esc(e["cat"]),"TRANSP:TRANSPARENT"]
        if link: L.append("URL:"+link)
        for a in e["alarms"]:
            trig="PT9H" if a==0 else (f"-P{a-1}DT15H" if a>1 else "-PT15H")
            L+=["BEGIN:VALARM","ACTION:DISPLAY","DESCRIPTION:"+esc(e["title"]),f"TRIGGER:{trig}","END:VALARM"]
        L.append("END:VEVENT")
    L.append("END:VCALENDAR")
    with open(path,"w",newline="",encoding="utf-8") as f: f.write("\r\n".join(fold(x) for x in L)+"\r\n")
