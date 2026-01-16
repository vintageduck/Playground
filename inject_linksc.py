#!/usr/bin/env python3
"""
Clean injection of LinkSC font family into theme.css.
This completely replaces any previous font injection attempts.
"""
import re

# Read base64 encoded fonts
with open('/tmp/linksc_regular_b64.txt', 'r') as f:
    regular_b64 = f.read().replace('\n', '')

with open('/tmp/linksc_italic_b64.txt', 'r') as f:
    italic_b64 = f.read().replace('\n', '')

css_path = "/Users/hugomarston/Documents/Histoire/.obsidian/themes/William Morris/theme.css"
with open(css_path, 'r') as f:
    content = f.read()

# 1. Strip ALL existing @font-face blocks
content = re.sub(r'@font-face\s*\{[^}]+\}\s*', '', content, flags=re.DOTALL)

# 2. Create simple, clean @font-face rules for ONE family with two styles
font_face_css = f'''@font-face {{
    font-family: 'LinkSC';
    src: url('data:font/ttf;charset=utf-8;base64,{regular_b64}') format('truetype');
    font-weight: normal;
    font-style: normal;
}}

@font-face {{
    font-family: 'LinkSC';
    src: url('data:font/ttf;charset=utf-8;base64,{italic_b64}') format('truetype');
    font-weight: normal;
    font-style: italic;
}}
'''

# Insert after comment block
if '*/' in content:
    parts = content.split('*/', 1)
    content = parts[0] + '*/\n' + font_face_css + parts[1]
else:
    content = font_face_css + content

# 3. Update link CSS - SIMPLE approach
# Just set font-family. Browser automatically picks italic when needed.
link_selector = r"(body:not\(\.morris-links-plain\) \.markdown-source-view\.mod-cm6 \.cm-hmd-internal-link,\s*body:not\(\.morris-links-plain\) \.markdown-preview-view \.internal-link\s*\{[^}]+\})"

replacement_css = """body:not(.morris-links-plain) .markdown-source-view.mod-cm6 .cm-hmd-internal-link,
body:not(.morris-links-plain) .markdown-preview-view .internal-link {
    font-family: 'LinkSC', serif;
    font-size: 1.1em;
    letter-spacing: 0.05em;
}"""

if re.search(link_selector, content, flags=re.DOTALL):
    content = re.sub(link_selector, replacement_css, content)
else:
    content += "\n\n" + replacement_css

# 4. Remove any previous CASE 2/3 italic hacks
content = re.sub(r'/\* CASE [123].+?\}\s*', '', content, flags=re.DOTALL)
content = re.sub(r'/\* Force the Italic.+?\}\s*', '', content, flags=re.DOTALL)
content = re.sub(r'/\* Explicitly ensure.+?\}\s*', '', content, flags=re.DOTALL)

with open(css_path, 'w') as f:
    f.write(content)

print("Injected 'LinkSC' font family (Regular + Italic).")
print("Link CSS simplified to just use 'LinkSC'.")
