import re

path = "/Users/hugomarston/Documents/Histoire/.obsidian/themes/William Morris/theme.css"

with open(path, 'r') as f:
    content = f.read()

# 1. Remove the @font-face blocks (the base64 ones)
# We assume they start at line ~10. Matches @font-face { ... } including newlines
# Using regex to find the blocks. 
# The blocks look like: @font-face {\n    font-family: 'Correlli ... }
new_content = re.sub(r'@font-face\s*\{[^}]+\}\s*', '', content, flags=re.DOTALL)

# 2. Fix the link CSS
# Search for the selector and replace the block
link_selector = r"(body:not\(\.morris-links-plain\) \.markdown-source-view\.mod-cm6 \.cm-hmd-internal-link,\s*body:not\(\.morris-links-plain\) \.markdown-preview-view \.internal-link\s*\{[^}]+\})"

replacement_css = """body:not(.morris-links-plain) .markdown-source-view.mod-cm6 .cm-hmd-internal-link,
body:not(.morris-links-plain) .markdown-preview-view .internal-link {
    font-family: 'EB Garamond', serif;
    font-size: 1.1em;
    letter-spacing: 0.05em;
    font-variant: small-caps;
}

/* Creative Fix for Italic Small Caps */
body:not(.morris-links-plain) .markdown-source-view.mod-cm6 .cm-hmd-internal-link .cm-em,
body:not(.morris-links-plain) .markdown-preview-view .internal-link em,
body:not(.morris-links-plain) .markdown-preview-view .internal-link i {
    font-family: 'EB Garamond', serif;
    font-style: normal;
    font-variant: small-caps;
    transform: skewX(-14deg);
    display: inline-block;
}"""

new_content = re.sub(link_selector, replacement_css, new_content)

with open(path, 'w') as f:
    f.write(new_content)

print("Restored theme.css: Removed Base64 fonts and reset link styles.")
