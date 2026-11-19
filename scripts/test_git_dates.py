import subprocess

def get_git_date(filepath):
    try:
        res = subprocess.run(['git', 'log', '-1', '--format=%cs', filepath], capture_output=True, text=True, check=True)
        date = res.stdout.strip()
        if date:
            return date
    except Exception:
        pass
    return None

test_files = [
    'index.html',
    'Notes/osy-k-scheme-notes.html',
    'Blog/50-capstone-project-ideas-computer-engineering.html',
    'Branches/Computer.html',
    'pyq/311302-basic-mathematics.html'
]

for tf in test_files:
    print(f"{tf} -> {get_git_date(tf)}")
