# Task: EV Greenfield — Germany

## Assignee and scope

- **Assignee:** Gilberto Garcia-Vazquez
- **Scope:** Germany EV greenfield manufacturing (cells, packs, vehicle assembly, cathode/anode, motor/inverter, recycling, charging equipment), 2015–2026
- **Target count:** 20 (training cycle)
- **Priority:** largest-investment-first
- **Start date:** 2026-04-24
- **Target finish date:** 2026-04-24

## What this task is

Gather and verify EV greenfield manufacturing records for Germany. Write verified records to `projects/nzipl/data/nzipl_ev_greenfield_global.json` following the `gather-ev-greenfield` skill protocol. Records ordered by `investmentM` descending.

## Sources to prioritize

- **German federal:** BMWK (`bmwk.de`), GTAI (`gtai.de`).
- **State investment agencies:** WFBB Brandenburg (`wfbb.de`), saarland.de, invest-in-thuringia.de, Niedersachsen.
- **German trade press:** Electrive.com (EN+DE), Battery-News.de, Handelsblatt, Tagesschau, Manager-Magazin.
- **Local-language queries:** `<Company> Werk <Stadt>`, `<Company> Zellfertigung <Stadt>`, `<Company> Batteriewerk`.
- **BNEF:** `projects/nzipl/data/nzipl_bnef_projects.json` — Mexico-only; no matches expected for Germany. (FDI_Combined.xlsx is deliberately NOT used — it belongs to a separate `/enrich-fdi` workstream.)

## Known candidates (priority order, investment-descending)

1. Tesla Gigafactory Berlin-Brandenburg (Grünheide) — vehicle_assembly; operating 2022
2. Northvolt Heide — cell; Cancelled (Chapter 11 Nov 2024; Lyten acquired June 2025)
3. Stellantis / ACC Kaiserslautern — cell; Cancelled Feb 2026
4. CATL Arnstadt (Thuringia) — cell; Operating 2023
5. Ford Cologne EV Center — vehicle_assembly; Operating June 2023
6. VW PowerCo Salzgitter — cell; Operating end 2025
7. SVOLT Überherrn (Saarland) — cell; Cancelled Jan 2025
8. BMW Irlbach / Strasskirchen — pack
9. VW Emden EV — vehicle_assembly
10. Gotion Göttingen — pack
11. Mercedes-Benz E-Campus Stuttgart — cell (pilot)
12. Porsche Cellforce Kirchentellinsfurt — cell (Tübingen area)
13. Microvast Ludwigsfelde — cell
14. Audi Ingolstadt PPE — vehicle_assembly
15. Mercedes-Benz Kamenz — pack
16. BMW Leipzig — pack
17. Akasol (BorgWarner) Darmstadt — pack
18. Kedali Erfurt — cell components (casings)
19. Leclanche Willstätt — cell
20. Mercedes-Benz Berlin-Brandenburg or alt

## What "done" looks like

- 20 records written.
- Every record has `verificationTier`, `verifiedBy`, `verifiedDate`, `license`, and at least one `sources.*` URL.
- Operating / Under-Construction records are all Tier 1.
- First 5 records pair-reviewed.
- Progress JSON counters reconcile.
