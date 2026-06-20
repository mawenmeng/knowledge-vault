"""Fix indicator node links - use proper Obsidian wiki links with relative paths"""
import os
import re

base_dir = 'D:\\knowledge-vault\\wiki\\indicators'

# Fix all indicator node files
fixed = 0
for root, dirs, files in os.walk(base_dir):
    for f in files:
        if not f.endswith('.md'):
            continue
        fp = os.path.join(root, f)
        with open(fp, 'r', encoding='utf8') as fh:
            content = fh.read()
        
        # Fix 1: Replace absolute Windows paths with wiki-relative paths
        # Pattern: D:\knowledge-vault\wiki\indicators\xxx -> wiki/indicators/xxx
        old_content = content
        content = re.sub(
            r'D:\\\\knowledge-vault\\\\wiki\\\\indicators\\\\',
            'wiki/indicators/',
            content
        )
        # Also fix mixed backslash/forward slash
        content = re.sub(
            r'D:\\\\knowledge-vault\\\\wiki\\\\indicators/',
            'wiki/indicators/',
            content
        )
        
        if content != old_content:
            with open(fp, 'w', encoding='utf8') as fh:
                fh.write(content)
            fixed += 1

print(f'Fixed {fixed} files with absolute path links')

# Now verify a sample
print('\n=== Verification ===')
with open('D:\\knowledge-vault\\wiki\\indicators\\工业生产资料\\GB_175-2023__抗压强度.md', 'r', encoding='utf8') as f:
    print(f.read())
