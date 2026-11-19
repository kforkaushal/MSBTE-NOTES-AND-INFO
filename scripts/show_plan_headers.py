with open('seo_plan_full.txt', 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f, 1):
        if line.startswith('#'):
            print(f"L{idx}: {line.strip()}")
