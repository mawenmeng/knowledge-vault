"""Fix index.md links - handle same title/display case"""
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
        rel = os.path.relpath(root, base)
        
        # Find ALL [[...|...]] links
        links = re.findall(r'\[\[([^\]/]+?)\|([^\]]+)\]\]', content)
        
        for title, display in links:
            if title.startswith('wiki/'):
                continue
            
            title_slug = title.replace(' ', '_')
            title_slug = re.sub(r'[<>:\"|?*]', '', title_slug)
            title_slug = title_slug.replace('\u00b3', '3').replace('\u00b2', '2').replace('\u207b', '-')
            title_slug = title_slug.replace('/', '\uff0f')
            
            new_link = '[[wiki/indicators/' + rel + '/' + title_slug + '|' + display + ']]'
            old_link = '[[' + title + '|' + display + ']]'
            content = content.replace(old_link, new_link)
        
        content = content.replace('[[|', '<!-- empty -->')
        
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
