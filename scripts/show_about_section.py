with open('about.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'About Us' in l or 'Empowering' in l or 'Our Mission' in l:
        print(f"Line {i+1}: {l.strip()}")
        for j in range(i, min(len(lines), i+30)):
            print(f"  {j+1}: {lines[j]}", end='')
        break
