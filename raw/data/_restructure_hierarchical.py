"""
Restructure indicator nodes into per-standard directories.
Each standard gets its own directory; files inside use clean names.

Before:
  wiki/indicators/工业生产资料/
    GB_175-2023__抗压强度.md
    GB_175-2023__抗压强度__3d.md
    GB_175-2023__抗压强度__3d__强度等级42_5__≥17_0MPa.md
    ...

After:
  wiki/indicators/工业生产资料/
    GB 175-2023/
      index.md                    ← Layer 1: standard node (title: GB 175-2023)
      抗压强度.md                  ← Layer 2: category (title: 抗压强度)
      3d.md                       ← Layer 3: subcategory (title: 3d)
      强度等级42.5_≥42.5MPa.md     ← Layer 4: value (title: 强度等级42.5 ≥42.5MPa)
      ...
"""
import os
import re
import shutil

base = 'D:\\knowledge-vault\\wiki\\indicators'

# Step 1: Parse all files, group by (cat_dir, std_no)
from collections import defaultdict

# {cat_dir: {std_no: {type: [files]}}}
groups = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

for root, dirs, files in os.walk(base):
    if '_references' in root:
        continue
    for f in files:
        if not f.endswith('.md'):
            continue
        fp = os.path.join(root, f)
        with open(fp, 'r', encoding='utf8') as fh:
            content = fh.read()
        
        # Parse frontmatter
        fm = {}
        for line in content.split('\n'):
            m = re.match(r'^(\w+): (.+)$', line)
            if m:
                fm[m.group(1)] = m.group(2).strip()
        
        node_type = fm.get('type', '')
        std_no = fm.get('std', '')
        
        if not std_no:
            continue
        
        rel_dir = os.path.relpath(root, base)
        if rel_dir == '.':
            continue
        
        groups[rel_dir][std_no][node_type].append({
            'path': fp,
            'content': content,
            'fm': fm
        })

print(f'Found {sum(len(stds) for stds in groups.values())} standards across {len(groups)} categories')

# Step 2: Create new structure
created = 0
for cat_dir in sorted(groups.keys()):
    for std_no in sorted(groups[cat_dir].keys()):
        # Create standard directory
        std_dirname = std_no.replace('/', '-')
        std_dir = os.path.join(base, cat_dir, std_dirname)
        os.makedirs(std_dir, exist_ok=True)
        
        files_data = groups[cat_dir][std_no]
        
        # Create Layer 1: standard index page
        index_content = f"""---
type: standard-node
title: {std_no}
std: {std_no}
category: {cat_dir}
---

# {std_no}

## 技术指标

"""
        
        # Collect links to category nodes
        cat_links = []
        for node_type in ['indicator-category', 'indicator-subcategory', 'indicator-value']:
            for item in files_data.get(node_type, []):
                title = item['fm'].get('title', '')
                cat_name = item['fm'].get('category', '')
                sub_name = item['fm'].get('subcategory', '')
                grade = item['fm'].get('grade', '')
                
                if node_type == 'indicator-category':
                    cat_links.append(f'- [[{cat_name}|{cat_name}]]')
                elif node_type == 'indicator-subcategory':
                    cat_links.append(f'  - [[{sub_name}|{sub_name}]]')
                elif node_type == 'indicator-value':
                    cat_links.append(f'    - [[{title}|{title}]]')
        
        # Deduplicate
        seen = set()
        unique_links = []
        for link in cat_links:
            if link not in seen:
                seen.add(link)
                unique_links.append(link)
        
        index_content += '\n'.join(unique_links)
        
        index_fp = os.path.join(std_dir, 'index.md')
        with open(index_fp, 'w', encoding='utf8') as fh:
            fh.write(index_content)
        created += 1
        
        # Create Layer 2/3/4 files with clean names
        for node_type in ['indicator-category', 'indicator-subcategory', 'indicator-value']:
            for item in files_data.get(node_type, []):
                content = item['content']
                fm = item['fm']
                title = fm.get('title', '')
                
                # Determine clean filename
                if node_type == 'indicator-category':
                    clean_name = title + '.md'
                elif node_type == 'indicator-subcategory':
                    clean_name = title + '.md'
                elif node_type == 'indicator-value':
                    # grade + expression
                    grade = fm.get('grade', '')
                    constraint = fm.get('constraint', '')
                    value = fm.get('value', '')
                    unit = fm.get('unit', '')
                    expr = f'{constraint}{value}{unit}'
                    clean_name = f'{grade}_{expr}.md'
                
                # Clean filename of invalid chars
                clean_name = clean_name.replace('\u00b3', '3').replace('\u00b2', '2').replace('\u207b', '-')
                clean_name = clean_name.replace('/', '\uff0f')
                clean_name = re.sub(r'[<>:"|?*]', '', clean_name)
                
                # Update content: fix links and title
                # Title is already clean from the original
                # Fix absolute paths in links
                content = content.replace('D:\\knowledge-vault\\wiki\\indicators\\', 'wiki/indicators/')
                
                # Update links: old format [[wiki/indicators/cat_dir/std_slug__cat__subcat__grade__expr|...]]
                # to new format [[wiki/indicators/cat_dir/std_no/clean_name|...]]
                # We need to map old filenames to new ones
                
                new_fp = os.path.join(std_dir, clean_name)
                if not os.path.exists(new_fp):
                    with open(new_fp, 'w', encoding='utf8') as fh:
                        fh.write(content)
                    created += 1

