# Latvia Resident Deadlines Calendar 2027

An unofficial subscribable calendar (.ics) of 2027 deadlines for residents of Latvia: annual income tax return (GID), real estate tax (NĪN), school and kindergarten admission in Riga, and workday transfers.

- Website (Russian): https://catherineriver.github.io/latvija-termini/
- Website (Latvian): https://catherineriver.github.io/latvija-termini/lv/
- Subscription feed (Russian): `https://catherineriver.github.io/latvija-termini/latvija-termini-2027.ics`
- Subscription feed (Latvian): `https://catherineriver.github.io/latvija-termini/latvija-termini-2027-lv.ics`

## What's included

17 events with reminders (30, 14, 7, 3 and 1 day ahead for key deadlines):

- Income tax return for 2026: filing opens 1 March, deadlines 1 June and 1 July, payment dates 23 June / 23 July / 23 August
- Real estate tax: notice by 15 February, payments on 31 March, 15 May, 15 August, 15 November
- Riga school (grade 1) and kindergarten admission dates
- Workdays that are not transferred in 2027

Vehicle inspection (CSDD) is not included because it depends on each vehicle.

## Rebuilding

```
python3 tools/gen_site.py
```

This regenerates both `.ics` files, `index.html`, `lv/index.html`, `sitemap.xml` and the Open Graph images. Requires Python 3 and Pillow. Dates and sources live in `tools/build.py`, Latvian texts in `tools/lv.py`.

## Disclaimer

Based on public sources (VID, Rīgas pašvaldība, likumi.lv), checked on 11 November 2026. This is not tax or legal advice. Verify deadlines at the source linked in each event. Kindergarten dates reflect previous years' practice; the 2027 schedule had not been published yet.
