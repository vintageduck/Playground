#!/usr/bin/env python3
"""Inject Custom Italic SC font and update CSS"""
import re

# Read the base64 encoded font
with open('/tmp/custom_italic_sc_base64.txt', 'r') as f:
    italic_b64 = f.read().replace('\n', '')

css_path = "/Users/hugomarston/Documents/Histoire/.obsidian/themes/William Morris/theme.css"
with open(css_path, 'r') as f:
    content = f.read()

# 1. Add the @font-face for the custom italic font
# We place it at the top (after comments)
font_face_css = f'''@font-face {{
    font-family: 'EBGaramond SC Italic Custom';
    src: url('data:font/truetype;base64,{italic_b64}') format('truetype');
    font-weight: normal;
    font-style: normal;
}}
'''

# Insert after the header comment (assumed to end at line 9, or search for first empty line after comment)
# Simpler: just replace the first @font-face or insert at top of file but after comments.
# Let's verify location. The file starts with comments ending at */
if '*/' in content:
    parts = content.split('*/', 1)
    new_content = parts[0] + '*/\n' + font_face_css + parts[1]
else:
    new_content = font_face_css + content

# 2. Update the Link CSS
# We need to target the Italic parts of the link specifically.
# The previous script added a "Creative Fix" block. We will replace that.

# Regex to find the "Creative Fix" block and replace it
creative_fix_pattern = r"/\* Creative Fix for Italic Small Caps \*/.+?display:\s*inline-block;\s*\}"
creative_fix_replacement = """/* Custom Italic Small Caps Font */
body:not(.morris-links-plain) .markdown-source-view.mod-cm6 .cm-hmd-internal-link .cm-em,
body:not(.morris-links-plain) .markdown-preview-view .internal-link em,
body:not(.morris-links-plain) .markdown-preview-view .internal-link i {
    font-family: 'EBGaramond SC Italic Custom', serif;
    font-style: normal; /* Font is already italic/skewed */
    font-variant: normal; /* Glyphs are already small caps */
    transform: none; /* Remove previous mechanical skew */
    letter-spacing: 0.05em;
}"""

# Check if pattern exists, if so replace, if not append (or insert if we can find the link block)
if re.search(creative_fix_pattern, new_content, flags=re.DOTALL):
    new_content = re.sub(creative_fix_pattern, creative_fix_replacement, new_content, flags=re.DOTALL)
else:
    # If the creative fix isn't there (maybe I reverted it?), append it or find the link block.
    # We'll just append it to ensure it overrides.
    new_content += "\n\n" + creative_fix_replacement

with open(css_path, 'w') as f:
    f.write(new_content)

print(f"Injected custom font face.")
print(f"Updated CSS to use 'EBGaramond SC Italic Custom'.")
