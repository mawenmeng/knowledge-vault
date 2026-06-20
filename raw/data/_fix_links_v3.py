"""
Fix remaining __ links in indicator files.
Uses a direct string replacement approach based on known old->new mappings.
"""
import os
import re

base = 'D:\\knowledge-vault\\wiki\\indicators'

# Step 1: Build old_basename -> new_basename mapping by examining file content
# Old basename was: std_slug__cat_slug__subcat_slug__grade_slug__expr_slug
# New basename is: title (for cat/subcat) or grade_expr (for values)

# We need to reconstruct old basenames from the frontmatter
old_to_new = {}  # (cat_dir, std_dirname, old_bn) -> new_bn

for root, dirs, files in os.walk(base):
    if '_references' in root:
        continue
    for f in files:
        if not f.endswith('.md'):
            continue
        fp = os.path.join(root, f)
        with open(fp, 'r', encoding='utf8') as fh:
            content = fh.read()
        
        fm = {}
        for line in content.split('\n'):
            m = re.match(r'^(\w+): (.+)$', line)
            if m:
                fm[m.group(1)] = m.group(2).strip()
        
        rel = os.path.relpath(root, base)
        parts = rel.split(os.sep)
        if len(parts) < 2:
            continue
        cat_dir = parts[0]
        std_dirname = parts[1]
        new_bn = f.replace('.md', '')
        
        std_no = fm.get('std', '')
        ntype = fm.get('type', '')
        title = fm.get('title', '')
        
        # Reconstruct old basename
        std_slug = std_no.replace('/', '-').replace(' ', '_')
        std_slug = re.sub(r'[<>:"|?*]', '', std_slug)
        
        if ntype == 'indicator-category':
            cat_slug = title.replace(' ', '_')
            cat_slug = re.sub(r'[<>:"|?*\\/]', '', cat_slug)
            old_bn = f'{std_slug}__{cat_slug}'
        elif ntype == 'indicator-subcategory':
            cat_name = fm.get('category', '')
            cat_slug = cat_name.replace(' ', '_')
            cat_slug = re.sub(r'[<>:"|?*\\/]', '', cat_slug)
            sub_slug = title.replace(' ', '_')
            sub_slug = re.sub(r'[<>:"|?*\\/]', '', sub_slug)
            old_bn = f'{std_slug}__{cat_slug}__{sub_slug}'
        elif ntype == 'indicator-value':
            cat_name = fm.get('category', '')
            cat_slug = cat_name.replace(' ', '_')
            cat_slug = re.sub(r'[<>:"|?*\\/]', '', cat_slug)
            sub_name = fm.get('subcategory', '')
            sub_slug = sub_name.replace(' ', '_')
            sub_slug = re.sub(r'[<>:"|?*\\/]', '', sub_slug)
            grade = fm.get('grade', '')
            grade_slug = grade.replace(' ', '_').replace('(', '').replace(')', '').replace('~', 'to')
            grade_slug = re.sub(r'[^\w\u4e00-\u9fff]', '_', grade_slug)
            grade_slug = re.sub(r'_+', '_', grade_slug).strip('_')
            constraint = fm.get('constraint', '')
            value = fm.get('value', '')
            unit = fm.get('unit', '')
            expr = f'{constraint}{value}{unit}'
            expr_slug = expr.replace(' ', '_').replace('\u00b3', '3').replace('\u00b2', '2').replace('\u207b', '-')
            expr_slug = expr_slug.replace('/', '\uff0f')
            expr_slug = re.sub(r'[^\w\u4e00-\u9fff\u2265\u2264=／%]', '_', expr_slug)
            expr_slug = re.sub(r'_+', '_', expr_slug).strip('_')
            old_bn = f'{std_slug}__{cat_slug}__{sub_slug}__{grade_slug}__{expr_slug}'
        else:
            continue
        
        key = (cat_dir, std_dirname, old_bn)
        old_to_new[key] = new_bn

print(f'Built {len(old_to_new)} old->new mappings')

# Step 2: Apply replacements
fixed = 0
total = 0

for root, dirs, files in os.walk(base):
    if '_references' in root:
        continue
    for f in files:
        if not f.endswith('.md'):
            continue
        fp = os.path.join(root, f)
        with open(fp, 'r', encoding='utf8') as fh:
            content = fh.read()
        
        old_content = content
        
        # Find all wiki/indicators links
        links = re.findall(r'\[\[(wiki/indicators/[^\]]+)\]\]', content)
        
        for link in links:
            total += 1
            link_parts = link.split('|')
            path = link_parts[0]
            
            path_parts = path.split('/')
            if len(path_parts) < 5:
                continue
            
            link_cat_dir = path_parts[2]
            link_std_dirname = path_parts[3]
            link_old_bn = '/'.join(path_parts[4:])
            
            key = (link_cat_dir, link_std_dirname, link_old_bn)
            
            if key in old_to_new:
                new_bn = old_to_new[key]
                old_link = f'[[{link}]]'
                new_link = f'[[wiki/indicators/{link_cat_dir}/{link_std_dirname}/{new_bn}'
                if '|' in link:
                    display = link.split('|', 1)[1]
                    new_link += f'|{display}'
                new_link += ']]'
                content = content.replace(old_link, new_link)
                fixed += 1
        
        if content != old_content:
            with open(fp, 'w', encoding='utf8') as fh:
                fh.write(content)

print(f'Fixed {fixed} links out of {total}')

# Step 3: Verify
remaining = 0
for root, dirs, files in os.walk(base):
    for f in files:
        if not f.endswith('.md'):
            continue
        fp = os.path.join(root, f)
        with open(fp, 'r', encoding='utf8') as fh:
            content = fh.read()
        links = re.findall(r'\[\[wiki/indicators/([^\]]+)\]\]', content)
        for l in links:
            if '__' in l:
                remaining += 1
                if remaining <= 10:
                    print(f'  REMAINING: [[wiki/indicators/{l}]] in {os.path.relpath(fp, base)}')

print(f'Remaining __ links: {remaining}')
