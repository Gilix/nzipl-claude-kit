# Cubes Reference (Production-Curated)

The DataMexico catalog is 96 cubes. The full list lives at `~/.claude/projects/-Users-gilbertogarcia-Desktop-GripPoint/memory/reference_datamexico_api.md` — go there for any cube not on this page. This page documents the 14 cubes that show up in real GripPoint pipelines, with full working request examples.

For each cube: what it answers, drilldowns, measures, endpoint, a copyable URL, and the response field shape.

---

## `inegi_denue` — Business registry (employment by geography × industry)

**Answers**: How many establishments and how many employees are in each combination of state/municipality × SCIAN industry?

**Source**: INEGI's DENUE (Directorio Estadístico Nacional de Unidades Económicas), updated multi-annually.

**Drilldowns**: `State`, `Municipality`, `Metro Area`, `National Industry` (SCIAN 2/3/4/6-digit), `Company Size`, `Number of Employees Midpoint`, `Date` / `Month`, `Sector`.

**Measures**: `Companies`, `Employees LCI`, `Employees Midpoint`, `Employees UCI` (lower/midpoint/upper confidence interval).

**Endpoint**: `/stats/rca` for industry-by-geography (avoids manufacturing drop). `/data` only when manufacturing isn't relevant.

**Working request** (state × industry employment, multi-month, full sector coverage):

```
https://www.economia.gob.mx/datamexico/api/stats/rca
  ?cube=inegi_denue
  &Month=20250522,20241126,20240523
  &rca=State,National Industry,Number of Employees Midpoint
  &threshold=National Industry:900,State:900
  &locale=es
  &parents=true
```

**Response fields**: `State`, `State ID`, `National Industry`, `National Industry ID`, `Sector`, `Sector ID` (manufacturing is `"31-33"`), `Number of Employees Midpoint`, plus RCA and share fields.

**Critical**: see gotcha #1 in `gotchas.md`. Single-month `/data` queries silently drop SCIAN 31-33, 43, 51, 54.

---

## `economy_foreign_trade_mun` — Municipality trade (HS4 detail)

**Answers**: How much does each municipality export/import, broken down by HS4 product? Year-level granularity.

**Source**: Secretaría de Economía aggregation of municipal customs data.

**Drilldowns**: `Municipality`, `State`, `HS4`, `HS6` (where available), `Year` / `Date Year`, `Country` (limited).

**Measures**: `Trade Value`.

**Endpoint**: `/data`.

**Working request** (all municipalities × HS4 × exports × 2023–2024):

```
https://www.economia.gob.mx/datamexico/api/data
  ?cube=economy_foreign_trade_mun
  &drilldowns=Municipality,HS4
  &measures=Trade Value
  &Flow=2
  &Date Year=2023,2024
  &parents=true
```

`Flow=2` is exports; `Flow=1` is imports.

**Response fields**: `Municipality`, `Municipality ID`, `State`, `State ID`, `HS4`, `HS4 ID`, `Trade Value`.

**Critical**: see gotcha #2. `HS4 ID` includes a chapter prefix (e.g., `20702` is chapter 2 + HS4 0702). Extract last 4 digits.

---

## `economy_foreign_trade_ent` — State trade (HS6 detail with country)

**Answers**: State-level exports/imports with HS6 product detail and partner country breakdown.

**Drilldowns**: `Geography` (state), `Flow`, `Year` / `Date`, `HS2` / `HS4` / `HS6`, `Country`.

**Measures**: `Trade Value`.

**Endpoint**: `/data`.

**Working request** (Nuevo León EV components 2024 by partner):

```
https://www.economia.gob.mx/datamexico/api/data
  ?cube=economy_foreign_trade_ent
  &drilldowns=Geography,HS6,Country
  &measures=Trade Value
  &Flow=2
  &Year=2024
  &Geography=19
  &parents=true
```

State IDs follow INEGI's 2-digit code (e.g., `19` is Nuevo León). Use `parents=true` to get state name + ID together.

---

## `economy_foreign_trade_nat` — National trade (broadest cube)

**Answers**: National-level exports/imports, HS2/4/6, by country and date.

**Drilldowns**: `Flow`, `HS2` / `HS4` / `HS6`, `Country`, `Year` / `Date`.

**Measures**: `Trade Value`.

**Endpoint**: `/data`.

Use this when you don't need subnational detail. For monthly seasonality, drill to `Date` instead of `Year`.

---

