"""
Fix link targets: for each [[path|display]], if display != basename(path),
set path basename = display (the display text IS the correct filename).
"""
import os
import re

base = 'D:\\knowledge-vault\\wiki\\indicators'

fixed = 0
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
            target_fname = path.split('/')[-1]
            if target_fname != display:
                # Fix the link target to match display text
                old_link = '[[wiki/indicators/' + path + '|' + display + ']]'
                parts = path.split('/')
                parts[-1] = display
                new_path = '/'.join(parts)
                new_link = '[[wiki/indicators/' + new_path + '|' + display + ']]'
                content = content.replace(old_link, new_link)
                fixed += 1
        
        if content != old_content:
            with open(fp, 'w', encoding='utf8') as fh:
                fh.write(content)

print('Fixed link targets: ' + str(fixed))

# Verify
print('\n=== 28d.md ===')
fp = os.path.join(base, '工业生产资料', 'GB 175-2023', '28d.md')
with open(fp, 'r', encoding='utf8') as f:
    for line in f:
        if '[[' in line:
            print('  ' + line.strip())

print('\n=== 3d.md ===')
fp = os.path.join(base, '工业生产资料', 'GB 175-2023', '3d.md')
with open(fp, 'r', encoding='utf8') as f:
    for line in f:
        if '[[' in line:
            print('  ' + line.strip())

# Verify files exist
print('\n=== File existence check ===')
for grade in ['强度等级32.5', '强度等级32.5R', '强度等级42.5', '强度等级42.5R', '强度等级52.5', '强度等级52.5R']:
    for expr in ['≥12.0MPa', '≥17.0MPa', '≥22.0MPa', '≥23.0MPa', '≥27.0MPa', '≥32.5MPa', '≥42.5MPa', '≥52.5MPa']:
        fname = grade + ' ' + expr + '.md'
        fp = os.path.join(base, '工业生产资料', 'GB 175-2023', fname)
        exists = os.path.exists(fp)
        if not exists:
            print('  MISSING: ' + fname)
