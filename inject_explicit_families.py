#!/usr/bin/env python3
"""Inject two explicit families: ObsidianSC-Regular and ObsidianSC-Italic"""
import re

# Read fonts
with open('/tmp/sc_regular_base64.txt', 'r') as f:
    regular_b64 = f.read().replace('\n', '')

with open('/tmp/custom_italic_sc_base64.txt', 'r') as f:
    italic_b64 = f.read().replace('\n', '')

css_path = "/Users/hugomarston/Documents/Histoire/.obsidian/themes/William Morris/theme.css"
with open(css_path, 'r') as f:
    content = f.read()

# 1. Strip ALL existing @font-face blocks to start clean
new_content = re.sub(r'@font-face\s*\{[^}]+\}\s*', '', content, flags=re.DOTALL)

# 2. Add distinct families
# Font Family 1: Upright
font_face_css = f'''@font-face {{
    font-family: 'ObsidianSC-Regular';
    src: url('data:font/ttf;charset=utf-8;base64,{regular_b64}') format('truetype');
    font-weight: normal;
    font-style: normal;
}}

@font-face {{
    font-family: 'ObsidianSC-Italic';
    src: url('data:font/ttf;charset=utf-8;base64,{italic_b64}') format('truetype');
    font-weight: normal;
    font-style: normal; /* We tell browser this is NORMAL style for this specific family */
}}
'''

if '*/' in new_content:
    parts = new_content.split('*/', 1)
    new_content = parts[0] + '*/\n' + font_face_css + parts[1]
else:
    new_content = font_face_css + new_content

# 3. Update Link Selectors
link_selector = r"(body:not\(\.morris-links-plain\) \.markdown-source-view\.mod-cm6 \.cm-hmd-internal-link,\s*body:not\(\.morris-links-plain\) \.markdown-preview-view \.internal-link\s*\{[^}]+\})"

# New CSS logic:
# 1. Base link uses ObsidianSC-Regular
replacement_css = """body:not(.morris-links-plain) .markdown-source-view.mod-cm6 .cm-hmd-internal-link,
body:not(.morris-links-plain) .markdown-preview-view .internal-link {
    font-family: 'ObsidianSC-Regular', 'EB Garamond', serif !important;
    font-size: 1.1em;
    letter-spacing: 0.05em;
    font-variant: normal;
    font-style: normal;
}

/* CASE 1: Italic inside Link [[_Text_]] */
body:not(.morris-links-plain) .markdown-source-view.mod-cm6 .cm-hmd-internal-link .cm-em,
body:not(.morris-links-plain) .markdown-preview-view .internal-link em,
body:not(.morris-links-plain) .markdown-preview-view .internal-link i {
    font-family: 'ObsidianSC-Italic', 'EB Garamond', serif !important;
    font-style: normal !important; 
    font-variant: normal;
    letter-spacing: 0.05em;
    transform: none !important;
}

/* CASE 2: Link inside Italic _[[Link]]_ */
body:not(.morris-links-plain) .cm-em .cm-hmd-internal-link,
body:not(.morris-links-plain) em .internal-link,
body:not(.morris-links-plain) i .internal-link {
    font-family: 'ObsidianSC-Italic', 'EB Garamond', serif !important;
    font-style: normal !important;
    font-variant: normal;
    letter-spacing: 0.05em;
    transform: none !important;
}

/* CASE 3: Link IS Italic (Mixed classes) */
body:not(.morris-links-plain) .cm-hmd-internal-link.cm-em {
    font-family: 'ObsidianSC-Italic', 'EB Garamond', serif !important;
    font-style: normal !important;
    font-variant: normal;
    letter-spacing: 0.05em;
    transform: none !important;
}
"""

if re.search(link_selector, new_content, flags=re.DOTALL):
    new_content = re.sub(link_selector, replacement_css, new_content)
else:
    new_content += "\n\n" + replacement_css

# Cleanup any previous "Explicitly ensure italics" blocks
legacy_italic_fix = r"/\* Explicitly ensure italics.+?\}"
new_content = re.sub(legacy_italic_fix, '', new_content, flags=re.DOTALL)

with open(css_path, 'w') as f:
    f.write(new_content)

print("Injected 'ObsidianSC-Regular' and 'ObsidianSC-Italic'.")
print("Updated link CSS to force family switching.")