print(f'Created {created} files')

# Step 3: Now fix all links between files
# Build a mapping: old_basename -> new_path
old_to_new = {}
for cat_dir in sorted(groups.keys()):
    for std_no in sorted(groups[cat_dir].keys()):
        std_dirname = std_no.replace('/', '-')
        std_dir = os.path.join(base, cat_dir, std_dirname)
        
        for node_type in ['indicator-category', 'indicator-subcategory', 'indicator-value']:
            for item in groups[cat_dir][std_no].get(node_type, []):
                old_fp = item['path']
                old_bn = os.path.basename(old_fp).replace('.md', '')
                
                fm = item['fm']
                title = fm.get('title', '')
                
                if node_type == 'indicator-category':
                    new_name = title + '.md'
                elif node_type == 'indicator-subcategory':
                    new_name = title + '.md'
                elif node_type == 'indicator-value':
                    grade = fm.get('grade', '')
                    constraint = fm.get('constraint', '')
                    value = fm.get('value', '')
                    unit = fm.get('unit', '')
                    expr = f'{constraint}{value}{unit}'
                    new_name = f'{grade}_{expr}.md'
                
                new_name = new_name.replace('\u00b3', '3').replace('\u00b2', '2').replace('\u207b', '-')
                new_name = new_name.replace('/', '\uff0f')
                new_name = re.sub(r'[<>:"|?*]', '', new_name)
                
                new_bn = new_name.replace('.md', '')
                old_to_new[old_bn] = (cat_dir, std_dirname, new_bn)

# Update links in all new files
link_fixed = 0
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
        for old_bn, (cat_dir, std_dirname, new_bn) in old_to_new.items():
            # Replace [[wiki/indicators/cat_dir/old_bn|...]] with [[wiki/indicators/cat_dir/std_dirname/new_bn|...]]
            old_link = f'wiki/indicators/{cat_dir}/{old_bn}'
            new_link = f'wiki/indicators/{cat_dir}/{std_dirname}/{new_bn}'
            content = content.replace(old_link, new_link)
        
        if content != old_content:
            with open(fp, 'w', encoding='utf8') as fh:
                fh.write(content)
            link_fixed += 1

print(f'Fixed links in {link_fixed} files')

# Step 4: Remove old flat files (those directly in cat_dir, not in subdirs)
removed = 0
for root, dirs, files in os.walk(base):
    if '_references' in root:
        continue
    rel = os.path.relpath(root, base)
    if rel == '.':
        continue
    # Only delete files directly in category dir (depth 1)
    if os.sep not in rel:
        for f in files:
            if f.endswith('.md'):
                fp = os.path.join(root, f)
                os.remove(fp)
                removed += 1

print(f'Removed {removed} old flat files')

# Step 5: Move _references
for root, dirs, files in os.walk(base):
    if '_references' in root:
        cat_dir = os.path.basename(os.path.dirname(root))
        ref_dir = os.path.join(base, cat_dir, '_references')
        os.makedirs(ref_dir, exist_ok=True)
        for f in files:
            if f.endswith('.md'):
                old_fp = os.path.join(root, f)
                new_fp = os.path.join(ref_dir, f)
                if old_fp != new_fp and not os.path.exists(new_fp):
                    shutil.move(old_fp, new_fp)
        # Remove old _references dir
        try:
            os.rmdir(root)
        except:
            pass

print('\nDone!')
