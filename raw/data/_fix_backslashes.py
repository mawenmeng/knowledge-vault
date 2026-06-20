"""Fix backslashes in wiki links"""
import os

base = 'D:\\knowledge-vault\\wiki\\indicators'

fixed = 0
for root, dirs, files in os.walk(base):
    for f in files:
        if f != 'index.md':
            continue
        fp = os.path.join(root, f)
        with open(fp, 'r', encoding='utf8') as fh:
            content = fh.read()
        
        old_content = content
        # Replace single backslash with forward slash
        content = content.replace('\\', '/')
        
        if content != old_content:
            with open(fp, 'w', encoding='utf8') as fh:
                fh.write(content)
            fixed += 1

print('Fixed ' + str(fixed) + ' files')

# Verify
fp = os.path.join(base, '工业生产资料', 'GB 175-2023', 'index.md')
with open(fp, 'r', encoding='utf8') as f:
    for line in f:
        if 'wiki/indicators' in line:
            print(line.strip()[:80])
            break
