# NZIPL Claude Kit

Shared knowledge base for the Net Zero Industrial Policy Lab team using Claude Code. Clone this repo and Claude Code picks up the context automatically.

## What this does

Every Claude Code session opened from this repo loads `CLAUDE.md`, which contains the Lab's data sources, API references, deliverable standards, and pipeline conventions. The design skill (`/nzipl-design`) applies the CICE visual identity to any output format. The glossary and gotchas files prevent the team from rediscovering the same issues independently.

## Contents

| File | Purpose |
|------|---------|
| `CLAUDE.md` | Lab context: data sources, sprint structure, API auth patterns, deliverable standards |
| `glossary.md` | 31 acronyms and 22 internal terms used across the Lab's work |
| `gotchas.md` | 11 documented data/API issues that cause silent failures, with workarounds |
| `discoveries.md` | Running log of team-contributed findings (append-only) |
| `CONTRIBUTING.md` | How to add to this kit |
| `.claude/skills/nzipl-design/` | Design system skill: tokens, HTML patterns, chart styles, PPTX layouts |
| `.claude/commands/` | Reusable prompts for common tasks |
| `tasks/` | Structured task definitions |

## Setup

```bash
git clone https://github.com/Gilix/nzipl-claude-kit.git
cd nzipl-claude-kit
```

Open Claude Code. The context loads on session start. Run `/nzipl-design` to verify the skill is available.

## Contributing

**Low friction**: Append a one-liner to `discoveries.md` and push. No PR needed.

**Structured changes**: Glossary terms, gotcha write-ups, design system updates, and CLAUDE.md edits go through PRs. See `CONTRIBUTING.md` for details.

## What belongs here vs. elsewhere

**Here**: Data source references, API behaviors, naming conventions, design tokens, methodology vocabulary, tooling patterns. Anything a teammate's Claude session should know.

**Not here**: Project-specific file paths, personal workflow preferences, API keys, contract details, or scoring methodology. Those stay in individual repos or local memory.
