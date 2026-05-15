# NZIPL PPTX Styles (Template-Based)

All PPTX decks are generated from the official NZIPL template (`references/NZIPL_PPT_Template_v1.potx`). The template contains all slide masters, layouts, backgrounds, logos, fonts, and colors. Claude fills placeholders with content - never builds slides from scratch.

## Step 1: Convert and Open the Template

python-pptx cannot open `.potx` files directly. Convert to `.pptx` by fixing the content type:

```python
import zipfile, shutil, os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.oxml.ns import qn

TEMPLATE = os.path.expanduser('~/.claude/skills/nzipl-design/references/NZIPL_PPT_Template_v1.potx')

def load_template(output_path):
    """Convert .potx to .pptx and return a clean Presentation with no slides."""
    shutil.copy2(TEMPLATE, output_path)
    
    with zipfile.ZipFile(output_path, 'r') as zin:
        ct = zin.read('[Content_Types].xml').decode('utf-8')
    ct = ct.replace('presentationml.template.main+xml',
                    'presentationml.presentation.main+xml')
    
    tmp = output_path + '.tmp'
    with zipfile.ZipFile(output_path, 'r') as zin:
        with zipfile.ZipFile(tmp, 'w') as zout:
            for item in zin.infolist():
                data = zin.read(item.filename)
                if item.filename == '[Content_Types].xml':
                    data = ct.encode('utf-8')
                zout.writestr(item, data)
    shutil.move(tmp, output_path)
    
    prs = Presentation(output_path)
    
    # Remove all example slides
    sldIdLst = prs.part._element.find(qn('p:sldIdLst'))
    for sldId in list(sldIdLst):
        rId = sldId.get(qn('r:id'))
        prs.part.drop_rel(rId)
        sldIdLst.remove(sldId)
    
    return prs
```

## Step 2: Choose a Layout

The template has 28 layouts. Use this map to pick the right one:

| Use case | Layout index | Layout name | Placeholders |
|----------|-------------|-------------|--------------|
| **Cover** (dark green bg, logo, title) | 0 | `1_Cover` | ph[14]=text, ph[15]=cover picture |
| **Cover variant 2** | 1 | `3_Cover` | ph[14]=text, ph[15]=cover picture |
| **Cover variant 3** | 2 | `Cover` | ph[14]=text, ph[15]=cover picture |
| **Cover variant 4** | 3 | `2_Cover` | ph[14]=text, ph[15]=cover picture |
| **Cover variant 5** | 4 | `4_Cover` | ph[14]=text, ph[15]=cover picture |
| **Content (1 column)** | 5 | `Title and Content (1 Column)` | ph[0]=title, ph[1]=body |
| **Content (2 column, text+text)** | 6 | `Title and Content (2 Column)` | ph[0]=title, ph[1]=body left, ph[13]=body right |
| **Content (text + picture)** | 7 | `5_Title and Content (2 Column)` | ph[0]=title, ph[1]=body, ph[13]=picture |
| **Content (text + picture) v2** | 8 | `6_Title and Content (2 Column)` | ph[0]=title, ph[1]=body, ph[13]=picture |
| **Content (text + picture + caption)** | 9 | `9_Title and Content (2 Column)` | ph[0]=title, ph[1]=body, ph[13]=picture, ph[15]=caption |
| **Content (text + picture) v3** | 10 | `1_Title and Content (2 Column)` | ph[0]=title, ph[1]=body, ph[13]=picture |
| **Content (text + picture) v4** | 11 | `7_Title and Content (2 Column)` | ph[0]=title, ph[1]=body, ph[13]=picture |
| **Content (text + picture + source)** | 12 | `8_Title and Content (2 Column)` | ph[0]=title, ph[1]=body, ph[13]=picture, ph[14]=source text |
| **Content (text + picture) v5** | 13 | `4_Title and Content (2 Column)` | ph[0]=title, ph[1]=body, ph[13]=picture |
| **Content (text + 2 pictures)** | 14 | `2_Title and Content (2 Column)` | ph[0]=title, ph[1]=body, ph[13]=pic1, ph[14]=pic2 |
| **Full-width multi-picture** | 15 | `3_Title and Content (2 Column)` | ph[13]=pic1, ph[14]=pic2, ph[15]=pic3, ph[16]=pic4 |
| **Section divider** | 16 | `1_Divder` | ph[0]=title, ph[14]=picture |
| **Section divider v2** | 17 | `Divder` | ph[0]=title, ph[14]=picture |
| **Callout (blue)** | 18 | `Callout Blue` | ph[13]=body, ph[14]=picture |
| **Callout (blue) v2** | 19 | `3_Callout Blue` | ph[13]=body, ph[14]=picture |
| **Callout (blue) v3** | 20 | `2_Callout Blue` | ph[13]=body, ph[14]=picture |
| **Callout (yellow) with text** | 21 | `2_Callout Yellow` | ph[13]=body, ph[14]=picture |
| **Comparison** | 22 | `Comparison` | ph[0]=title, ph[1]=label left, ph[2]=content left, ph[3]=label right, ph[4]=content right |
| **Callout (yellow) minimal** | 23-27 | `3-6_Callout Yellow` | ph[14]=picture |

