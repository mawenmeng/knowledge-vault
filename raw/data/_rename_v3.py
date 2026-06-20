"""Rename value nodes - include std_no + category + grade for uniqueness"""
import os
import re

base_dir = 'D:\\knowledge-vault\\wiki\\indicators'

rename_map = {}

for root, dirs, files in os.walk(base_dir):
    for f in files:
        if not f.endswith('.md'):
            continue
        fp = os.path.join(root, f)
        
        with open(fp, 'r', encoding='utf8') as fh:
            content = fh.read()
        
        if 'type: indicator-value' not in content:
            continue
        
        m_title = re.search(r'^title: (.+)$', content, re.M)
        m_std = re.search(r'^std: (.+)$', content, re.M)
        m_grade = re.search(r'^grade: (.+)$', content, re.M)
        m_cat = re.search(r'^category: (.+)$', content, re.M)
        
        if not all([m_title, m_std, m_grade, m_cat]):
            continue
        
        title = m_title.group(1).strip()
        std_no = m_std.group(1).strip()
        grade = m_grade.group(1).strip()
        category = m_cat.group(1).strip()
        
        # Build filename: std_no - grade - expression.md
        # e.g., "GB 175-2023 - 强度等级42.5 - ≥42.5MPa.md"
        std_clean = std_no.replace('/', '-').replace(' ', '_')
        grade_clean = grade.replace(' ', '_').replace('\u00b3', '3').replace('\u00b2', '2').replace('\u207b', '-')
        grade_clean = re.sub(r'[<>:"|?*]', '', grade_clean)
        
        expr_part = title.replace(grade, '').strip()
        if expr_part.startswith(' '):
            expr_part = expr_part[1:]
        expr_clean = expr_part.replace(' ', '_').replace('\u00b3', '3').replace('\u00b2', '2').replace('\u207b', '-')
        expr_clean = expr_clean.replace('/', '\uff0f')
        expr_clean = re.sub(r'[<>:"|?*]', '', expr_clean)
        
        new_name = f'{std_clean}__{grade_clean}__{expr_clean}'
        new_name = re.sub(r'_+', '_', new_name).strip('_')
        
        new_fp = os.path.join(root, new_name + '.md')
        
        if fp != new_fp and not os.path.exists(new_fp):
            rename_map[fp] = new_fp

print(f'Files to rename: {len(rename_map)}')

# Build old->new basename mapping
old_to_new = {}
for old_fp, new_fp in rename_map.items():
    old_bn = os.path.basename(old_fp).replace('.md', '')
    new_bn = os.path.basename(new_fp).replace('.md', '')
    old_to_new[old_bn] = new_bn

# Update links
link_fixed = 0
for root, dirs, files in os.walk(base_dir):
    for f in files:
        if not f.endswith('.md'):
            continue
        fp = os.path.join(root, f)
        with open(fp, 'r', encoding='utf8') as fh:
            content = fh.read()
        
        old_content = content
        for old_bn, new_bn in old_to_new.items():
            content = content.replace('|' + old_bn, '|' + new_bn)
        
        if content != old_content:
            with open(fp, 'w', encoding='utf8') as fh:
                fh.write(content)
            link_fixed += 1

print(f'Link references updated: {link_fixed} files')

# Rename
renamed = 0
for old_fp, new_fp in rename_map.items():
    os.rename(old_fp, new_fp)
    renamed += 1

print(f'Files renamed: {renamed}')

# Verify
print('\n=== Sample ===')
sample_dir = 'D:\\knowledge-vault\\wiki\\indicators\\工业生产资料'
for f in sorted(os.listdir(sample_dir)):
    if 'GB_175' in f and '抗压' in f and '3d' in f:
        print(f)
