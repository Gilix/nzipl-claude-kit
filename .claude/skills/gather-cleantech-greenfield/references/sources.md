# Source catalog

Priority: Tier A → Tier B. Skip Tier C and below — the validator hard-rejects the worst offenders.

## Forbidden (validator blocks)

The validator rejects any `sources.*` URL from:
- `wikipedia.org`, `grokipedia.com` — tertiary summaries, not sources
- `linkedin.com`, `reddit.com`, `twitter.com`, `x.com`, `facebook.com`, `instagram.com` — social
- `medium.com` — self-published

Use Wikipedia for lead generation only. Never cite.

## Cross-cutting Tier A — government and IGO

These apply across all four techs.

**United States**: `energy.gov` (DOE Loan Programs Office, EERE Solar Energy Technologies Office, EERE Wind Energy Technologies Office, Hydrogen and Fuel Cell Technologies Office, Building Technologies Office for heat pumps), `selectusa.gov`, state econ-dev agencies (`michiganbusiness.org`, `tnecd.com`, `gadc.georgia.gov`, `texaswideopenforbusiness.com`, `azcommerce.com`).

**EU**: `commission.europa.eu`, `cinea.ec.europa.eu` (Innovation Fund), `eib.org` (EIB project disclosures), `bmwk.de` and `gtai.de` (Germany), `businessfrance.fr`, `investinspain.org`, `paih.gov.pl`, `hipa.hu`, `mse.gov.it`.

**Asia**: `meti.go.jp` and `jetro.go.jp` (Japan), `motie.go.kr` and `investkorea.org` (Korea), `miit.gov.cn` and `ndrc.gov.cn` (China), `investindia.gov.in` and `mnre.gov.in` (India MNRE — primary for solar/wind), `meti.gov.tw` (Taiwan).

**MENA / Africa**: `gov.uae` and `mocaf.gov.ae` (UAE), `mewa.gov.sa` and `pif.gov.sa` (Saudi Arabia), `mem.gov.ma` (Morocco), `dmre.gov.za` (South Africa).

**Latin America**: `gov.br/mdic` (Brazil), `gob.mx/se` (Mexico), `mineco.gob.cl` (Chile), `produccion.gob.ar` (Argentina).

**Multilaterals (corroborator only)**: `iea.org` (Tracker reports for hydrogen, solar, wind, heat pumps), `irena.org`, `worldbank.org` projects database.

## Tier A per tech — industry-specific

### Solar PV

**Companies**: First Solar `firstsolar.com`, JinkoSolar `jinkosolar.com`, LONGi `longi.com`, Trina Solar `trinasolar.com`, JA Solar `jasolar.com`, Canadian Solar `csisolar.com`, Hanwha Q Cells `qcells.com`, REC Group `recgroup.com`, Maxeon `maxeon.com`, Suniva `suniva.com`, Meyer Burger `meyerburger.com`, Enphase `enphase.com`, SolarEdge `solaredge.com`, Sungrow `en.sungrowpower.com`.

**Industry bodies**: `seia.org` (SEIA — US), `solarpowereurope.org`, `globalsolarcouncil.org`, `iea-pvps.org` (IEA-PVPS).

**Tier B trade press**: `pv-magazine.com` (named-author only), `pv-tech.org`, `taiyangnews.info`, `solarpowerworldonline.com`. Avoid press-release-only republishers.

### Wind

**Companies**: Vestas `vestas.com`, Siemens Gamesa `siemensgamesa.com`, GE Vernova `gevernova.com`, Nordex `nordex-online.com`, Goldwind `goldwind.com`, Mingyang `myse.com.cn`, Enercon `enercon.de`, Suzlon `suzlon.com`, TPI Composites `tpicomposites.com`, LM Wind Power `lmwindpower.com`, Cadeler `cadeler.com` (offshore foundations / install vessels).

**Industry bodies**: `gwec.net` (Global Wind Energy Council), `windeurope.org`, `acore.org` (US), `4coffshore.com` (the offshore-wind project database — Tier-A primary for offshore), `iea.org/programmes/iea-wind` (IEA Wind TCP).

