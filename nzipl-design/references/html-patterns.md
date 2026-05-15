# NZIPL HTML Patterns

CSS and HTML patterns for scrollytelling, dashboards, and Leaflet maps. Light theme with Archivo typeface, forest green (#063309) brand accent, matching the published NZIPL brief identity.

## Table of Contents
1. [Shared HTML Boilerplate](#shared-html-boilerplate)
2. [Scrollytelling Play Cards](#scrollytelling-play-cards)
3. [Interactive Dashboards](#interactive-dashboards)
4. [Leaflet Maps](#leaflet-maps)
5. [Common Components](#common-components)

---

## Shared HTML Boilerplate

Every NZIPL HTML deliverable starts with this structure:

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>[Title] — NZIPL</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<!-- Additional CDN links (D3, Leaflet, Chart.js, etc.) go here -->
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  font-family: 'Archivo', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: #FFFFFF;
  color: #303030;
  font-weight: 300;
  line-height: 1.55;
}
h1, h2, h3, h4, h5, h6 {
  font-family: 'Archivo', sans-serif;
  color: #063309;
}
h1 { font-weight: 300; }
h2 { font-weight: 700; }
h3 { font-weight: 400; }
h4 { font-weight: 400; font-style: italic; color: #042606; }
h5, h6 { font-weight: 600; }
a { color: #063309; text-decoration: none; }
a:hover { color: #0E4A13; text-decoration: underline; }
</style>
</head>
<body>
<!-- Content -->
</body>
</html>
```

---

## Scrollytelling Play Cards

Vertical, section-by-section narratives. Each section has a heading, narrative text, and one or more data visualizations.

### Page Structure

```
.header            -> Title bar with green accent line
.hero              -> Play name, key metric cards, one-sentence framing
.section           -> Repeating content blocks
  .section-head    -> Section number + title
  .narrative       -> 2-4 sentences of analysis
  .chart-container -> D3 visualization(s)
  .source-note     -> Data source attribution
.footer            -> Attribution, data notes
```

### Header CSS

```css
.header {
  background: #FFFFFF;
  padding: 1.5rem 2rem 1rem;
  border-bottom: 2px solid #063309;
}

.header h1 {
  font-size: 2rem;
  font-weight: 300;
  color: #063309;
  margin-bottom: 0.25rem;
}

.header h1::before {
  content: '';
  display: block;
  width: 36px;
  height: 3px;
  background: #063309;
  margin-bottom: 0.5rem;
  border-radius: 2px;
}

.header .subtitle {
  font-size: 0.875rem;
  font-weight: 500;
  color: #063309;
  max-width: 700px;
}
```

### Section CSS

```css
.section {
  max-width: 960px;
  margin: 0 auto;
  padding: 2rem;
  border-bottom: 1px solid #D0D0D0;
}

.section-head {
  display: flex;
  align-items: baseline;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.section-num {
  font-size: 0.75rem;
  font-weight: 600;
  color: #063309;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  white-space: nowrap;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #063309;
}

.narrative {
  font-size: 1rem;
  font-weight: 300;
  color: #303030;
  max-width: 720px;
  margin-bottom: 1.5rem;
  line-height: 1.6;
}
```

### Hero Metric Cards

```css
.metric-row {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  margin: 1.5rem 0;
}

.metric-card {
  background: #FFFFFF;
  border: 1px solid #D0D0D0;
  border-radius: 0.5rem;
  padding: 1rem 1.25rem;
  min-width: 160px;
  flex: 1;
  box-shadow: 0 1px 3px rgba(0,0,0,0.08), 0 1px 2px rgba(0,0,0,0.06);
}

.metric-label {
  font-size: 0.75rem;
  font-weight: 600;
  color: #666666;
  text-transform: uppercase;
  letter-spacing: 0.4px;
  margin-bottom: 0.25rem;
}

.metric-value {
  font-size: 1.75rem;
  font-weight: 700;
  color: #063309;
}

.metric-value.negative { color: #C87654; }
.metric-value.neutral  { color: #1B6CA8; }

.metric-note {
  font-size: 0.75rem;
  font-weight: 300;
  color: #888888;
  margin-top: 0.25rem;
}
```

### Chart Container

```css
.chart-container {
  background: #FFFFFF;
  border: 1px solid #D0D0D0;
  border-radius: 0.5rem;
  padding: 1rem;
  margin: 1rem 0;
  box-shadow: 0 1px 3px rgba(0,0,0,0.08), 0 1px 2px rgba(0,0,0,0.06);
}

.chart-title {
  font-size: 0.875rem;
  font-weight: 400;
  font-style: italic;
  color: #042606;
  margin-bottom: 0.75rem;
}

.chart-container svg {
  width: 100%;
  display: block;
}
```

### Source Notes

```css
.source-note {
  font-size: 0.75rem;
  font-weight: 300;
  color: #888888;
  margin-top: 0.5rem;
  padding-top: 0.5rem;
  border-top: 1px solid #E8E8E8;
}
```

---

## Interactive Dashboards

Dashboards use a toolbar + main content area pattern.

**Class name rules:** Use `.dash-card` for dashboard cards. Do not rename to `.chart-card` or similar. For charts inside dashboard cards, nest a `.chart-container` inside a `.dash-card`.

### Layout

```css
.dashboard {
  display: grid;
  grid-template-rows: auto auto 1fr auto;
  min-height: 100vh;
}

.toolbar {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  padding: 0.75rem 1.5rem;
  background: #F5F6F4;
  border-bottom: 1px solid #D0D0D0;
  align-items: center;
}

.main-content {
  padding: 1.5rem;
  background: #F5F6F4;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

@media (max-width: 768px) {
  .main-content { grid-template-columns: 1fr; }
}
```

### Toolbar Buttons

```css
.toolbar-btn {
  font-family: 'Archivo', sans-serif;
  font-size: 0.875rem;
  font-weight: 400;
  padding: 0.375rem 0.75rem;
  border: 1px solid #D0D0D0;
  border-radius: 0.5rem;
  background: #FFFFFF;
  color: #666666;
  cursor: pointer;
  transition: all 0.15s;
}

.toolbar-btn:hover {
  border-color: #063309;
  color: #063309;
  background: #E8F3EA;
}

.toolbar-btn.active {
  background: #063309;
  color: #FFFFFF;
  border-color: #063309;
}
```

### Dashboard Cards

```css
.dash-card {
  background: #FFFFFF;
  border: 1px solid #D0D0D0;
  border-radius: 0.5rem;
  padding: 1rem;
  box-shadow: 0 1px 3px rgba(0,0,0,0.08), 0 1px 2px rgba(0,0,0,0.06);
}

.dash-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.dash-card-title {
  font-size: 0.875rem;
  font-weight: 400;
  font-style: italic;
  color: #042606;
}
```

### Data Tables

```css
.data-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.875rem;
}

.data-table th {
  font-size: 0.75rem;
  font-weight: 600;
  color: #063309;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  text-align: left;
  padding: 0.5rem 0.75rem;
  border-bottom: 2px solid #D0D0D0;
}

.data-table td {
  padding: 0.5rem 0.75rem;
  font-weight: 300;
  color: #303030;
  border-bottom: 1px solid #E8E8E8;
}

.data-table tr:hover td {
  background: #E8F3EA;
}

.data-table .num {
  text-align: right;
  font-variant-numeric: tabular-nums;
}
```

---

## Leaflet Maps

Maps use CartoDB Positron (light) tiles and follow the same card/panel patterns.

### Map Setup

```css
#map {
  width: 100%;
  min-height: 450px;
  position: relative;
  border-radius: 0.5rem;
}
```

```javascript
L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
  attribution: '&copy; OpenStreetMap &copy; CARTO',
  maxZoom: 18
}).addTo(map);
```

### Info Panel (map hover/click)

```css
.info-panel {
  background: rgba(255, 255, 255, 0.96);
  border: 1px solid #D0D0D0;
  border-radius: 0.5rem;
  padding: 1rem;
  font-size: 0.875rem;
  max-width: 280px;
  line-height: 1.5;
  box-shadow: 0 2px 8px rgba(0,0,0,0.12);
}

.info-panel h3 {
  font-size: 0.875rem;
  font-weight: 700;
  color: #063309;
  margin-bottom: 0.5rem;
}

.info-panel .ip-row {
  display: flex;
  justify-content: space-between;
  gap: 0.75rem;
  padding: 0.125rem 0;
  color: #303030;
}

.info-panel .ip-label {
  color: #666666;
  font-size: 0.75rem;
  font-weight: 400;
}

.info-panel .ip-val {
  font-weight: 600;
  text-align: right;
}

.info-panel .ip-note {
  margin-top: 0.5rem;
  padding-top: 0.5rem;
  border-top: 1px solid #D0D0D0;
  font-size: 0.75rem;
  font-weight: 300;
  color: #888888;
}
```

### Legend Box

```css
.legend-box {
  background: rgba(255, 255, 255, 0.96);
  border: 1px solid #D0D0D0;
  border-radius: 0.5rem;
  padding: 0.75rem 1rem;
  font-size: 0.75rem;
  max-height: calc(100vh - 340px);
  overflow-y: auto;
  box-shadow: 0 1px 3px rgba(0,0,0,0.08);
}

.legend-box h4 {
  font-size: 0.75rem;
  font-weight: 600;
  color: #063309;
  text-transform: uppercase;
  letter-spacing: 0.4px;
  cursor: pointer;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.125rem 0;
  color: #303030;
  cursor: pointer;
  transition: opacity 0.2s;
}

.legend-item.off { opacity: 0.25; }

.legend-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}
```

### Choropleth Styling (GeoJSON)

```javascript
function choroplethStyle(feature, getValue, colorScale) {
  const val = getValue(feature);
  return {
    fillColor: colorScale(val),
    fillOpacity: opacityScale(val),
    weight: 1,
    color: '#D0D0D0',
    opacity: 0.6
  };
}

function highlightFeature(e) {
  e.target.setStyle({ weight: 2, color: '#063309', fillOpacity: 0.7 });
  e.target.bringToFront();
}

function resetHighlight(e) {
  geojsonLayer.resetStyle(e.target);
}
```

---

## Common Components

### Pull Quote

```css
.pull-quote {
  font-size: 1.25rem;
  font-weight: 600;
  font-style: italic;
  color: #B85900;
  max-width: 720px;
  margin: 2rem auto;
  padding: 1.5rem 0;
  border-top: 1px solid #D0D0D0;
  border-bottom: 1px solid #D0D0D0;
  line-height: 1.4;
}
```

### Data Notes Footer

```css
.data-notes {
  background: #F5F6F4;
  padding: 1rem 1.5rem;
  border-top: 1px solid #D0D0D0;
  font-size: 0.875rem;
  font-weight: 300;
  color: #888888;
  line-height: 1.6;
}

.data-notes h4 {
  font-size: 0.75rem;
  font-weight: 600;
  color: #B85900;
  margin-bottom: 0.5rem;
  text-transform: uppercase;
  letter-spacing: 0.4px;
  font-style: normal;
}

.data-notes .dn-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}

@media (max-width: 768px) {
  .data-notes .dn-grid { grid-template-columns: 1fr; }
}
```

### Attribution Footer

```css
.attribution {
  text-align: center;
  padding: 1.25rem 1.5rem;
  font-size: 0.75rem;
  font-weight: 300;
  color: #888888;
  border-top: 1px solid #D0D0D0;
}

.attribution a { color: #063309; }
```

Content: `Net Zero Industrial Policy Lab | Johns Hopkins University | netzeropolicylab.com`

### Tooltip (shared)

```css
.tooltip {
  position: absolute;
  background: rgba(255, 255, 255, 0.97);
  border: 1px solid #D0D0D0;
  border-radius: 0.375rem;
  padding: 0.5rem 0.75rem;
  font-size: 0.875rem;
  color: #303030;
  pointer-events: none;
  z-index: 1000;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.12);
  max-width: 240px;
}

.tooltip .tt-title {
  font-size: 0.875rem;
  font-weight: 700;
  color: #063309;
  margin-bottom: 0.25rem;
}

.tooltip .tt-row {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  font-size: 0.75rem;
}

.tooltip .tt-label { color: #666666; }
.tooltip .tt-val { color: #303030; font-weight: 600; }
```

### Loading Indicator

```css
#loading {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 2000;
  font-size: 1rem;
  font-weight: 500;
  color: #063309;
}
```

### Progress Bar

```css
.progress-bar {
  height: 6px;
  background: #E8E8E8;
  border-radius: 0.25rem;
  margin-top: 0.25rem;
}

.progress-fill {
  height: 100%;
  border-radius: 0.25rem;
  background: #063309;
  transition: width 0.3s;
}
```