## `complexity_eci` — ECI by geography

**Answers**: Economic Complexity Index for a Mexican entity (state, metro, municipality) over time.

**Drilldowns**: `Nation`, `Level`, `Geography State` / `Geography Metro Area` / `Geography Municipality`, `Date Day`, `Latest`.

**Measures**: `ECI`, `ECI Ranking`.

**Endpoint**: `/data`.

**Working request** (latest ECI for all states):

```
https://www.economia.gob.mx/datamexico/api/data
  ?cube=complexity_eci
  &drilldowns=Geography State
  &measures=ECI,ECI Ranking
  &Latest=true
  &parents=true
```

Drop `Latest=true` and add `Date Day` to get a time series.

---

## `complexity_pci` — PCI by industry

**Answers**: Product Complexity Index for SCIAN industries.

**Drilldowns**: `National Industry`, `Date Day`, `Latest`.

**Measures**: `PCI`, `PCI Ranking`.

**Endpoint**: `/data`.

Pair with `complexity_eci` for a Mexican subnational ECI/PCI dual view that doesn't exist in OEC.

---

## `inegi_economic_census` — Industry structure (90+ measures per industry × geography)

**Answers**: Production, employment, wages, capex, expenses, fixed assets — extremely deep industry structure data per municipality, every 5 years.

**Drilldowns**: `Industry 6 Digit` (SCIAN), `Geography`, `Year` (2009, 2014, 2019, 2024 census waves).

**Measures**: 90+, including `Total Production`, `Total Personnel`, `Wages and Salaries`, `Gross Capital Formation`, `Total Expenses`, etc. See cube metadata at `/tesseract/cubes/inegi_economic_census` for the full list.

**Endpoint**: `/data`.

**Working request** (transportation equipment manufacturing by municipality, 2019):

```
https://www.economia.gob.mx/datamexico/api/data
  ?cube=inegi_economic_census
  &drilldowns=Geography,Industry 6 Digit
  &measures=Total Personnel,Wages and Salaries,Total Production
  &Industry 6 Digit=336111
  &Year=2019
  &parents=true
```

For the 2014 census specifically there are dedicated cubes (`inegi_economic_census_2014_mun`, `inegi_economic_census_2014_ent`) with the same shape.

---

## `industrial_parks` — AMPIP industrial parks registry

**Answers**: List of registered industrial parks in Mexico with state and municipality, count per municipality.

**Source**: AMPIP (Asociación Mexicana de Parques Industriales Privados).

**Drilldowns**: `State`, `Municipality`, `Industrial Parks`.

**Measures**: `Parks` (count, always 1 per row in practice).

**Endpoint**: `/tesseract/data.jsonrecords` (the form `nzipl_parks_pipeline.py` uses) or `/data` (also works).

**Working request**:

```
https://www.economia.gob.mx/apidatamexico/tesseract/data.jsonrecords
  ?cube=industrial_parks
  &drilldowns=State,Municipality,Industrial Parks
  &measures=Parks
```

**Response fields**: `Industrial Parks ID`, `Industrial Parks` (park name), `Municipality`, `Municipality ID`, `State`, `State ID`, `Parks`.

**Critical**: AMPIP records have **no lat/lng**. Geocode separately. The production fallback ladder is (1) Nominatim with park name, (2) Nominatim with `"parque industrial, <muni>, <state>"`, (3) municipality centroid from the GeoJSON. See `nzipl_parks_pipeline.py`.

---

## `economy_fdi` and the FDI family (16 cubes)

**Answers**: Foreign Direct Investment movements by state, industry, country of origin, investment type, year/quarter. The FDI surface is split across 16 cubes that pre-aggregate different combinations to keep response sizes small.

**Most useful in this family**:

| Cube | Drilldowns | Use for |
|------|-----------|---------|
| `fdi_year_state_industry` | Geography, Year, FDI Industry (2/3/4-digit) | "FDI by state and industry per year" |
| `fdi_year_industry_country` | FDI Industry, Year, Country Origin | "Where does FDI in industry X come from" |
| `fdi_3_country_origin` | Geography, Year, Country Origin | "Top countries investing in state X" |
| `fdi_4_investment_type` | Investment Type, Geography, Year, Country Origin | "New vs reinvested capital by state" |
| `economy_fdi` | Investment Type, Industry, Geography, Date, Origin Country | The general/most flexible FDI cube |

**Endpoint**: `/data`.

**Measures**: `Investment` (USD), `Count` (number of projects).

