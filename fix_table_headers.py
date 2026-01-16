#!/usr/bin/env python3
import re

css_path = "/Users/hugomarston/Documents/Histoire/.obsidian/themes/William Morris/theme.css"

with open(css_path, 'r') as f:
    content = f.read()

# Fix Style 1: Medieval Ledger
# Add !important to th background and color
content = re.sub(
    r'(body\.table-ledger th\s*\{[^}]*background-color:\s*)([^;]+)(;)', 
    r'\1\2 !important\3', 
    content
)
content = re.sub(
    r'(body\.table-ledger th\s*\{[^}]*color:\s*)([^;]+)(;)', 
    r'\1\2 !important\3', 
    content
)

# Insert nth-child override for Ledger if not present
if "body.table-ledger th:nth-child(n)" not in content:
    content = content.replace(
        "border-bottom: 3px double #fff;",
        "border-bottom: 3px double #fff;\n}\n\n/* Kill alternation */\nbody.table-ledger th:nth-child(n) {\n    background-color: var(--morris-red) !important;\n    color: #fff !important;"
    )

# Fix Style 2: Simple
# Add !important
content = re.sub(
    r'(body\.table-simple th\s*\{[^}]*background:\s*)([^;]+)(;)', 
    r'\1\2 !important\3', 
    content
)

if "body.table-simple th:nth-child(n)" not in content:
    content = content.replace(
        "padding-right: 0;",
        "padding-right: 0;\n}\n\nbody.table-simple th:nth-child(n) {\n    background: transparent !important;\n    background-color: transparent !important;"
    )

# Fix Style 3: Kelmscott
content = re.sub(
    r'(body\.table-kelmscott th\s*\{[^}]*background-color:\s*)([^;]+)(;)', 
    r'\1\2 !important\3', 
    content
)

if "body.table-kelmscott th:nth-child(n)" not in content:
    content = content.replace(
        "letter-spacing: 0.15em;",
        "letter-spacing: 0.15em;\n}\n\nbody.table-kelmscott th:nth-child(n) {\n    background-color: var(--text-normal) !important;"
    )

# Fix Style 4: Tapestry
content = re.sub(
    r'(body\.table-tapestry th\s*\{[^}]*background-color:\s*)([^;]+)(;)', 
    r'\1\2 !important\3', 
    content
)

if "body.table-tapestry th:nth-child(n)" not in content:
    content = content.replace(
        "/* Removed tint pattern */",
        "/* Removed tint pattern */\n}\n\nbody.table-tapestry th:nth-child(n) {\n    background-color: transparent !important;"
    )

with open(css_path, 'w') as f:
    f.write(content)

print("Applied !important overrides to all table styles.")