**Tier B trade press**: `rechargenews.com`, `windpowermonthly.com`, `offshorewind.biz`, `northamericanwindpower.com`.

### Hydrogen / electrolyzers

**Companies — electrolyzer makers**: Nel `nelhydrogen.com`, ITM Power `itm-power.com`, Plug Power `plugpower.com`, Cummins (HyLYZER) `cummins.com`, Siemens Energy `siemens-energy.com`, John Cockerill `johncockerill.com`, McPhy `mcphy.com`, Sunfire `sunfire.de`, Topsoe `topsoe.com` (SOEC), Bloom Energy `bloomenergy.com`, Ceres Power `ceres.tech`.

**Companies — green ammonia / e-methanol**: CF Industries `cfindustries.com`, Yara `yara.com`, Topsoe `topsoe.com`, BASF `basf.com` (chemistries), Air Products `airproducts.com` (NEOM), Ørsted `orsted.com` (Project FlagshipONE), HIF Global `hifglobal.com`.

**Industry bodies**: `hydrogencouncil.com`, `hydrogeneurope.eu`, `iea.org/reports/hydrogen-tracker` (IEA Hydrogen Tracker — primary for FID-stage projects), `irena.org` (Green Hydrogen Tracker).

**Tier B trade press**: `hydrogeninsight.com`, `h2-bulletin.com`, `fuelcellsworks.com`, `ammoniaenergy.org`, `rechargenews.com` (cross-cutting).

**Government H2 programs (primary for project-level FID)**: US DOE `energy.gov/hydrogenhubs` (Regional Clean Hydrogen Hubs program), German `bmwk.de` IPCEI hydrogen, EU `cinea.ec.europa.eu` Innovation Fund, Japan METI Green Innovation Fund, UK `gov.uk/government/publications/hydrogen-allocation-round-2`.

### Heat pumps

**Companies**: Daikin `daikin.com`, Mitsubishi Electric `mitsubishielectric.com`, Carrier `carrier.com`, Trane `trane.com`, Bosch `bosch-thermotechnology.com`, Viessmann (now Carrier-owned) `viessmann.com`, Vaillant `vaillant.com`, NIBE `nibe.eu`, Panasonic `panasonic.com`, LG `lg.com/global/business`, Samsung HVAC `samsunghvac.com`, Johnson Controls `johnsoncontrols.com`, Copeland (compressor maker, formerly Emerson) `copeland.com`.

**Industry bodies**: `ehpa.org` (European Heat Pump Association — best primary for EU heat-pump factory data), `ahrinet.org` (US AHRI), `iea.org/programmes/heat-pumping-technologies` (IEA HPT), `nea.gov.sg` (Singapore for SE Asia commercial heat pumps).

**Tier B trade press**: `hvacrnews.com`, `ach&r-news.com`, `coolingpost.com`, `eubia.org`.

## Tier D — Dedup / receipt only (never citation)

Currently empty. Reserved for future dedup-target snapshots (e.g., a future BloombergNEF cleantech snapshot mirroring the Mexico EV one).

## Language-first rule

Asian and European parents often announce in local language weeks before English. Search local first; machine translation suffices for dates, numbers, coordinates.

| Parent language | Engine + query primitive |
|----------------|----------------|
| Chinese | Baidu: `<company hanzi> <project type hanzi> 工厂 <city hanzi>` |
| Japanese | Google.co.jp: `<company kanji> 工場 <prefecture>` |
| Korean | Naver: `<company hangul> 공장 <city>` |
| German | Handelsblatt / Tagesschau: `<company> Werk <Stadt>` |
| French | Le Monde / Les Échos: `<company> usine <ville>` |
| Spanish | El País / Reuters.es: `<company> planta <ciudad>` |
| Portuguese | Valor Econômico: `<company> fábrica <cidade>` |
| Italian | Il Sole 24 Ore: `<company> stabilimento <città>` |

Detailed country and tech templates: `appendix/search-playbook.md`.

## When to extend this file

Append a new Tier A source (government portal, open database, named-author trade outlet that consistently has earlier reporting) when you discover one. Log a one-liner in `appendix/common-mistakes.md` so others know. Tier B churn (newsroom renames, URL changes) — update in place.