### Default layout choices

| User asks for... | Use layout |
|---|---|
| Title/cover slide | 0 (`1_Cover`) |
| Text-only content | 5 (`Title and Content (1 Column)`) |
| Text + chart/figure | 7 (`5_Title and Content (2 Column)`) |
| Text + chart + source note | 12 (`8_Title and Content (2 Column)`) |
| Full-width data/chart | 5 with image inserted manually |
| Section break | 16 (`1_Divder`) |
| Key quote or callout | 18 (`Callout Blue`) |
| Side-by-side comparison | 22 (`Comparison`) |

## Step 3: Fill Placeholders

### Text placeholders

```python
slide = prs.slides.add_slide(prs.slide_layouts[5])

# Title (ph[0])
slide.placeholders[0].text = "The EV Supply Chain Opportunity"

# Body (ph[1]) - supports multiple paragraphs
tf = slide.placeholders[1].text_frame
tf.clear()
p = tf.paragraphs[0]
p.text = "First bullet point here."

p2 = tf.add_paragraph()
p2.text = "Second bullet point here."
```

The template controls all formatting (font, size, color, bullets). Do NOT set font properties on runs - the placeholder styles handle it.

### Picture placeholders

Insert matplotlib charts or user-supplied images into picture placeholders:

```python
slide = prs.slides.add_slide(prs.slide_layouts[7])  # text + picture
slide.placeholders[0].text = "Manufacturing Competitiveness"
slide.placeholders[1].text = "Analysis of eight indicators."

# Insert chart into picture placeholder
slide.placeholders[13].insert_picture('chart.png')
```

### Cover slide

```python
slide = prs.slides.add_slide(prs.slide_layouts[0])  # 1_Cover

# Title + subtitle in text placeholder
slide.placeholders[14].text = "Presentation Title\nSubtitle or date"

# Optional: insert cover image
# slide.placeholders[15].insert_picture('cover_photo.jpg')
```

## Step 4: Generate Charts for Slides

Generate charts as PNGs using matplotlib, then insert into picture placeholders. Use the NZIPL matplotlib theme from `chart-styles.md`.

```python
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

# Register Archivo
FONT_DIR = os.path.expanduser('~/Library/Fonts')
for f in os.listdir(FONT_DIR):
    if f.startswith('Archivo') and f.endswith('.ttf'):
        fm.fontManager.addfont(os.path.join(FONT_DIR, f))

plt.rcParams.update({
    'figure.facecolor': '#FFFFFF',
    'axes.facecolor': '#FFFFFF',
    'axes.edgecolor': '#888888',
    'axes.labelcolor': '#303030',
    'xtick.color': '#303030',
    'ytick.color': '#303030',
    'text.color': '#303030',
    'grid.color': '#E8E8E8',
    'grid.linewidth': 0.3,
    'font.family': 'sans-serif',
    'font.sans-serif': ['Archivo', 'Calibri', 'sans-serif'],
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
})

NZIPL_COLORS = ['#6B9E9E', '#1B6CA8', '#D4A34A', '#8A4200', '#CB5B1D', '#5B7266']
```

Save charts with transparent=False and white background:
```python
fig.savefig('chart.png', dpi=300, bbox_inches='tight',
            facecolor='#FFFFFF', edgecolor='none', transparent=False)
```

Charts should have NO titles - the slide title or a text placeholder provides the caption.

## Step 5: Save

```python
prs.save('output.pptx')
```

## Complete Example

```python
import os, shutil, zipfile
from pptx import Presentation
from pptx.oxml.ns import qn

# 1. Load template
prs = load_template('/tmp/my_deck.pptx')

# 2. Cover slide
s1 = prs.slides.add_slide(prs.slide_layouts[0])
s1.placeholders[14].text = "Critical Minerals in Latin America\nApril 2026"

# 3. Content slide with text
s2 = prs.slides.add_slide(prs.slide_layouts[5])
s2.placeholders[0].text = "Why Critical Minerals Matter"
tf = s2.placeholders[1].text_frame
tf.clear()
tf.paragraphs[0].text = "Latin America holds 60% of global lithium reserves."
p2 = tf.add_paragraph()
p2.text = "Chile, Argentina, and Brazil are the key players."

# 4. Text + chart slide
s3 = prs.slides.add_slide(prs.slide_layouts[7])
s3.placeholders[0].text = "Lithium Reserves by Country"
s3.placeholders[1].text = "Chile leads with 44% of known reserves."
s3.placeholders[13].insert_picture('/tmp/lithium_bar.png')

# 5. Section divider
s4 = prs.slides.add_slide(prs.slide_layouts[16])
s4.placeholders[0].text = "Supply Chain Analysis"

# 6. Save
prs.save('/tmp/my_deck.pptx')
```

## Notes

- Never override placeholder fonts/colors/sizes - the template handles all styling
- Picture placeholders auto-crop inserted images to fit; generate charts at roughly 16:9 aspect ratio for best results
- The template is 62MB due to embedded background images - this is normal
- Footer and slide number placeholders exist but are managed by the template's header/footer settings
- If Archivo is not installed, PowerPoint falls back to Calibri (acceptable but not ideal)
