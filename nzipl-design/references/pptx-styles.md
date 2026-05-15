# NZIPL PPTX Styles

Slide deck formatting using python-pptx. Light theme with forest green (#063309) brand accent, Archivo font, matching the published NZIPL brief identity.

## Table of Contents
1. [Slide Dimensions and Setup](#slide-dimensions-and-setup)
2. [Color Constants](#color-constants)
3. [Font Mapping](#font-mapping)
4. [Slide Layouts](#slide-layouts)
5. [Chart Styling in PPTX](#chart-styling-in-pptx)
6. [Common Patterns](#common-patterns)

---

## Slide Dimensions and Setup

```python
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

prs = Presentation()
prs.slide_width = Inches(13.333)   # Widescreen 16:9
prs.slide_height = Inches(7.5)
```

Always use widescreen 16:9 (13.333 x 7.5 inches).

---

## Color Constants

```python
# Light theme surfaces
BG_BODY       = RGBColor(0xFF, 0xFF, 0xFF)   # #FFFFFF slide background
BG_SECTION    = RGBColor(0xF5, 0xF6, 0xF4)   # #F5F6F4 section/panel backgrounds
BG_INPUT      = RGBColor(0xED, 0xEE, 0xEC)   # #EDEEEC recessed surfaces

# Text
TEXT_HEADING   = RGBColor(0x06, 0x33, 0x09)   # #063309 headings, brand accent
TEXT_BODY      = RGBColor(0x30, 0x30, 0x30)   # #303030 body text
TEXT_DIMMED    = RGBColor(0x66, 0x66, 0x66)   # #666666 subtitles, labels
TEXT_MUTED     = RGBColor(0x88, 0x88, 0x88)   # #888888 source notes, footnotes
TEXT_CAPTION   = RGBColor(0x04, 0x26, 0x06)   # #042606 figure captions

# Brand green scale
BRAND_7       = RGBColor(0x06, 0x33, 0x09)   # #063309 primary brand
BRAND_6       = RGBColor(0x0E, 0x4A, 0x13)   # #0E4A13 hover/pressed
BRAND_5       = RGBColor(0x1A, 0x66, 0x32)   # #1A6632 lighter accent

# Figure palette
TEAL          = RGBColor(0x6B, 0x9E, 0x9E)   # #6B9E9E primary chart fill
STEEL_BLUE    = RGBColor(0x4E, 0x8C, 0xA8)   # #4E8CA8 secondary fill
AMBER         = RGBColor(0xD4, 0xA3, 0x4A)   # #D4A34A warm accent

# Functional
QUOTE_AMBER   = RGBColor(0xB8, 0x59, 0x00)   # #B85900 pull quotes
INFO_BLUE     = RGBColor(0x1B, 0x6C, 0xA8)   # #1B6CA8 informational
NEGATIVE      = RGBColor(0xC8, 0x76, 0x54)   # #C87654 deficit, decline

# Stage colors
UPSTREAM      = RGBColor(0x8A, 0x42, 0x00)   # #8A4200 brown
MIDSTREAM     = RGBColor(0x1A, 0x66, 0x32)   # #1A6632 forest green
DOWNSTREAM    = RGBColor(0x2C, 0xA0, 0x3E)   # #2CA03E bright green
FINAL_PRODUCT = RGBColor(0xCB, 0x5B, 0x1D)   # #CB5B1D orange

# Border and grid
BORDER_COLOR  = RGBColor(0xD0, 0xD0, 0xD0)   # #D0D0D0
BORDER_SUBTLE = RGBColor(0xE8, 0xE8, 0xE8)   # #E8E8E8
WHITE         = RGBColor(0xFF, 0xFF, 0xFF)
```

---

## Font Mapping

Archivo must be installed on the rendering machine. Fallback: Calibri.

| Role | Primary | Fallback |
|------|---------|----------|
| Heading | Archivo | Calibri |
| Body | Archivo Light | Calibri Light |
| Emphasis | Archivo Medium | Calibri |
| Data/code | JetBrains Mono | Consolas |

```python
FONT_MAIN = 'Archivo'
FONT_DATA = 'JetBrains Mono'

def set_font(run, name, size, bold=False, italic=False, color=TEXT_BODY):
    run.font.name = name
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
```

---

## Slide Layouts

### Title Slide

```python
def make_title_slide(prs, title, subtitle):
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank layout
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = BG_BODY

    # Green accent bar (vertical left marker)
    bar = slide.shapes.add_shape(
        1, Inches(0.6), Inches(2.2), Pt(4), Inches(0.35)
    )
    bar.fill.solid()
    bar.fill.fore_color.rgb = BRAND_7
    bar.line.fill.background()

    # Title
    txBox = slide.shapes.add_textbox(Inches(0.8), Inches(2.4), Inches(10), Inches(1.2))
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = title
    set_font(run, FONT_MAIN, 32, bold=False, color=TEXT_HEADING)

    # Subtitle
    p2 = tf.add_paragraph()
    run2 = p2.add_run()
    run2.text = subtitle
    set_font(run2, FONT_MAIN, 16, color=TEXT_DIMMED)

    # Green bottom border
    border = slide.shapes.add_shape(
        1, Inches(0), Inches(7.35), Inches(13.333), Pt(3)
    )
    border.fill.solid()
    border.fill.fore_color.rgb = BRAND_7
    border.line.fill.background()

    # Attribution
    att = slide.shapes.add_textbox(Inches(0.8), Inches(6.5), Inches(8), Inches(0.4))
    p3 = att.text_frame.paragraphs[0]
    run3 = p3.add_run()
    run3.text = 'Net Zero Industrial Policy Lab | Johns Hopkins University'
    set_font(run3, FONT_MAIN, 10, color=TEXT_MUTED)

    return slide
```

### Section Divider Slide

```python
def make_section_slide(prs, section_num, section_title):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = BG_BODY

    # Section number
    txBox = slide.shapes.add_textbox(Inches(0.8), Inches(2.8), Inches(2), Inches(0.5))
    p = txBox.text_frame.paragraphs[0]
    run = p.add_run()
    run.text = f'SECTION {section_num}'
    set_font(run, FONT_MAIN, 11, bold=True, color=TEXT_HEADING)

    # Section title
    txBox2 = slide.shapes.add_textbox(Inches(0.8), Inches(3.3), Inches(10), Inches(1))
    p2 = txBox2.text_frame.paragraphs[0]
    run2 = p2.add_run()
    run2.text = section_title
    set_font(run2, FONT_MAIN, 28, bold=True, color=TEXT_HEADING)

    # Attribution
    att = slide.shapes.add_textbox(Inches(0.8), Inches(7.05), Inches(8), Inches(0.3))
    p3 = att.text_frame.paragraphs[0]
    run3 = p3.add_run()
    run3.text = 'NZIPL | Johns Hopkins University'
    set_font(run3, FONT_MAIN, 9, color=TEXT_MUTED)

    return slide
```

### Content Slide (text + chart area)

```python
def make_content_slide(prs, title, body_text=None):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = BG_BODY

    # Slide title with green marker
    bar = slide.shapes.add_shape(1, Inches(0.6), Inches(0.45), Pt(4), Inches(0.35))
    bar.fill.solid()
    bar.fill.fore_color.rgb = BRAND_7
    bar.line.fill.background()

    txBox = slide.shapes.add_textbox(Inches(0.8), Inches(0.35), Inches(8), Inches(0.5))
    p = txBox.text_frame.paragraphs[0]
    run = p.add_run()
    run.text = title
    set_font(run, FONT_MAIN, 18, bold=True, color=TEXT_HEADING)

    # Body text (left column)
    if body_text:
        txBox2 = slide.shapes.add_textbox(Inches(0.8), Inches(1.2), Inches(4.5), Inches(5.5))
        tf = txBox2.text_frame
        tf.word_wrap = True
        p2 = tf.paragraphs[0]
        run2 = p2.add_run()
        run2.text = body_text
        set_font(run2, FONT_MAIN, 13, color=TEXT_BODY)
        p2.space_after = Pt(8)

    # Chart/image area: right side
    # Placeholder: Inches(5.8) to Inches(12.5), y from 1.0 to 6.8
    # slide.shapes.add_picture(img_path, Inches(5.8), Inches(1.0), Inches(6.7), Inches(5.8))

    # Attribution
    att = slide.shapes.add_textbox(Inches(0.8), Inches(7.05), Inches(8), Inches(0.3))
    p3 = att.text_frame.paragraphs[0]
    run3 = p3.add_run()
    run3.text = 'NZIPL | Johns Hopkins University'
    set_font(run3, FONT_MAIN, 9, color=TEXT_MUTED)

    return slide
```

### Data Slide (full-width chart or table)

```python
def make_data_slide(prs, title, source_note=None):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = BG_BODY

    # Title bar
    title_bg = slide.shapes.add_shape(
        1, Inches(0), Inches(0), Inches(13.333), Inches(0.9)
    )
    title_bg.fill.solid()
    title_bg.fill.fore_color.rgb = BG_SECTION
    title_bg.line.fill.background()

    txBox = slide.shapes.add_textbox(Inches(0.8), Inches(0.2), Inches(10), Inches(0.5))
    p = txBox.text_frame.paragraphs[0]
    run = p.add_run()
    run.text = title
    set_font(run, FONT_MAIN, 16, italic=True, color=TEXT_CAPTION)

    # Chart area: Inches(0.5) to Inches(12.8), y from 1.1 to 6.5

    # Source note
    if source_note:
        att = slide.shapes.add_textbox(Inches(0.8), Inches(6.9), Inches(10), Inches(0.3))
        p2 = att.text_frame.paragraphs[0]
        run2 = p2.add_run()
        run2.text = f'Source: {source_note}'
        set_font(run2, FONT_MAIN, 9, color=TEXT_MUTED)

    return slide
```

### Metric Cards Slide

```python
def make_metrics_slide(prs, title, metrics):
    """
    metrics: list of dicts with keys 'label', 'value', 'note' (optional), 'color' (optional)
    """
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = BG_BODY

    # Title
    txBox = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(10), Inches(0.5))
    p = txBox.text_frame.paragraphs[0]
    run = p.add_run()
    run.text = title
    set_font(run, FONT_MAIN, 18, bold=True, color=TEXT_HEADING)

    # Metric cards in a row
    card_width = min(2.5, (12 - 0.5 * (len(metrics) - 1)) / len(metrics))
    start_x = (13.333 - (card_width * len(metrics) + 0.5 * (len(metrics) - 1))) / 2

    for i, m in enumerate(metrics):
        x = start_x + i * (card_width + 0.5)
        # Card background
        card = slide.shapes.add_shape(1, Inches(x), Inches(2.0), Inches(card_width), Inches(2.0))
        card.fill.solid()
        card.fill.fore_color.rgb = BG_SECTION
        card.line.color.rgb = BORDER_COLOR
        card.line.width = Pt(1)

        # Label
        lbl = slide.shapes.add_textbox(Inches(x + 0.2), Inches(2.2), Inches(card_width - 0.4), Inches(0.3))
        p_lbl = lbl.text_frame.paragraphs[0]
        r_lbl = p_lbl.add_run()
        r_lbl.text = m['label'].upper()
        set_font(r_lbl, FONT_MAIN, 9, bold=True, color=TEXT_DIMMED)

        # Value
        val = slide.shapes.add_textbox(Inches(x + 0.2), Inches(2.6), Inches(card_width - 0.4), Inches(0.8))
        p_val = val.text_frame.paragraphs[0]
        r_val = p_val.add_run()
        r_val.text = m['value']
        val_color = m.get('color', TEXT_HEADING)
        set_font(r_val, FONT_MAIN, 28, bold=True, color=val_color)

        # Note
        if m.get('note'):
            nt = slide.shapes.add_textbox(Inches(x + 0.2), Inches(3.4), Inches(card_width - 0.4), Inches(0.4))
            p_nt = nt.text_frame.paragraphs[0]
            r_nt = p_nt.add_run()
            r_nt.text = m['note']
            set_font(r_nt, FONT_MAIN, 10, color=TEXT_MUTED)

    return slide
```

---

## Chart Styling in PPTX

Generate charts as PNG using matplotlib, then insert as pictures.

### Matplotlib NZIPL Theme

```python
import matplotlib.pyplot as plt

nzipl_theme = {
    'figure.facecolor': '#FFFFFF',
    'axes.facecolor': '#FFFFFF',
    'axes.edgecolor': '#888888',
    'axes.labelcolor': '#303030',
    'axes.titlesize': 11,
    'axes.titleweight': 600,
    'axes.labelsize': 10,
    'axes.grid': True,
    'xtick.color': '#303030',
    'ytick.color': '#303030',
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'text.color': '#303030',
    'grid.color': '#E8E8E8',
    'grid.linestyle': '-',
    'grid.linewidth': 0.3,
    'grid.alpha': 0.6,
    'legend.facecolor': '#FFFFFF',
    'legend.edgecolor': 'none',
    'legend.fontsize': 9,
    'font.family': 'sans-serif',
    'font.sans-serif': ['Archivo', 'Calibri', 'sans-serif'],
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.1,
}

plt.rcParams.update(nzipl_theme)

NZIPL_COLORS = ['#6B9E9E', '#1B6CA8', '#D4A34A', '#8A4200', '#CB5B1D', '#5B7266']
STAGE_COLORS = ['#8A4200', '#1A6632', '#2CA03E', '#CB5B1D']

BRAND_GREEN = '#063309'
TEAL = '#6B9E9E'
STEEL_BLUE = '#4E8CA8'
AMBER = '#D4A34A'
QUOTE_AMBER = '#B85900'
ORANGE = '#CB5B1D'
BROWN = '#8A4200'
```

### Saving Charts for PPTX

```python
fig.savefig('chart.png', dpi=300, bbox_inches='tight',
            facecolor='#FFFFFF', edgecolor='none', transparent=False)
```

Use dpi=300 for crisp rendering. Always set facecolor to white (`#FFFFFF`).

---

## Common Patterns

### Table on Slide

```python
def style_table(table):
    """Apply NZIPL styling to a pptx table."""
    for row_idx, row in enumerate(table.rows):
        for cell in row.cells:
            cell.fill.solid()
            cell.fill.fore_color.rgb = BG_BODY

            for paragraph in cell.text_frame.paragraphs:
                for run in paragraph.runs:
                    if row_idx == 0:
                        set_font(run, FONT_MAIN, 10, bold=True, color=TEXT_HEADING)
                    else:
                        set_font(run, FONT_MAIN, 11, color=TEXT_BODY)
```

Table styling: thin horizontal rules only, no vertical lines, no cell shading. Header row separated by heavier rule.

### Slide Numbers

```python
def add_slide_number(slide, num, total):
    txBox = slide.shapes.add_textbox(Inches(12.2), Inches(7.1), Inches(1), Inches(0.3))
    p = txBox.text_frame.paragraphs[0]
    p.alignment = PP_ALIGN.RIGHT
    run = p.add_run()
    run.text = f'{num}/{total}'
    set_font(run, FONT_MAIN, 9, color=TEXT_MUTED)
```

### Pull Quote Slide

```python
def make_pullquote_slide(prs, quote_text):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = BG_BODY

    txBox = slide.shapes.add_textbox(Inches(1.5), Inches(2.5), Inches(10), Inches(2.5))
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = quote_text
    set_font(run, FONT_MAIN, 20, bold=True, italic=True, color=QUOTE_AMBER)

    att = slide.shapes.add_textbox(Inches(0.8), Inches(7.05), Inches(8), Inches(0.3))
    p3 = att.text_frame.paragraphs[0]
    run3 = p3.add_run()
    run3.text = 'NZIPL | Johns Hopkins University'
    set_font(run3, FONT_MAIN, 9, color=TEXT_MUTED)

    return slide
```
