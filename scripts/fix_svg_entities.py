import glob, re, xml.etree.ElementTree as ET

for svg in glob.glob('resourse/**/*.svg', recursive=True):
    with open(svg, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace bare & with &amp;
    fixed_content = re.sub(r'&(?!(?:amp|lt|gt|quot|apos|#\d+|#x[0-9a-fA-F]+);)', '&amp;', content)
    if fixed_content != content:
        with open(svg, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        print(f"Fixed entities in: {svg}")

# Re-validate
all_valid = True
for svg in glob.glob('resourse/**/*.svg', recursive=True):
    try:
        ET.parse(svg)
    except Exception as e:
        print(f"STILL INVALID: {svg} -> {e}")
        all_valid = False

if all_valid:
    print("ALL SVGs are 100% VALID XML!")
