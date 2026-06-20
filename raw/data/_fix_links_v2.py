"""
Fix all links in indicator files after restructuring.
Old format: [[wiki/indicators/cat_dir/std_dir/old_bn|display]]
New format: [[wiki/indicators/cat_dir/std_dir/new_bn|display]]

We need to map old basenames to new ones by parsing the actual files.
"""
import os
import re
import json

base = 'D:\\knowledge-vault\\wiki\\indicators'

# Step 1: Build a mapping from all existing files
# key: (cat_dir, std_dirname, old_bn) -> new_bn
# where old_bn is what the file was called in the flat structure

# Actually, let's parse the links in files to find old basenames,
# then look up the correct new basename from the file's content

# First, collect all new files: (cat_dir, std_dirname, new_bn) -> (std_no, node_type, title)
new_files = {}
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
        
        key = (cat_dir, std_dirname, new_bn)
        new_files[key] = {
            'std_no': fm.get('std', ''),
            'type': fm.get('type', ''),
            'title': fm.get('title', ''),
            'category': fm.get('category', ''),
            'subcategory': fm.get('subcategory', ''),
            'grade': fm.get('grade', ''),
            'constraint': fm.get('constraint', ''),
            'value': fm.get('value', ''),
            'unit': fm.get('unit', ''),
        }

print(f'Found {len(new_files)} new files')

# Step 2: Build reverse mapping: (cat_dir, std_no, title_or_key) -> new_bn
# For category nodes: title is the key
# For subcategory nodes: title is the key
# For value nodes: grade + expr is the key

title_to_new = {}  # (cat_dir, std_no, title) -> new_bn
grade_to_new = {}  # (cat_dir, std_no, category, subcategory, grade) -> new_bn

for (cat_dir, std_dirname, new_bn), info in new_files.items():
    std_no = info['std_no']
    ntype = info['type']
    title = info['title']
    
    if ntype == 'indicator-category':
        title_to_new[(cat_dir, std_no, title)] = new_bn
    elif ntype == 'indicator-subcategory':
        title_to_new[(cat_dir, std_no, title)] = new_bn
    elif ntype == 'indicator-value':
        grade = info['grade']
        constraint = info['constraint']
        value = info['value']
        unit = info['unit']
        expr = f'{constraint}{value}{unit}'
        key = f'{grade}_{expr}'
        cat = info.get('category', '')
        sub = info.get('subcategory', '')
        grade_to_new[(cat_dir, std_no, cat, sub, grade)] = new_bn

# Step 3: Fix links in all files
fixed = 0
total_links = 0

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
        
        # Find all [[wiki/indicators/...]] links
        links = re.findall(r'\[\[(wiki/indicators/[^\]]+)\]\]', content)
        
        for link in links:
            total_links += 1
            # Parse link: wiki/indicators/cat_dir/std_dirname/old_bn|display
            link_parts = link.split('|')
            path = link_parts[0]
            display = link_parts[1] if len(link_parts) > 1 else ''
            
            path_parts = path.split('/')
            if len(path_parts) < 4:
                continue
            
            link_cat_dir = path_parts[2]
            link_std_dirname = path_parts[3]
            link_old_bn = '/'.join(path_parts[4:])  # might have subdirs
            
            # Check if this link still has __ format
            if '__' not in link_old_bn:
                continue  # already clean
            
            # The old format: std_slug__cat_slug__subcat_slug__grade_slug__expr_slug
            # We need to find the correct new basename
            
            # Get the std_no from the directory name
            std_no = link_std_dirname
            
            # Parse the old basename to extract info
            parts = link_old_bn.split('__')
            
            if len(parts) == 2:
                # Category link: std_slug__cat_slug
                cat_slug = parts[1]
                # Try to find by title
                # We need to look up the actual title from the category node
                for (ckey_cat, ckey_std, ckey_title), cnew_bn in title_to_new.items():
                    if ckey_cat == link_cat_dir and ckey_std == std_no:
                        # Check if this category's slug matches
                        cat_slug_guess = ckey_title.replace(' ', '_')
                        cat_slug_guess = re.sub(r'[<>:"|?*\\/]', '', cat_slug_guess)
                        if cat_slug_guess.lower() == cat_slug.lower():
                            new_link = f'wiki/indicators/{link_cat_dir}/{link_std_dirname}/{cnew_bn}'
                            if display:
                                new_link += f'|{display}'
                            content = content.replace(f'[[{link}]]', f'[[{new_link}]]')
                            fixed += 1
                            break
            
            elif len(parts) == 3:
                # Subcategory link: std_slug__cat_slug__subcat_slug
                cat_slug = parts[1]
                subcat_slug = parts[2]
                for (skey_cat, skey_std, skey_title), snew_bn in title_to_new.items():
                    if skey_cat == link_cat_dir and skey_std == std_no:
                        subcat_slug_guess = skey_title.replace(' ', '_')
                        subcat_slug_guess = re.sub(r'[<>:"|?*\\/]', '', subcat_slug_guess)
                        if subcat_slug_guess.lower() == subcat_slug.lower():
                            new_link = f'wiki/indicators/{link_cat_dir}/{link_std_dirname}/{snew_bn}'
                            if display:
                                new_link += f'|{display}'
                            content = content.replace(f'[[{link}]]', f'[[{new_link}]]')
                            fixed += 1
                            break
            
            elif len(parts) >= 4:
                # Value link: std_slug__cat_slug__subcat_slug__grade_slug__expr_slug
                cat_slug = parts[1]
                subcat_slug = parts[2]
                grade_slug = parts[3]
                
                # Find matching value node
                for (vkey_cat, vkey_std, vkey_cat2, vkey_sub, vkey_grade), vnew_bn in grade_to_new.items():
                    if (vkey_cat == link_cat_dir and vkey_std == std_no and 
                        vkey_sub.replace(' ', '_').lower() == subcat_slug.lower()):
                        # Check grade
                        grade_slug_guess = vkey_grade.replace(' ', '_')
                        grade_slug_guess = re.sub(r'[<>:"|?*\\/]', '', grade_slug_guess)
                        if grade_slug_guess.lower() == grade_slug.lower():
                            new_link = f'wiki/indicators/{link_cat_dir}/{link_std_dirname}/{vnew_bn}'
                            if display:
                                new_link += f'|{display}'
                            content = content.replace(f'[[{link}]]', f'[[{new_link}]]')
                            fixed += 1
                            break
        
        if content != old_content:
            with open(fp, 'w', encoding='utf8') as fh:
                fh.write(content)

print(f'Fixed {fixed} links out of {total_links} total links checked')

# Step 4: Verify - check for remaining __ links
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
                if remaining <= 5:
                    print(f'  Remaining: [[wiki/indicators/{l}]] in {os.path.relpath(fp, base)}')

print(f'Remaining __ links: {remaining}')
