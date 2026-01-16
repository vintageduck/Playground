import re
import base64
import os
from fontTools.ttLib import TTFont

css_path = "/Users/hugomarston/Documents/Histoire/.obsidian/themes/William Morris/theme.css"
extract_dir = "/tmp/extracted_fonts"

if not os.path.exists(extract_dir):
    os.makedirs(extract_dir)

print(f"Reading {css_path}...")
with open(css_path, 'r') as f:
    content = f.read()

# Regex to find @font-face blocks and extract family and base64 src
# src: url('data:font/ttf;charset=utf-8;base64,AAEAAA...')
pattern = r"@font-face\s*\{[^}]*font-family:\s*'([^']+)';[^}]*src:\s*url\('data:([^;]+);charset=([^;]+);base64,([^']+)'\)"

matches = re.finditer(pattern, content)

found = False
for i, match in enumerate(matches):
    found = True
    family_name = match.group(1)
    mime_type = match.group(2)
    charset = match.group(3)
    b64_data = match.group(4)
    
    print(f"\n--- Font {i+1} ---")
    print(f"Family: {family_name}")
    print(f"MIME: {mime_type}")
    print(f"Charset: {charset}")
    print(f"Base64 Length: {len(b64_data)}")
    
    # Validation 1: Check for whitespace
    if '\n' in b64_data or ' ' in b64_data:
        print("WARNING: Base64 string contains whitespace/newlines! This might break CSS.")
        # clean it for testing decode
        b64_data = b64_data.replace('\n', '').replace(' ', '')
    else:
        print("Base64 string is clean (no whitespace).")

    # Validation 2: Try to decode
    try:
        font_data = base64.b64decode(b64_data)
        print(f"Decoded Size: {len(font_data)} bytes")
        
        # Save to file
        filename = f"{family_name}_{i}.ttf"
        filepath = os.path.join(extract_dir, filename)
        with open(filepath, 'wb') as outfiles:
            outfiles.write(font_data)
        
        # Validation 3: Try to open with fontTools
        try:
            tt = TTFont(filepath)
            print("SUCCESS: Valid TTF file detected by fontTools.")
            print(f"  Internal Family: {tt['name'].getDebugName(1)}")
            print(f"  Internal Subfamily: {tt['name'].getDebugName(2)}")
        except Exception as e:
            print(f"ERROR: fontTools could not open format! {e}")
            
    except Exception as e:
        print(f"ERROR: Base64 decode failed! {e}")

if not found:
    print("No embedded fonts found matching regex!")
