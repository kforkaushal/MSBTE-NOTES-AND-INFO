with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'nana-patekar' in l or 'asha-bhosle' in l or 'ajit-pawar' in l:
        print(f"--- Line {i+1} ---")
        for j in range(max(0, i-5), min(len(lines), i+15)):
            print(f"{j+1}: {lines[j]}", end='')
