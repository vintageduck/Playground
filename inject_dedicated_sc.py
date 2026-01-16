#!/usr/bin/env python3
"""Inject Dedicated Obsidian SC Font Family"""
import re

# Read the base64 encoded fonts
with open('/tmp/sc_regular_base64.txt', 'r') as f:
    regular_b64 = f.read().replace('\n', '')

with open('/tmp/custom_italic_sc_base64.txt', 'r') as f:
    italic_b64 = f.read().replace('\n', '')

css_path = "/Users/hugomarston/Documents/Histoire/.obsidian/themes/William Morris/theme.css"
with open(css_path, 'r') as f:
    content = f.read()

# 1. Strip ALL existing @font-face blocks to start clean
# Matches @font-face { ... }
new_content = re.sub(r'@font-face\s*\{[^}]+\}\s*', '', content, flags=re.DOTALL)

# 2. Strip previous "Creative Fix" or "Custom Italic" blocks
new_content = re.sub(r'/\* Creative Fix.+?\}', '', new_content, flags=re.DOTALL)
new_content = re.sub(r'/\* Custom Italic.+?\}', '', new_content, flags=re.DOTALL)

# 3. Create new @font-face blocks for "Obsidian SC"
# Both have font-family 'Obsidian SC', but different styles.
font_face_css = f'''@font-face {{
    font-family: 'Obsidian SC';
    src: url('data:font/truetype;base64,{regular_b64}') format('truetype');
    font-weight: normal;
    font-style: normal;
}}

@font-face {{
    font-family: 'Obsidian SC';
    src: url('data:font/truetype;base64,{italic_b64}') format('truetype');
    font-weight: normal;
    font-style: italic;
}}
'''

# Insert at top (after comments if possible)
if '*/' in new_content:
    parts = new_content.split('*/', 1)
    new_content = parts[0] + '*/\n' + font_face_css + parts[1]
else:
    new_content = font_face_css + new_content

# 4. Update Link Selectors to use 'Obsidian SC' explicitly
# We remove font-variant: small-caps because the font IS small caps.
# We trust the browser to pick the 'italic' face when em/i tags are used.

link_selector = r"(body:not\(\.morris-links-plain\) \.markdown-source-view\.mod-cm6 \.cm-hmd-internal-link,\s*body:not\(\.morris-links-plain\) \.markdown-preview-view \.internal-link\s*\{[^}]+\})"

# The new CSS for links. 
# Note: We DON'T need a separate rule for 'em' because the family 'Obsidian SC' has an italic face defined.
# So clean simple CSS should work.
replacement_css = """body:not(.morris-links-plain) .markdown-source-view.mod-cm6 .cm-hmd-internal-link,
body:not(.morris-links-plain) .markdown-preview-view .internal-link {
    font-family: 'Obsidian SC', serif;
    font-size: 1.1em;
    letter-spacing: 0.05em;
    font-variant: normal; /* The font itself is SC, no variation needed */
    font-style: normal; /* Default to normal */
}

/* Explicitly ensure italics use the italic face of the family */
body:not(.morris-links-plain) .markdown-source-view.mod-cm6 .cm-hmd-internal-link .cm-em,
body:not(.morris-links-plain) .markdown-preview-view .internal-link em,
body:not(.morris-links-plain) .markdown-preview-view .internal-link i {
    font-family: 'Obsidian SC', serif;
    font-style: italic;
    font-variant: normal;
}"""

# Check if we can find the old selector to replace
if re.search(link_selector, new_content, flags=re.DOTALL):
    new_content = re.sub(link_selector, replacement_css, new_content)
else:
    # If regex fails (maybe formatting changed), append it
    new_content += "\n\n" + replacement_css

with open(css_path, 'w') as f:
    f.write(new_content)

print("Injected 'Obsidian SC' family with Normal and Italic styles.")
print("Updated link CSS to use 'Obsidian SC' exclusively.")
