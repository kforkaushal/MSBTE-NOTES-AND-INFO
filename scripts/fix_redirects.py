with open('_redirects', 'r', encoding='utf-8') as f:
    text = f.read()

# Fix target with .html
text = text.replace('/notes/315319-operating-system.html', '/notes/315319-operating-system')

# Remove case-insensitive wildcard loop rules
old_block = '''# ------------------------------------------
# 3. Uppercase path to canonical lowercase 301 redirects (Section 3.1)
# ------------------------------------------
/Blog/*    /blog/:splat    301!
/Notes/*    /notes/:splat    301!
/Branches/*    /branches/:splat    301!
/CollegeInfo/*    /collegeinfo/:splat    301!
/Jobs/*    /jobs/:splat    301!
/Courses/*    /courses/:splat    301!
/News/*    /news/:splat    301!
/PYQ/*     /pyq/:splat     301!


# ------------------------------------------

/Model-Answer/*    /model-answer/:splat    301!'''

new_block = '''# ------------------------------------------
# 3. Clean canonical 301 redirects (Case folding handled via clean internal links & canonicals)
# ------------------------------------------'''

text = text.replace(old_block, new_block)

with open('_redirects', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated _redirects: removed risky wildcard loop rules and fixed target URLs.")
