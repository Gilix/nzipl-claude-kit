# Search playbook

Query templates by technology and country. Copy-paste into your search engine of choice (prefer the country's native engine when it exists — Naver for Korea, Baidu for China, Google.de for Germany, etc.).

## Query primitives

Every search starts from one of these primitives, combined with quotation marks for the company name:

1. `"<Company>" <project-type> <city> <country>`
2. `"<Company>" <project-type> factory site:<company-domain>`
3. `"<Company>" <project-type> "<city>" -site:wikipedia.org`
4. `"<Company>" <project-type> permit <state/province>`
5. `"<Company>" <project-type> groundbreaking <year>`
6. `"<Company>" <project-type> announcement <year>`

## Project-type keywords by tech

**Solar**: `polysilicon`, `wafer`, `cell`, `module`, `gigafactory`, `inverter`, `tracker`, `solar plant` (factory, not generation)

**Wind**: `nacelle`, `blade`, `tower`, `turbine factory`, `offshore foundation`, `jacket`, `wind plant manufacturing`

**Hydrogen**: `electrolyzer`, `gigafactory`, `hydrogen plant`, `green ammonia plant`, `e-methanol plant`, `SAF facility`, `fuel cell factory`

**Heat pumps**: `heat pump factory`, `compressor plant`, `HVAC factory`, `heat pump assembly`

## Country playbooks

### United States

```
site:energy.gov "<Company>" "<State>"
site:energy.gov/hydrogenhubs "<Company>"   # for H2
site:selectusa.gov "<Company>"
site:<state>.gov "<Company>" tax incentive
"<Company>" "<City>" permit application
```

Key state agency domains: `gadc.georgia.gov`, `michiganbusiness.org`, `tnecd.com`, `texaswideopenforbusiness.com`, `azcommerce.com`, `oregon4biz.com`.

For solar specifically: SEIA's `seia.org/solar-industry-data` tracks announced US module / cell capacity.

### Germany

```
site:bmwk.de "<Company>"
site:gtai.de "<Company>"
"<Company>" Werk "<Stadt>"
"<Company>" Solarfabrik OR Modulfabrik OR Zellfertigung "<Stadt>"
"<Company>" Windkraft Werk "<Stadt>"
"<Company>" Elektrolyse Werk "<Stadt>"
"<Company>" Wärmepumpe Werk "<Stadt>"
site:brandenburg.de OR site:sachsen.de OR site:nrw.de "<Company>"
```

Tier A German sources: BMWK, GTAI, state economy ministries. Tier B: Handelsblatt, Süddeutsche, Tagesschau, FAZ.

### Spain

```
site:investinspain.org "<Company>"
"<Company>" fábrica "<Ciudad>"
"<Company>" planta solar OR eólica OR hidrógeno "<Región>"
"<Company>" gigafábrica
```

Spain has high solar / wind / green-hydrogen activity. Iberdrola, Acciona, Solaria as domestic sponsors; First Solar, Cellnex as inbound.

### France

```
site:businessfrance.fr "<Company>"
site:ecologie.gouv.fr "<Company>"
"<Company>" usine "<Ville>"
"<Company>" gigafactory "<Région>"
"<Company>" pompe à chaleur usine
```

Heat pumps are an active French focus 2024–2026.

### China

```
site:miit.gov.cn "<Company-hanzi>"
site:ndrc.gov.cn "<Company-hanzi>"
"<Company-hanzi>" 工厂 "<City-hanzi>"
"<Company-hanzi>" 光伏 OR 风电 OR 氢能 OR 电解槽 工厂
```

Key transliterations:
- Solar: 隆基 (LONGi), 晶科 (Jinko), 天合 (Trina), 晶澳 (JA Solar), 阿特斯 (Canadian Solar/CSI), 正泰 (Chint), 协鑫 (GCL).
- Wind: 金风 (Goldwind), 远景 (Envision), 明阳 (Mingyang), 上海电气 (Shanghai Electric Wind), 三一 (Sany).
- Hydrogen: 隆基氢能 (LONGi Hydrogen), 阳光氢能 (Sungrow Hydrogen), 国家电投 (SPIC), 中船重工 (CSIC).

### India

```
site:investindia.gov.in "<Company>"
site:mnre.gov.in "<Company>"
"<Company>" "<City>" solar OR wind OR hydrogen
"<Company>" gigafactory India
"<Company>" PLI scheme solar OR wind
```

PLI (Production Linked Incentive) notifications on `mnre.gov.in` and `heavyindustries.gov.in` are authoritative for Indian announcements. Reliance, Adani Green, Tata Power Solar, Waaree, Vikram Solar, Goldi Solar, Suzlon Energy.

### South Korea

```
site:motie.go.kr "<Company>"
site:investkorea.org "<Company>"
"<Company-hangul>" 공장 "<City>"
"<Company-hangul>" 태양광 OR 풍력 OR 수소 공장
```

Hanwha Q Cells (한화큐셀), Hyundai Heavy Industries (현대중공업) Wind, Doosan Enerbility (두산에너빌리티) hydrogen / SMR.

### Japan

```
site:meti.go.jp "<Company>"
site:jetro.go.jp "<Company>"
"<Company-kanji>" 工場 "<Prefecture>"
"<Company-kanji>" 太陽光 OR 風力 OR 水素 OR ヒートポンプ
```

Heat pumps especially: Daikin (ダイキン), Mitsubishi Electric (三菱電機), Panasonic (パナソニック).

### Brazil

```
site:gov.br/mdic "<Company>"
site:apexbrasil.com.br "<Company>"
"<Company>" fábrica "<Cidade>"
"<Company>" "<Estado>" eólica OR solar OR hidrogênio verde
```

Brazil's wind manufacturing cluster: Bahia, Ceará, Pernambuco. Vestas Aquiraz, Siemens Gamesa Camaçari, GE Vernova Pernambuco. Green H2: Pecém Complex (Ceará).

### Mexico

```
site:gob.mx/se "<Empresa>"
"<Company>" planta <ciudad> México
"<Empresa>" "<Estado>" parque industrial
"<Empresa>" calentamiento OR bomba de calor
```

Mexican cleantech manufacturing is relatively thin outside heat pumps (Carrier, Trane, Lennox in Monterrey / Saltillo / Nuevo Laredo) and solar BoS (Mitsubishi Electric in Querétaro, Schneider in Apodaca).

### Saudi Arabia / UAE

```
site:mewa.gov.sa "<Company>"
site:pif.gov.sa "<Company>"
site:masdar.ae "<Company>"
"<Company>" NEOM
"<Company>" gigafactory Saudi
```

NEOM Helios H2, ACWA Power solar / hydrogen, Masdar offshore wind. Most projects involve PIF / Masdar as anchor sponsor.

### Egypt / Morocco

```
site:moic.gov.eg "<Company>"
site:mem.gov.ma "<Company>"
"<Company>" "<City>" solar plant
"<Company>" Egypt OR Morocco green hydrogen
```

Strong inbound solar (Scatec, Engie, Acwa Power) and emerging green-H2 (Fortescue Egypt, OCP Morocco).

### South Africa

```
site:dmre.gov.za "<Company>"
"<Company>" "<Province>" solar OR wind
"<Company>" South Africa hydrogen hub
```

Sasol-Air Liquide H2 hub at Sasolburg; multiple inbound solar developers in Northern Cape.

### Vietnam / Cambodia / Malaysia / Thailand (solar AD/CVD circumvention)

These countries received an unusual surge of "new solar factory" announcements 2022–2024 in response to US AD/CVD on Chinese solar. Apply extra scrutiny: distinguish real cell + module production from module-only assembly with imported cells. The CBP enforcement actions (US Customs) are a useful filter — companies that took CBP action are not Tier 1 candidates.

```
"<Company>" Vietnam OR Cambodia OR Malaysia OR Thailand solar factory
"<Company>" CBP enforcement OR detention   # red-flag check
site:trade.gov "<Company>"   # for AD/CVD records
```

## Query anti-patterns

Avoid these:

- **Date-bounded "<Company> 2024"** alone — too noisy. Pair with project-type and geography.
- **Generic "solar factory <country>"** — returns aggregator listicles. Start with the company.
- **Relying on Wikipedia infobox numbers** — they lag real announcements by months and often cite the largest announced figure, not the current one.
- **Using the first result uncritically** — usually a press release repackaged by a wire service. Check the original company domain.
- **Trusting the "GW" headline alone** — solar GW figures often conflate cell vs module vs nameplate vs effective capacity. Verify which.
- **"100 MW heat pump factory"** — heat pump capacity is units/year or MW-thermal/year, not MW-electric. Recheck the unit.

## Dead-end recovery

When a search returns nothing useful:

1. **Switch language.** If the company is Asian or European, try the native-language query.
2. **Narrow on permits.** `"<Company>" "<State/Province>" "permit" OR "incentive" OR "grant"`.
3. **Widen to the parent.** If the facility operator is a subsidiary, search the parent company.
4. **Check supplier announcements.** Equipment vendors (Manz for solar, LM Wind Power for blades, Siemens Energy for electrolyzers, Bitzer / Copeland for heat-pump compressors) announce plant orders. These often confirm a plant exists even when the operator hasn't publicized it.
5. **Check construction contractor announcements.** Bechtel, Fluor, M+W Group, Exyte regularly announce solar / hydrogen plant contracts.
6. **Check city-level economic-development news.** `areadevelopment.com`, `businessfacilities.com`, regional papers.
7. **Last resort: log the candidate at Tier 3** with the single source and revisit in 30 days.

## Logging searches

When you find a genuinely new source type or a useful query pattern — especially a local-language query that unlocked a difficult record — append it to `common-mistakes.md`. The playbook gets smarter over time. Significant patterns get promoted into this file.
