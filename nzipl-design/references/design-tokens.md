# NZIPL Design Tokens

Single source of truth for all visual values. Light theme with forest green (#063309) brand accent, matching the published NZIPL brief identity. Archivo typeface.

## Table of Contents
1. [Color System](#color-system)
2. [Typography](#typography)
3. [Spacing and Layout](#spacing-and-layout)
4. [Borders and Radii](#borders-and-radii)
5. [Shadows](#shadows)
6. [Breakpoints](#breakpoints)
7. [Google Fonts Link](#google-fonts-link)

---

## Color System

### Surface Colors (Light Theme)

| Token | Hex | Usage |
|-------|-----|-------|
| `bg-body` | `#FFFFFF` | Page/slide background |
| `bg-section` | `#F5F6F4` | Alternating section backgrounds, panel areas |
| `bg-card` | `#FFFFFF` | Cards, paper, panels (on section bg) |
| `bg-input` | `#EDEEEC` | Input fields, recessed surfaces |
| `bg-elevated` | `#FFFFFF` | Hover/active cards |

### Text Colors

| Token | Hex | Usage |
|-------|-----|-------|
| `text-heading` | `#063309` | All headings, brand accent text |
| `text-body` | `#303030` | Body text, paragraphs, table values |
| `text-dimmed` | `#666666` | Subtitles, labels, toolbar text |
| `text-muted` | `#888888` | Source notes, axis text, footnotes |
| `text-faint` | `#AAAAAA` | Disabled, placeholder |

### Brand Green Scale

| Token | Hex | Usage |
|-------|-----|-------|
| `brand-0` | `#E8F3EA` | Lightest tint (highlight bg, hover) |
| `brand-1` | `#C5E5CA` | Light background fills |
| `brand-2` | `#8DD097` | Subtle accent fills |
| `brand-3` | `#4DB55A` | Light positive accent |
| `brand-4` | `#2CA03E` | Downstream stage, positive indicator |
| `brand-5` | `#1A6632` | Midstream stage, lighter brand accent |
| `brand-6` | `#0E4A13` | Hover/pressed on brand elements |
| `brand-7` | `#063309` | Primary brand - headings, links, accents |
| `brand-8` | `#042606` | Figure captions (H4) |
| `brand-9` | `#021A04` | Darkest (rare) |

### Figure Palette

#### Style A: Clean Institutional (default)

Used for radar charts, simple bar/line charts, country comparisons.

| Token | Hex | Usage |
|-------|-----|-------|
| `teal` | `#6B9E9E` | Primary chart fill, radar polygons |
| `steel-blue` | `#4E8CA8` | Secondary fill |
| `amber` | `#D4A34A` | Warm accent, paired radar |

#### Style B: Warm Analytical (supply chain data)

Used for value chain visualizations, trade flow charts, treemaps.

| Token | Hex | Usage |
|-------|-----|-------|
| `pull-amber` | `#B85900` | Pull quotes, primary warm accent |
| `brown` | `#8A4200` | Upstream/extraction |
| `orange` | `#CB5B1D` | Final product stage |
| `gold` | `#D4A34A` | Warm neutral |
| `steel-blue-contrast` | `#1B6CA8` | Cool contrast (sparingly) |
| `grey-green` | `#5B7266` | Neutral |

#### Supply Chain Stage Colors

| Stage | Hex | Semantic |
|-------|-----|----------|
| Upstream | `#8A4200` | Brown (earth, extraction) |
| Midstream | `#1A6632` | Forest green (processing) |
| Downstream | `#2CA03E` | Bright green (assembly) |
| Final Product | `#CB5B1D` | Orange (finished goods) |

#### Technology Colors

| Technology | Hex |
|------------|-----|
| Batteries | `#1A6632` |
| Biofuel | `#5C8A00` |
| Electrolyzers | `#1B6CA8` |
| Geothermal | `#8B2500` |
| Heat Pumps | `#C17A2E` |
| Magnets | `#4A4580` |
| Nuclear | `#4A7C59` |
| Solar | `#E87722` |
| Transmission | `#607080` |
| Wind | `#1A8C28` |

#### Categorical (6-color, for multi-play comparisons)

| Index | Color | Hex |
|-------|-------|-----|
| 0 | Teal | `#6B9E9E` |
| 1 | Steel Blue | `#1B6CA8` |
| 2 | Amber | `#D4A34A` |
| 3 | Brown | `#8A4200` |
| 4 | Orange | `#CB5B1D` |
| 5 | Grey-green | `#5B7266` |

### Functional Colors

| Token | Hex | Context |
|-------|-----|---------|
| `positive` | `#2CA03E` | Growth, advantage, RCA > 1 |
| `negative` | `#C87654` | Decline, deficit |
| `warning` | `#B85900` | Attention, pull quotes |
| `info` | `#1B6CA8` | Informational, reference lines |
| `border` | `#D0D0D0` | Card borders, dividers, grid lines |
| `border-subtle` | `#E8E8E8` | Inner dividers, subtle rules |

### Chart Color Scales

#### Sequential (single-hue, for choropleths and heatmaps)
Green scale for positive metrics (RCA, relatedness density):
```
['#E8F3EA', '#C5E5CA', '#8DD097', '#4DB55A', '#2CA03E', '#1A6632', '#063309']
```

#### Diverging (values above/below a threshold)
Red-to-green through neutral grey:
```
['#C87654', '#D4A090', '#E0C8BC', '#D0D0D0', '#8DD097', '#4DB55A', '#1A6632']
```

---

## Typography

### Font Stack

| Role | Family | Weight | Fallbacks |
|------|--------|--------|-----------|
| Headings | Archivo | 600-700 | Calibri, -apple-system, sans-serif |
| Body text | Archivo | 300 (Light) | Calibri Light, sans-serif |
| Intro/emphasis | Archivo | 500 (Medium) | Calibri, sans-serif |
| Labels/UI | Archivo | 400 (Regular) | Calibri, sans-serif |
| Code/Data | JetBrains Mono | 400 | Consolas, monospace |

Archivo is used for all text. Headings are distinguished by weight (600-700) and color (#063309), not by a separate typeface. Body text uses weight 300 (Light) matching the published briefs.

### Type Scale

| Element | Size | Weight | Line-height | Color |
|---------|------|--------|-------------|-------|
| Page title (h1) | 2.5rem (40px) | 300 | 1.2 | `#063309` |
| Section heading (h2) | 1.625rem (26px) | 700 | 1.3 | `#063309` |
| Subsection (h3) | 1.25rem (20px) | 400 | 1.3 | `#063309` |
| h4 (figure caption) | 1rem (16px) | 400 italic | 1.05 | `#042606` |
| h5 | 1rem (16px) | 600 | 1.4 | `#063309` |
| h6 | 0.875rem (14px) | 600 | 1.4 | `#063309` |
| Body text (md) | 1rem (16px) | 300 | 1.55 | `#303030` |
| Small body (sm) | 0.875rem (14px) | 300 | 1.5 | `#303030` |
| Intro text | 1.125rem (18px) | 500 | 1.5 | `#063309` |
| Caption/label (xs) | 0.75rem (12px) | 400 | 1.5 | `#666666` |
| Source note | 0.75rem (12px) | 300 | 1.5 | `#888888` |
| Button text | 0.875rem (14px) | 500 | 1 | varies |
| Chart axis tick | 0.75rem (12px) | 400 | 1 | `#303030` |
| Pull quote | 1.25rem (20px) | 600 italic | 1.4 | `#B85900` |

---

## Spacing and Layout

### Spacing Scale

| Token | Value | Usage |
|-------|-------|-------|
| `xs` | 0.5rem (8px) | Icon gaps, tight inline spacing |
| `sm` | 0.75rem (12px) | Button padding, legend gaps |
| `md` | 1rem (16px) | Card padding, control gaps |
| `lg` | 1.5rem (24px) | Section padding, panel padding |
| `xl` | 2rem (32px) | Major section spacing |

### Container Widths

| Size | Max-width |
|------|-----------|
| xs | 540px |
| sm | 720px |
| md | 960px |
| lg | 1140px |
| xl | 1320px |

### Grid Patterns

Dashboard grid: `display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;`
Metric cards: `display: flex; gap: 1rem; flex-wrap: wrap;`
Toolbar: `display: flex; flex-wrap: wrap; gap: 0.75rem; align-items: center;`

---

## Borders and Radii

### Border Radius

| Token | Value | Usage |
|-------|-------|-------|
| `xs` | 0.25rem (4px) | Buttons, badges |
| `sm` | 0.375rem (6px) | Small cards, tooltips |
| `md` | 0.5rem (8px) | Cards, paper, panels (default) |
| `lg` | 0.75rem (12px) | Large containers |
| `xl` | 1rem (16px) | Hero sections |

Default for cards and paper: `md` (0.5rem).

### Border Styles

| Element | Border |
|---------|--------|
| Card/paper | 1px solid `#D0D0D0` |
| Active element | 1px solid `#063309` |
| Subtle divider | 1px solid `#E8E8E8` |
| Section divider | 1px solid `#D0D0D0` |

---

## Shadows

| Token | Value | Usage |
|-------|-------|-------|
| `sm` | `0 1px 3px rgba(0,0,0,0.08), 0 1px 2px rgba(0,0,0,0.06)` | Cards, paper (default) |
| `md` | `0 4px 6px rgba(0,0,0,0.07)` | Elevated elements |
| `tooltip` | `0 2px 8px rgba(0,0,0,0.12)` | Tooltips, popovers |

---

## Breakpoints

| Name | Width | Changes |
|------|-------|---------|
| xs | < 576px | Single column, stacked controls |
| sm | >= 576px | 540px container |
| md | >= 768px | Two-column grid, side-by-side charts |
| lg | >= 992px | Full toolbar, sidebar panels |
| xl | >= 1200px | 1140px container |
| xxl | >= 1400px | 1320px container |

---

## Font Installation

Archivo must be installed locally for PPTX rendering, matplotlib chart generation, and Word documents. HTML deliverables load Archivo from Google Fonts and do not require local installation.

### Install Archivo (required before first use)

Run this Python snippet to download and install all Archivo weights:

```python
import os, urllib.request, matplotlib.font_manager as fm

FONT_DIR = os.path.expanduser('~/Library/Fonts')  # macOS; use ~/.local/share/fonts on Linux
os.makedirs(FONT_DIR, exist_ok=True)

WEIGHTS = {
    'Light': 'https://fonts.gstatic.com/s/archivo/v25/k3k6o8UDI-1M0wlSV9XAw6lQkqWY8Q82sJaRE-NWIDdgffTTajNp8A.ttf',
    'Regular': 'https://fonts.gstatic.com/s/archivo/v25/k3k6o8UDI-1M0wlSV9XAw6lQkqWY8Q82sJaRE-NWIDdgffTTNDNp8A.ttf',
    'Medium': 'https://fonts.gstatic.com/s/archivo/v25/k3k6o8UDI-1M0wlSV9XAw6lQkqWY8Q82sJaRE-NWIDdgffTTBjNp8A.ttf',
    'SemiBold': 'https://fonts.gstatic.com/s/archivo/v25/k3k6o8UDI-1M0wlSV9XAw6lQkqWY8Q82sJaRE-NWIDdgffTT6jRp8A.ttf',
    'Bold': 'https://fonts.gstatic.com/s/archivo/v25/k3k6o8UDI-1M0wlSV9XAw6lQkqWY8Q82sJaRE-NWIDdgffTT0zRp8A.ttf',
}

for name, url in WEIGHTS.items():
    dest = os.path.join(FONT_DIR, f'Archivo-{name}.ttf')
    if not os.path.exists(dest):
        urllib.request.urlretrieve(url, dest)
        print(f'Installed: Archivo-{name}.ttf')
    fm.fontManager.addfont(dest)

print('Archivo installed. Restart any open applications to pick up the new fonts.')
```

After installation, restart Word/PowerPoint to pick up the new fonts. For matplotlib, call `fm.fontManager.addfont()` at the top of any script (as shown above) or clear the font cache (`~/.matplotlib/fontlist-*.json`).

### Google Fonts Link (HTML only)

Include this in every HTML deliverable's `<head>`:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@300;400;500;600;700&display=swap" rel="stylesheet">
```

For deliverables that also use code/data display:
```html
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400&display=swap" rel="stylesheet">
```
