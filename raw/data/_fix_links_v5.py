"""
Fix remaining __ links - use content-based matching.
For each __ link, find the target file by looking at all files in the same std dir
and matching by title.
"""
import os
import re

base = 'D:\\knowledge-vault\\wiki\\indicators'

# Step 1: Build a lookup: (cat_dir, std_dirname, title) -> new_bn
title_to_new = {}  # (cat_dir, std_dirname, title) -> new_bn
# Also build: (cat_dir, std_dirname, grade, expr) -> new_bn for value nodes
value_to_new = {}  # (cat_dir, std_dirname, grade, expr) -> new_bn

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
        
        ntype = fm.get('type', '')
        title = fm.get('title', '')
        
        if ntype in ('indicator-category', 'indicator-subcategory'):
            title_to_new[(cat_dir, std_dirname, title)] = new_bn
        elif ntype == 'indicator-value':
            grade = fm.get('grade', '')
            constraint = fm.get('constraint', '')
            value = fm.get('value', '')
            unit = fm.get('unit', '')
            expr = f'{constraint}{value}{unit}'
            value_to_new[(cat_dir, std_dirname, grade, expr)] = new_bn

print(f'Title lookup: {len(title_to_new)}')
print(f'Value lookup: {len(value_to_new)}')

# Step 2: Parse __ links and resolve them
fixed = 0
total = 0
unresolved = []

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
        
        links = re.findall(r'\[\[(wiki/indicators/[^\]]+)\]\]', content)
        
        for link in links:
            total += 1
            if '__' not in link:
                continue
            
            link_parts = link.split('|')
            path = link_parts[0]
            display = link_parts[1] if len(link_parts) > 1 else ''
            
            path_parts = path.split('/')
            if len(path_parts) < 5:
                continue
            
            link_cat_dir = path_parts[2]
            link_std_dirname = path_parts[3]
            link_old_bn = '/'.join(path_parts[4:])
            
            # Parse the old basename to extract info
            # Format: cat_slug__subcat_slug__grade_slug__expr_slug
            bn_parts = link_old_bn.split('__')
            
            if len(bn_parts) == 1:
                # Category link: just cat_slug
                # Try to find by display text
                if display:
                    key = (link_cat_dir, link_std_dirname, display)
                    if key in title_to_new:
                        new_bn = title_to_new[key]
                        new_link = f'[[wiki/indicators/{link_cat_dir}/{link_std_dirname}/{new_bn}|{display}]]'
                        content = content.replace(f'[[{link}]]', new_link)
                        fixed += 1
                    else:
                        unresolved.append(link)
            
            elif len(bn_parts) == 2:
                # Subcategory link: cat_slug__subcat_slug
                if display:
                    key = (link_cat_dir, link_std_dirname, display)
                    if key in title_to_new:
                        new_bn = title_to_new[key]
                        new_link = f'[[wiki/indicators/{link_cat_dir}/{link_std_dirname}/{new_bn}|{display}]]'
                        content = content.replace(f'[[{link}]]', new_link)
                        fixed += 1
                    else:
                        unresolved.append(link)
            
            elif len(bn_parts) >= 3:
                # Value link: cat_slug__subcat_slug__grade_slug__expr_slug
                # Use display text to extract grade and expr
                if display:
                    # display format: "grade expr" or just "grade"
                    # Try to match by grade and expr
                    display = display.strip()
                    # The display is the title of the value node
                    key = (link_cat_dir, link_std_dirname, display)
                    if key in title_to_new:
                        new_bn = title_to_new[key]
                        new_link = f'[[wiki/indicators/{link_cat_dir}/{link_std_dirname}/{new_bn}|{display}]]'
                        content = content.replace(f'[[{link}]]', new_link)
                        fixed += 1
                    else:
                        # Try to find by grade
                        # The grade is the first part of display before space
                        grade_match = re.match(r'^(\S+)', display)
                        if grade_match:
                            grade = grade_match.group(1)
                            for (vkey_cat, vkey_std, vkey_grade, vkey_expr), vnew_bn in value_to_new.items():
                                if (vkey_cat == link_cat_dir and vkey_std == link_std_dirname 
                                    and vkey_grade == grade):
                                    new_link = f'[[wiki/indicators/{link_cat_dir}/{link_std_dirname}/{vnew_bn}|{display}]]'
                                    content = content.replace(f'[[{link}]]', new_link)
                                    fixed += 1
                                    break
                            else:
                                unresolved.append(link)
                else:
                    unresolved.append(link)
        
        if content != old_content:
            with open(fp, 'w', encoding='utf8') as fh:
                fh.write(content)

print(f'\nFixed {fixed} links')
print(f'Unresolved: {len(unresolved)}')
for u in unresolved[:10]:
    print(f'  {u}')
