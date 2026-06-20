"""
Fix remaining issues:
1. Backslashes in index.md links
2. Wrong display text in value links (28d.md etc.)
"""
import os
import re

base = 'D:\\knowledge-vault\\wiki\\indicators'

# Fix 1: Backslashes in all index.md files
fixed_bs = 0
for root, dirs, files in os.walk(base):
    for f in files:
        if f != 'index.md':
            continue
        fp = os.path.join(root, f)
        with open(fp, 'r', encoding='utf8') as fh:
            content = fh.read()
        old = content
        content = content.replace('\\', '/')
        if content != old:
            with open(fp, 'w', encoding='utf8') as fh:
                fh.write(content)
            fixed_bs += 1

print('Fixed backslashes in ' + str(fixed_bs) + ' index.md files')

# Fix 2: Wrong display text in value links
# The link target file name contains the correct expression
# The display text should match the file name (without .md)
# Strategy: for each [[wiki/indicators/.../filename|display]], if display != filename, fix it
fixed_display = 0
for root, dirs, files in os.walk(base):
    for f in files:
        if not f.endswith('.md'):
            continue
        fp = os.path.join(root, f)
        with open(fp, 'r', encoding='utf8') as fh:
            content = fh.read()
        
        old_content = content
        
        # Find all wiki/indicators links with display text
        links = re.findall(r'\[\[(wiki/indicators/[^\]|]+)\|([^\]]+)\]\]', content)
        
        for path, display in links:
            # Get the filename from the path (last segment)
            filename = path.split('/')[-1]
            
            # If display text doesn't match filename, fix it
            if display != filename:
                old_link = '[[wiki/indicators/' + path + '|' + display + ']]'
                new_link = '[[wiki/indicators/' + path + '|' + filename + ']]'
                content = content.replace(old_link, new_link)
                fixed_display += 1
        
        if content != old_content:
            with open(fp, 'w', encoding='utf8') as fh:
                fh.write(content)

print('Fixed display text mismatches: ' + str(fixed_display))

# Verify
print('\n=== Verification ===')
fp = os.path.join(base, '工业生产资料', 'GB 175-2023', 'index.md')
with open(fp, 'r', encoding='utf8') as f:
    print('index.md:')
    for line in f:
        if '[[' in line:
            print('  ' + line.strip())

fp = os.path.join(base, '工业生产资料', 'GB 175-2023', '28d.md')
with open(fp, 'r', encoding='utf8') as f:
    print('\n28d.md:')
    for line in f:
        if '[[' in line:
            print('  ' + line.strip())

fp = os.path.join(base, '工业生产资料', 'GB 175-2023', '3d.md')
with open(fp, 'r', encoding='utf8') as f:
    print('\n3d.md:')
    for line in f:
        if '[[' in line:
            print('  ' + line.strip())
