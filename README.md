# Календарь жителя Латвии 2027

Неофициальный календарь-подписка (.ics) со сроками 2027 года: декларация о доходах (GID), налог на недвижимость (NĪN), приём в 1-й класс и садики в Риге, рабочие дни.

Сайт: https://catherineriver.github.io/latvija-termini/
Подписка: `https://catherineriver.github.io/latvija-termini/latvija-termini-2027.ics`

## Пересборка

```
python3 tools/gen_site.py   # пересоздаёт .ics, index.html, sitemap.xml, og.png
```

Нужен Pillow (для og.png). Даты и источники лежат в `tools/build.py`.

Данные из открытых источников (VID, Rīgas pašvaldība, likumi.lv), сверено 11.11.2026. Не является налоговой или юридической консультацией.
