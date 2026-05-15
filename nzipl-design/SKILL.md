---
name: nzipl-design
description: "Apply the NZIPL visual identity to HTML deliverables (scrollytelling, dashboards, interactive maps), PPTX slide decks, and data visualizations. Light theme with Archivo typeface and forest green (#063309) brand accent, matching the published NZIPL brief identity. Use whenever creating or formatting deliverables for NZIPL/JHU, or when the user mentions NZIPL style, Lab style, play cards, constraint maps, scrollytelling, or any visualization that should match the Lab's design system. Also trigger for 'like the play cards', 'in the Lab style', or 'brief style'. Covers D3.js and Chart.js chart styling, Leaflet map theming, PPTX slide layout, and the full token system."
---

# NZIPL Design System Skill

This skill applies the Net Zero Industrial Policy Lab visual identity to deliverables. The design system matches the published NZIPL brief identity: light backgrounds, Archivo typeface, forest green (#063309) brand accent, and the institutional figure palette (teal/amber/stage colors).

## When to use this skill

Apply this system to any deliverable produced for NZIPL or that the user wants styled in the Lab's visual language. The three primary output formats are:

1. **HTML scrollytelling** (play cards, constraint maps, briefing dashboards)
2. **HTML interactive maps** (Leaflet-based infrastructure/choropleth overlays)
3. **PPTX slide decks** (presentations, briefings, summaries)

## How to use this skill

### Step 1: Identify the output format

| User says | Format | Reference to read |
|-----------|--------|-------------------|
| "play card", "scrollytelling", "briefing page" | HTML scrollytelling | `references/html-patterns.md` |
| "dashboard", "interactive dashboard" | HTML dashboard | `references/html-patterns.md` |
| "map", "infrastructure map", "choropleth" | HTML Leaflet map | `references/html-patterns.md` |
| "deck", "slides", "presentation", "pptx" | PPTX (template-based) | `references/pptx-styles.md` |
| "chart", "visualization", "graph" | Embedded viz | `references/chart-styles.md` |

### Step 2: Read the design tokens

**Always read `references/design-tokens.md` first.** It contains every color, font, spacing, and radius value. The tokens are the single source of truth.

### Step 3: Read the format-specific reference

Read the reference file(s) matching the output format. Most deliverables need both the format reference and the chart styles reference.

### Step 4: Apply the system

Follow the patterns in the reference files. Key principles:

**Light background, green headings.** Body background is white (`#FFFFFF`). Cards and panels use white with subtle borders or `#F5F6F4` section backgrounds. Headings use `#063309` (NZIPL forest green). Body text is `#303030`.

**Archivo for everything.** One typeface family, differentiated by weight. Headings: 600-700. Body: 300 (Light). Intro/emphasis: 500 (Medium). Labels: 400 (Regular). Load from Google Fonts in every HTML deliverable with weights 300-700.

**Forest green brand accent.** Primary accent is `#063309`. Used for headings, links, section markers, active states. Lighter greens (`#1A6632`, `#2CA03E`) for chart fills and positive indicators. Amber (`#B85900`) for pull quotes and warm highlights.

**Clean institutional figure palette.** Charts use teal (`#6B9E9E`) as default fill, amber (`#D4A34A`) as warm accent, and the supply chain stage colors (brown/green/orange) for value chain visualizations. White chart backgrounds, `#D0D0D0` grid lines, `#888888` axes.

**Minimal chrome.** Cards use `border: 1px solid #D0D0D0` and subtle shadows. No heavy borders or decoration. Tables use thin horizontal rules only.

**Attribution footer.** All deliverables include: "Net Zero Industrial Policy Lab | Johns Hopkins University | netzeropolicylab.com"

## File structure

```
nzipl-design/
  SKILL.md                          <- You are here
  references/
    design-tokens.md                 <- Colors, typography, spacing, radii (single source of truth)
    html-patterns.md                 <- Scrollytelling, dashboard, and map CSS/HTML patterns
    chart-styles.md                  <- D3.js and Chart.js styling (axes, tooltips, legends, color scales)
    pptx-styles.md                   <- Template-based PPTX generation (layout map, placeholder filling)
    NZIPL_PPT_Template_v1.potx       <- Official NZIPL PowerPoint template (28 layouts, all backgrounds/logos)
```

## Related skills

- `nzipl-brief`: Word document briefs (.docx) using the same visual identity for print
- `editor`: Developmental editing for academic and policy writing
