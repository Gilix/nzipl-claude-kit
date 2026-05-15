# Verification protocol

`verificationTier` is the most load-bearing field. Tier inflation is the most common failure. The validator enforces the matrix below.

## Tier matrix

| Tier | Required evidence | Min distinct citation URLs |
|------|-------------------|----|
| 1 Confirmed | Primary (company PR / govt filing / SEC / regulatory disclosure) + corroborator (permit / named-author trade coverage / equipment-vendor announcement) + independent news | 3 |
| 2 Likely | Company announcement + one top-tier independent, OR two independent top-tier named-authors | 2 |
| 3 Announced-only | Single source | 1 |

Syndication of one press release = one source, not three. A Reuters pickup of a company PR plus the original PR plus a translation is one substantive claim with three URLs — fails Tier 1's "three independent" requirement.

## Status × tier (enforced)

| Status | Required tier |
|--------|--------------|
| Operating | 1 |
| Under Construction | 1 |
| Closed | 1 |
| Rumored | 3 |
| Planned / Announced / Paused / Cancelled | any |

Invalid pair → fix tier (add sources) or status (downgrade), not both.

## Disambiguation

Every source must distinguish the specific facility — by city, permit ID, groundbreaking date, capacity, or product line. Drop a tier when sources conflate sister plants. High-ambiguity operators by tech:

- **Solar**: First Solar (multiple US sites: Ohio, Alabama, Louisiana), JinkoSolar (Vietnam, Florida, Jacksonville), LONGi (multiple Southeast Asia + Malaysia). Distinguish by state, not just country.
- **Wind**: Vestas (multiple US blade and tower plants — Brighton CO, Pueblo CO, Windsor CO), Siemens Gamesa (offshore vs onshore lines), Goldwind (multiple Xinjiang and Inner Mongolia).
- **Hydrogen**: Plug Power (Genfuel network — Rochester NY, Camden GA, Vista CA, Louisiana Hydrogen Hub all simultaneously announced), ITM Power (Sheffield + Bessemer City NC), Nel (Heroya + Wallingford CT). Cross-check by GW capacity.
- **Heat pumps**: Daikin (multiple US sites + EU contract manufacturers), Mitsubishi Electric (multiple Asia + Tennessee).

## Paywalls

Tier-1 citations allowed only if a free mirror exists. Cite the mirror URL. No mirror = source is invisible.

## Conflicting sources

| Disagreement | Resolution |
|--------------|-----------|
| Two investment figures | Most recent → `investmentM`; earlier → `investmentM_history`. |
| Company says "Operating", independent says "delayed" | Trust independent; downgrade status. |
| Company says "Cancelled", independent says "Paused" | Trust company. |
| Different dates | Use most precise; note ambiguity. |
| Capacity stated in different units | Convert to canonical unit per `schema.md` projectType matrix; preserve original in `product`. |

Never silently average. Hydrogen capacity in particular often appears as both "input MW" and "output kt-H2/year"; record one and note the conversion source in `product`.

## Re-verification

Records decay. On every re-touch:
- Update `verifiedDate`.
- Evidence stronger → upgrade tier, add URLs.
- Evidence weaker → downgrade tier or status.
- Value changed → append to `investmentM_history`; update `investmentM` headline.

Hydrogen records decay fastest — many MOU-stage announcements collapse within 18 months. Solar polysilicon next. Heat pumps and wind typically decay slower.
