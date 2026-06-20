"""Fix index.md links - use forward slashes"""
import os
import re

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
        
        # Replace backslashes in wiki/indicators paths
        content = content.replace('wiki/indicators\\', 'wiki/indicators/')
        
        if content != old_content:
            with open(fp, 'w', encoding='utf8') as fh:
                fh.write(content)
            fixed += 1

print('Fixed ' + str(fixed) + ' index.md files')

# Verify
print('\n=== index.md links (first 5) ===')
with open('D:\\knowledge-vault\\wiki\\indicators\\工业生产资料\\GB 175-2023\\index.md', 'r', encoding='utf8') as f:
    count = 0
    for line in f:
        if '[[' in line:
            print(line.strip())
            count += 1
            if count >= 5:
                break
