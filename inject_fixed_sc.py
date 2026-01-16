#!/usr/bin/env python3
"""Inject Dedicated Obsidian SC Font Family - Attempt 2"""
import re

# Read the base64 encoded fonts
with open('/tmp/sc_regular_base64.txt', 'r') as f:
    regular_b64 = f.read().replace('\n', '')

with open('/tmp/custom_italic_sc_base64.txt', 'r') as f:
    italic_b64 = f.read().replace('\n', '')

css_path = "/Users/hugomarston/Documents/Histoire/.obsidian/themes/William Morris/theme.css"
with open(css_path, 'r') as f:
    content = f.read()

# 1. Strip ALL existing @font-face blocks
new_content = re.sub(r'@font-face\s*\{[^}]+\}\s*', '', content, flags=re.DOTALL)

# 2. Add new @font-face blocks
# Using 'ObsidianSmallCaps' (no space)
# Using data:font/ttf (standard for TTF)
font_face_css = f'''@font-face {{
    font-family: 'ObsidianSmallCaps';
    src: url('data:font/ttf;charset=utf-8;base64,{regular_b64}') format('truetype');
    font-weight: normal;
    font-style: normal;
}}

@font-face {{
    font-family: 'ObsidianSmallCaps';
    src: url('data:font/ttf;charset=utf-8;base64,{italic_b64}') format('truetype');
    font-weight: normal;
    font-style: italic;
}}
'''

if '*/' in new_content:
    parts = new_content.split('*/', 1)
    new_content = parts[0] + '*/\n' + font_face_css + parts[1]
else:
    new_content = font_face_css + new_content

# 3. Update Link Selectors
link_selector = r"(body:not\(\.morris-links-plain\) \.markdown-source-view\.mod-cm6 \.cm-hmd-internal-link,\s*body:not\(\.morris-links-plain\) \.markdown-preview-view \.internal-link\s*\{[^}]+\})"

# Explicitly restoring font-variant: small-caps just in case the font desires it,
# though if the font behaves as analyzed, it shouldn't matter.
# But 'normal' is safer if glyphs are hardcoded.
# Let's use 'normal' but ensuring specificity.
replacement_css = """body:not(.morris-links-plain) .markdown-source-view.mod-cm6 .cm-hmd-internal-link,
body:not(.morris-links-plain) .markdown-preview-view .internal-link {
    font-family: 'ObsidianSmallCaps', 'EB Garamond', serif !important;
    font-size: 1.1em;
    letter-spacing: 0.05em;
    font-variant: normal;
    font-style: normal;
}

body:not(.morris-links-plain) .markdown-source-view.mod-cm6 .cm-hmd-internal-link .cm-em,
body:not(.morris-links-plain) .markdown-preview-view .internal-link em,
body:not(.morris-links-plain) .markdown-preview-view .internal-link i {
    font-family: 'ObsidianSmallCaps', 'EB Garamond', serif !important;
    font-style: italic;
    font-variant: normal;
}"""

if re.search(link_selector, new_content, flags=re.DOTALL):
    new_content = re.sub(link_selector, replacement_css, new_content)
else:
    new_content += "\n\n" + replacement_css

with open(css_path, 'w') as f:
    f.write(new_content)

print("Injected 'ObsidianSmallCaps' family.")
print("Updated link CSS to use 'ObsidianSmallCaps' !important.")
