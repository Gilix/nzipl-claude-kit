# DataMexico API Skill

A Claude Code skill that turns Claude into an expert on the DataMexico API — Mexican government's economic data platform via `economia.gob.mx`. Auto-triggers when Claude needs to query Mexican subnational data (DENUE manufacturing employment, AMPIP industrial parks, INEGI economic census, municipality HS4 trade, ECI/PCI by Mexican state, FDI, CONEVAL poverty, etc.).

## What's in this folder

```
datamexico-api/
├── SKILL.md              ← Decision tree + hard rules (the skill entry file)
├── references/
│   ├── endpoints.md      ← URL families, params, response shape, multi-month workaround
│   ├── cubes.md          ← 14 most-used cubes with full request examples
│   ├── gotchas.md        ← 12 known traps with traceable incidents and workarounds
│   ├── patterns.md       ← 8 stdlib-only Python templates for common queries
│   └── pipelines.md      ← Pointers to canonical production pipelines + their caches
└── README.md             ← This file
```

Total: ~54 KB of curated DataMexico expertise distilled from production pipelines that have been debugged against real data.

## Why this skill exists

DataMexico is the canonical source for Mexican subnational data — state, municipality, and metro-area cuts that OEC's Mexico cube does not cover at the same depth. But the API has several silent traps: the `/data` endpoint drops manufacturing sectors from DENUE, HS4 IDs include a chapter prefix that breaks naive joins, state names need three different normalization maps depending on the consuming dataset, etc.

Each trap has been hit at least once in production. This skill consolidates the workarounds so the next person writing a Mexico pipeline doesn't rediscover them.

## Install

To activate the skill in a Claude Code project:

1. Copy this folder into the project's skills directory:
   ```
   cp -R datamexico-api /path/to/your/project/.claude/skills/
   ```
   (Or if you don't have a project-level `.claude/skills/`, use `~/.claude/skills/` for user-level activation across all projects.)

2. Restart your Claude Code session, or run `/skills` to confirm `datamexico-api` is loaded.

3. The skill auto-triggers when you ask Claude about DataMexico, DENUE, AMPIP parks, ECI/PCI Mexico, specific cube names, or any Mexican subnational data query. No explicit invocation required.

## Authoring conventions

If you extend this skill, please follow the conventions baked into the existing pipelines:

- **Stdlib-only Python** in code examples (`urllib.request`, `json`, `pathlib`). No `requests`, `pandas`, `httpx`. Matches every existing DataMexico pipeline in the GripPoint kit.
- **Trace gotchas to incidents.** Each gotcha entry should cite which pipeline discovered it, so future readers know *why* the rule exists and can judge edge cases.
- **Cache-first pattern.** Examples should write `*_cache.json` next to the script and ship a `--skip-api` flag.
- **Don't duplicate the master catalog.** The 96-cube full catalog lives in user memory at `~/.claude/projects/-Users-gilbertogarcia-Desktop-GripPoint/memory/reference_datamexico_api.md`. This skill curates only the cubes that show up in real work — link to the master for the long tail.

## Provenance

The skill's content is distilled from production pipelines in the GripPoint repo:

- `projects/nzipl/data/nzipl_denue_pipeline.py` — DENUE multi-month workaround
- `projects/nzipl/data/compute_municipality_rca.py` — HS4 chapter-prefix extraction
- `projects/nzipl/data/nzipl_parks_pipeline.py` — AMPIP parks + state name normalization (3-map strategy) + Nominatim 3-tier geocoding
- `intelligence/data/datamexico_dashboard_pipeline.py` — Multi-cube dashboard pattern
- `projects/acapulco/data/acapulco_pipeline.py` — Metro-area drilldown
- `projects/juarez-elpaso/data/fetch_*.py` — City-level patterns

If you find a new gotcha or a useful cube combination, contribute it back via the kit's standard process (see `nzipl-claude-kit/CONTRIBUTING.md`).

## License

Internal NZIPL Lab tooling. Same license as the parent kit.