**Working request** (FDI to Nuevo León by industry, 2020–2024):

```
https://www.economia.gob.mx/datamexico/api/data
  ?cube=fdi_year_state_industry
  &drilldowns=Year,FDI Industry
  &measures=Investment,Count
  &Geography=19
  &Year=2020,2021,2022,2023,2024
  &parents=true
```

Note: `FDI Industry` is its own taxonomy (not SCIAN). Drilldown levels are 2/3/4-digit.

---

## `coneval_poverty` — Poverty and deprivation by municipality

**Answers**: Poverty headcount, extreme poverty, six deprivation indicators, welfare line — by year and geography.

**Drilldowns**: `Year` (CONEVAL waves: 2010, 2015, 2020, 2022...), `Geography`.

**Measures**: `Population`, `Poverty`, `Extreme Poverty`, `Moderate Poverty`, `Vulnerable by Lacks`, `Vulnerable by Income`, six deprivation types (education, health access, social security, housing quality, basic services, food access), `Welfare Line`.

**Endpoint**: `/data`.

**Working request** (state-level poverty 2022):

```
https://www.economia.gob.mx/datamexico/api/data
  ?cube=coneval_poverty
  &drilldowns=Geography
  &measures=Population,Poverty,Extreme Poverty
  &Year=2022
  &parents=true
```

Pair with `coneval_gini_mun` for inequality.

---

## `coneval_gini_mun` — Gini coefficient by municipality

**Drilldowns**: `Geography` (municipality), `Year`.

**Measures**: `GINI`, `Income Rate`.

**Endpoint**: `/data`.

For state-level: `coneval_gini_ent`. For national: `coneval_gini_nat`.

---

## `inegi_enoe` — Labor force (workforce, hours, wages)

**Answers**: Labor force participation, employment formality, wages, hours, by demographics and industry — quarterly survey.

**Drilldowns**: `Job Situation`, `Schooling`, `Formality`, `Age Group`, `Geography`, `Industry`, `Sex`, `Date` (quarter), `Occupation`.

**Measures**: `Records`, `Workforce`, `Hours`, `Days`, `Monthly Wage`, `Workforce MOE`.

**Endpoint**: `/data`.

For establishments-side data ("how many workers do firms report") prefer `inegi_denue` + `inegi_economic_census`. For households-side ("who is working, what do they earn") use `inegi_enoe`.

---

## `banxico_mun_income_remittances` — Municipal remittance flows

**Answers**: USD remittance amount received by municipality, by quarter.

**Drilldowns**: `Geography Municipality`, `Time` (quarter).

**Measures**: `Remittance Amount`.

**Endpoint**: `/data`.

Useful as a household-income proxy that complements `coneval_poverty`. Some Mexican states (Michoacán, Guanajuato, Oaxaca) get >5% of state GDP from remittances.

---

## `inegi_gdp` — National GDP by sector

**Drilldowns**: `Sector`, `Date`.

**Measures**: `GDP`.

**Endpoint**: `/data`.

For state-level GDP look at `inegi_economic_census` `Total Production` aggregated by state, since DataMexico does not expose a clean state-GDP cube.

---

## Cubes NOT on this page

The following are in the 96-cube catalog but rarely needed and not documented here. Look them up in the master catalog when needed:

- COVID-19 cubes (`gobmx_covid*`, `covid_population_projection`)
- T-MEC/USMCA aggregates (`T_MEC_*`) — useful for value-chain framing but limited subnational depth
- Investment announcements (`Anuncios_Inversion_*`)
- IMPI intellectual property (`impi_*`)
- INFONAVIT housing finance (`infonavit_*`)
- Education / health / security (ANUIES, `health_*`, `sesnsp_crimes`)
- Population (`inegi_population*`, `conapo_metro_area_population`)
- Income surveys (`inegi_enigh_*`)
- Agricultural prices (`sniim_products`)
- BACI bilateral (`trade_i_baci_a_12` — prefer querying via OEC)

→ Master catalog: `~/.claude/projects/-Users-gilbertogarcia-Desktop-GripPoint/memory/reference_datamexico_api.md`

## Discovering a cube's exact dimensions and measures

If a cube isn't in this list and you need its full schema, query its metadata endpoint:

```
https://www.economia.gob.mx/apidatamexico/tesseract/cubes/<cube_name>
```

Returns the full Tesseract definition: dimensions (with hierarchies), measures, named sets, default sort, source attribution.
