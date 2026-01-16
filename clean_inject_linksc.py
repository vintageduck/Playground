#!/usr/bin/env python3
"""
COMPREHENSIVE cleanup and injection of LinkSC font.
Removes ALL conflicting rules and injects clean CSS.
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

# 2. Strip ALL internal-link related CSS blocks containing font-family
# This is aggressive but necessary to eliminate conflicts
patterns_to_remove = [
    r'body:not\(\.morris-links-plain\)[^{]*\.cm-hmd-internal-link[^{]*\{[^}]+\}\s*',
    r'body:not\(\.morris-links-plain\)[^{]*\.internal-link[^{]*\{[^}]+\}\s*',
]

for pattern in patterns_to_remove:
    content = re.sub(pattern, '', content, flags=re.DOTALL)

# 3. Create complete font-face and CSS rules
injection = f'''@font-face {{
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

/* Internal Links - Small Caps */
body:not(.morris-links-plain) .markdown-source-view.mod-cm6 .cm-hmd-internal-link,
body:not(.morris-links-plain) .markdown-preview-view .internal-link {{
    font-family: 'LinkSC', serif !important;
    font-size: 1.1em;
    letter-spacing: 0.05em;
}}
'''

# Insert after comment block
if '*/' in content:
    parts = content.split('*/', 1)
    content = parts[0] + '*/\n' + injection + parts[1]
else:
    content = injection + content

with open(css_path, 'w') as f:
    f.write(content)

print("DONE: Cleaned ALL conflicting rules.")
print("Injected 'LinkSC' font family with !important override.")
