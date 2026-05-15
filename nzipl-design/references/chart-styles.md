# NZIPL Chart Styles

Styling reference for D3.js and Chart.js visualizations. Light theme with the NZIPL institutional figure palette. White chart backgrounds, #D0D0D0 grid lines, #888888 axes, Archivo typeface.

## Table of Contents
1. [D3.js Patterns](#d3js-patterns)
2. [Chart.js Configuration](#chartjs-configuration)
3. [Chart Type Selection](#chart-type-selection)

---

## D3.js Patterns

D3 is the primary charting library for scrollytelling and play cards. All charts render as SVG within `.chart-container` elements.

### SVG Container Setup

```javascript
const margin = { top: 20, right: 20, bottom: 40, left: 50 };
const width = containerWidth - margin.left - margin.right;
const height = 300 - margin.top - margin.bottom;

const svg = d3.select(container)
  .append('svg')
  .attr('viewBox', `0 0 ${width + margin.left + margin.right} ${height + margin.top + margin.bottom}`)
  .append('g')
  .attr('transform', `translate(${margin.left},${margin.top})`);
```

Use `viewBox` for responsive sizing. Do not set fixed width/height on SVG elements.

### Axis Styling

```javascript
// X-axis
svg.append('g')
  .attr('transform', `translate(0,${height})`)
  .call(d3.axisBottom(xScale).tickSize(0).tickPadding(8))
  .call(g => g.select('.domain').attr('stroke', '#888888'))
  .call(g => g.selectAll('.tick text')
    .attr('fill', '#303030')
    .attr('font-family', 'Archivo, sans-serif')
    .attr('font-size', '12px'));

// Y-axis
svg.append('g')
  .call(d3.axisLeft(yScale).tickSize(-width).tickPadding(8).ticks(5))
  .call(g => g.select('.domain').remove())
  .call(g => g.selectAll('.tick line')
    .attr('stroke', '#D0D0D0')
    .attr('stroke-dasharray', '2,2'))
  .call(g => g.selectAll('.tick text')
    .attr('fill', '#303030')
    .attr('font-family', 'Archivo, sans-serif')
    .attr('font-size', '12px'));
```

Key patterns:
- X-axis: no tick marks (`tickSize(0)`), domain line in `#888888`
- Y-axis: no domain line, grid lines as dashed `#D0D0D0` lines extending to full width
- Tick labels: Archivo, 12px, `#303030`
- Tick padding: 8px

### Bar Charts

```javascript
// Horizontal bars (most common in play cards)
svg.selectAll('.bar')
  .data(data)
  .join('rect')
  .attr('class', 'bar')
  .attr('x', 0)
  .attr('y', d => yScale(d.name))
  .attr('width', d => xScale(d.value))
  .attr('height', yScale.bandwidth())
  .attr('fill', '#6B9E9E')
  .attr('rx', 3);

// Value labels at end of bars
svg.selectAll('.bar-label')
  .data(data)
  .join('text')
  .attr('x', d => xScale(d.value) + 6)
  .attr('y', d => yScale(d.name) + yScale.bandwidth() / 2)
  .attr('dy', '0.35em')
  .attr('fill', '#303030')
  .attr('font-family', 'Archivo, sans-serif')
  .attr('font-size', '12px')
  .text(d => formatValue(d.value));
```

Bar fill colors by context:
- Default/institutional: `#6B9E9E` (teal, Style A)
- Technology-specific: use technology colors from design-tokens.md
- Supply chain: use stage colors (brown/green/orange)
- Negative/deficit: `#C87654`
- Highlight (selected): `#1B6CA8`

Bar radius: `rx: 3`.

### Line Charts

```javascript
const line = d3.line()
  .x(d => xScale(d.year))
  .y(d => yScale(d.value))
  .curve(d3.curveMonotoneX);

// Hero series (country of interest)
svg.append('path')
  .datum(heroData)
  .attr('fill', 'none')
  .attr('stroke', '#6B9E9E')
  .attr('stroke-width', 2.5)
  .attr('d', line);

// Secondary series
svg.append('path')
  .datum(otherData)
  .attr('fill', 'none')
  .attr('stroke', '#D0D0D0')
  .attr('stroke-width', 1.5)
  .attr('d', line);

// Data points
svg.selectAll('.dot')
  .data(data)
  .join('circle')
  .attr('cx', d => xScale(d.year))
  .attr('cy', d => yScale(d.value))
  .attr('r', 3)
  .attr('fill', '#6B9E9E')
  .attr('stroke', '#FFFFFF')
  .attr('stroke-width', 1.5);
```

Line weights: hero series 2.5px, secondary series 1.5px.
Dot stroke matches page background (`#FFFFFF`) to create visual separation.

### Treemaps

```javascript
// Supply chain stage treemap
function stageColor(stage) {
  const colors = {
    'upstream': '#8A4200',
    'midstream': '#1A6632',
    'downstream': '#2CA03E',
    'final_product': '#CB5B1D'
  };
  return colors[stage] || '#5B7266';
}

cell.append('text')
  .attr('fill', '#FFFFFF')
  .attr('font-family', 'Archivo, sans-serif')
  .attr('font-size', d => d.dx > 80 ? '12px' : '10px')
  .text(d => d.data.name);
```

Treemap stroke between cells: `#FFFFFF` at 1px (uses page background to create gaps).
Labels inside rectangles use white text on colored fills.

### Radar Charts (GP Brief Signature Element)

```javascript
// Single filled polygon
const radarArea = d3.areaRadial()
  .angle((d, i) => i * (2 * Math.PI / axes.length))
  .innerRadius(0)
  .outerRadius(d => radiusScale(d.value));

svg.append('path')
  .datum(data)
  .attr('d', radarArea)
  .attr('fill', '#6B9E9E')
  .attr('fill-opacity', 0.5)
  .attr('stroke', '#6B9E9E')
  .attr('stroke-width', 1.5);

// Grid rings at 0%, 50%, 100%
[0, 0.5, 1].forEach(pct => {
  svg.append('circle')
    .attr('r', radiusScale(pct))
    .attr('fill', 'none')
    .attr('stroke', '#D0D0D0')
    .attr('stroke-width', 0.5);
});

// Axis labels
axisLabels.forEach((label, i) => {
  svg.append('text')
    .attr('x', labelX(i))
    .attr('y', labelY(i))
    .attr('fill', '#303030')
    .attr('font-family', 'Archivo, sans-serif')
    .attr('font-size', '10px')
    .attr('text-anchor', textAnchor(i))
    .text(label);
});

// Grid value labels
svg.selectAll('.grid-label')
  .data([0.5, 1])
  .join('text')
  .attr('fill', '#888888')
  .attr('font-size', '9px')
  .text(d => `${d * 100}%`);
```

Paired radar (manufacturing + resources): first polygon `#6B9E9E`, second polygon `#D4A34A` at 40% opacity.

### Annotations

```javascript
// Reference line (e.g., RCA = 1 threshold)
svg.append('line')
  .attr('x1', xScale(1)).attr('x2', xScale(1))
  .attr('y1', 0).attr('y2', height)
  .attr('stroke', '#888888')
  .attr('stroke-width', 1)
  .attr('stroke-dasharray', '4,3');

// Annotation label
svg.append('text')
  .attr('x', xScale(1) + 6)
  .attr('y', 12)
  .attr('fill', '#888888')
  .attr('font-family', 'Archivo, sans-serif')
  .attr('font-size', '12px')
  .attr('font-weight', 600)
  .text('RCA = 1');
```

Annotation colors: `#888888` for reference lines and labels. Dashed line: `4,3`.

### D3 Tooltip

```javascript
const tooltip = d3.select('body').append('div')
  .attr('class', 'tooltip')
  .style('opacity', 0);

function showTooltip(event, d) {
  tooltip.transition().duration(150).style('opacity', 1);
  tooltip.html(`
    <div class="tt-title">${d.name}</div>
    <div class="tt-row">
      <span class="tt-label">Exports</span>
      <span class="tt-val">${formatUSD(d.exports)}</span>
    </div>
    <div class="tt-row">
      <span class="tt-label">RCA</span>
      <span class="tt-val">${d.rca.toFixed(2)}</span>
    </div>
  `)
  .style('left', (event.pageX + 12) + 'px')
  .style('top', (event.pageY - 20) + 'px');
}

function hideTooltip() {
  tooltip.transition().duration(200).style('opacity', 0);
}
```

Tooltip CSS is defined in `html-patterns.md` under Common Components.

### Number Formatting

```javascript
const formatUSD = d => {
  if (d >= 1e9) return `$${(d / 1e9).toFixed(1)}B`;
  if (d >= 1e6) return `$${(d / 1e6).toFixed(1)}M`;
  if (d >= 1e3) return `$${(d / 1e3).toFixed(0)}K`;
  return `$${d.toFixed(0)}`;
};

const formatPct = d => `${(d * 100).toFixed(1)}%`;
const formatRCA = d => d.toFixed(2);
```

---

## Chart.js Configuration

Chart.js is used for dashboards and simpler visualizations. Apply the NZIPL theme via global defaults.

### Global Defaults

```javascript
Chart.defaults.color = '#303030';
Chart.defaults.borderColor = '#D0D0D0';
Chart.defaults.font.family = "'Archivo', sans-serif";
Chart.defaults.font.size = 12;

// Legend
Chart.defaults.plugins.legend.labels.color = '#666666';
Chart.defaults.plugins.legend.labels.font = { family: "'Archivo', sans-serif", size: 12, weight: 400 };
Chart.defaults.plugins.legend.labels.boxWidth = 12;
Chart.defaults.plugins.legend.labels.padding = 12;

// Tooltip
Chart.defaults.plugins.tooltip.backgroundColor = 'rgba(255, 255, 255, 0.97)';
Chart.defaults.plugins.tooltip.borderColor = '#D0D0D0';
Chart.defaults.plugins.tooltip.borderWidth = 1;
Chart.defaults.plugins.tooltip.titleFont = { family: "'Archivo', sans-serif", size: 13, weight: 700 };
Chart.defaults.plugins.tooltip.titleColor = '#063309';
Chart.defaults.plugins.tooltip.bodyFont = { family: "'Archivo', sans-serif", size: 12, weight: 300 };
Chart.defaults.plugins.tooltip.bodyColor = '#303030';
Chart.defaults.plugins.tooltip.padding = { top: 8, bottom: 8, left: 12, right: 12 };
Chart.defaults.plugins.tooltip.cornerRadius = 6;
```

### Scale Configuration

```javascript
const nziplScaleOptions = {
  x: {
    grid: { display: false },
    border: { color: '#888888' },
    ticks: {
      color: '#303030',
      font: { family: "'Archivo', sans-serif", size: 12 },
      padding: 8
    }
  },
  y: {
    grid: {
      color: '#D0D0D0',
      borderDash: [2, 2],
      drawBorder: false
    },
    ticks: {
      color: '#303030',
      font: { family: "'Archivo', sans-serif", size: 12 },
      padding: 8
    }
  }
};
```

### Bar Chart Example

```javascript
new Chart(ctx, {
  type: 'bar',
  data: {
    labels: labels,
    datasets: [{
      data: values,
      backgroundColor: '#6B9E9E',
      borderRadius: 4,
      borderSkipped: false,
      barPercentage: 0.7,
      categoryPercentage: 0.85
    }]
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    plugins: { legend: { display: false } },
    scales: nziplScaleOptions
  }
});
```

### Doughnut Chart

```javascript
new Chart(ctx, {
  type: 'doughnut',
  data: {
    labels: labels,
    datasets: [{
      data: values,
      backgroundColor: ['#6B9E9E', '#1B6CA8', '#D4A34A', '#8A4200', '#CB5B1D'],
      borderColor: '#FFFFFF',
      borderWidth: 2
    }]
  },
  options: {
    responsive: true,
    cutout: '65%',
    plugins: {
      legend: {
        position: 'right',
        labels: { color: '#303030', padding: 8 }
      }
    }
  }
});
```

Doughnut border between segments: `#FFFFFF` at 2px (matches page background). Cutout: 65%.

---

## Chart Type Selection

| Question | Chart Type | Library |
|----------|-----------|---------|
| How does X rank against peers? | Horizontal bar | D3 or Chart.js |
| How has X changed over time? | Line chart | D3 |
| What is the composition of X? | Treemap or stacked bar | D3 |
| What share does X hold? | Doughnut | Chart.js |
| Where is X concentrated geographically? | Choropleth map | Leaflet + D3 scale |
| How do two variables relate? | Scatter plot | D3 |
| What is the distribution of X? | Histogram or box plot | D3 |
| How do 3+ plays compare across metrics? | Grouped bar or radar | D3 or Chart.js |
| Country competitiveness profile? | Radar / spider chart | D3 |
| Export composition by supply chain? | Treemap (stage colors) | D3 |

Default chart height: 300px for standard, 400px for hero charts, 200px for small multiples.
