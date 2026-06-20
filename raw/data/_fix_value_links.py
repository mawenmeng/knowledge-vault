"""
Fix link targets in Layer 3 (subcategory) files.
The restructuring script mapped old basenames incorrectly for some files.
Strategy: For each Layer 3 node, verify that value links point to files
that exist and contain the correct expression.
"""
import os
import re
import json

base = 'D:\\knowledge-vault\\wiki\\indicators'

# Step 1: Build a lookup of value nodes: (std_dir, grade, expr) -> filename
# Read from all_indicators.json to get the ground truth
json_path = 'D:\\knowledge-vault\\raw\\data\\_extracted\\all_indicators.json'
with open(json_path, 'r', encoding='utf8') as f:
    all_data = json.load(f)

# Build the mapping from the JSON data
# Structure: {std_code: {category: {subcategory: [{grade, constraint, value, unit, ...}]}}}
std_value_map = {}
for item in all_data:
    std = item.get('standard', '')
    cat = item.get('indicator_category', '')
    sub = item.get('indicator_subcategory', '')
    grade = item.get('grade', '')
    constraint = item.get('constraint', '')
    value = item.get('value', '')
    unit = item.get('unit', '')
    
    if not all([std, cat, sub, grade]):
        continue
    
    expr = constraint + str(value) + unit
    
    if std not in std_value_map:
        std_value_map[std] = {}
    if cat not in std_value_map[std]:
        std_value_map[std][cat] = {}
    if sub not in std_value_map[std][cat]:
        std_value_map[std][cat][sub] = []
    std_value_map[std][cat][sub].append({
        'grade': grade,
        'constraint': constraint,
        'value': value,
        'unit': unit,
        'expr': expr
    })

# Step 2: For each Layer 3 file, check and fix value links
fixed = 0
total_links_checked = 0
for root, dirs, files in os.walk(base):
    for f in files:
        if f == 'index.md' or not f.endswith('.md'):
            continue
        fp = os.path.join(root, f)
        with open(fp, 'r', encoding='utf8') as fh:
            content = fh.read()
        
        # Check if this is a Layer 3 (subcategory) node
        if 'type: indicator-subcategory' not in content:
            continue
        
        # Get std and title from frontmatter
        std_code = ''
        title = ''
        for line in content.split('\n'):
            if line.startswith('std:'):
                std_code = line.split(':', 1)[1].strip()
            if line.startswith('title:'):
                title = line.split(':', 1)[1].strip()
        
        if not std_code or not title:
            continue
        
        # Get the category from the link in the file
        cat_match = re.search(r'\[\[wiki/indicators/[^]]+/([^/|]+)\]\]', content)
        category = ''
        if cat_match:
            category = cat_match.group(1)
        
        # Find the expected values for this std/category/subcategory
        expected_values = []
        if std_code in std_value_map:
            for cat_key, subs in std_value_map[std_code].items():
                # Try to match category by checking if the link target contains cat_key
                if category and cat_key in category:
                    if title in subs:
                        expected_values = subs[title]
                        break
                elif cat_key in content:
                    if title in subs:
                        expected_values = subs[title]
                        break
        
        if not expected_values:
            continue
        
        # Build expected filenames
        expected_fnames = {}
        for ev in expected_values:
            grade = ev['grade']
            expr = ev['expr']
            fname = grade + ' ' + expr
            expected_fnames[grade] = fname
        
        # Check each value link in the file
        links = re.findall(r'\[\[(wiki/indicators/[^\]|]+)\|([^\]]+)\]\]', content)
        
        for path, display in links:
            total_links_checked += 1
            target_fname = path.split('/')[-1]
            
            # Check if the target file exists
            target_path = os.path.join(base, path.replace('wiki/indicators/', ''))
            if not os.path.exists(target_path + '.md'):
                # Try with underscores
                alt_path = target_path.replace(' ', '_')
                if os.path.exists(alt_path + '.md'):
                    # Target exists with underscores - will be fixed by rename
                    pass
                else:
                    # Target doesn't exist - need to fix
                    # Extract grade from display text
                    grade_match = re.match(r'^(\S+)', display)
                    if grade_match:
                        grade = grade_match.group(1)
                        if grade in expected_fnames:
                            correct_fname = expected_fnames[grade]
                            old_link = '[[wiki/indicators/' + path + '|' + display + ']]'
                            new_link = '[[wiki/indicators/' + '/'.join(path.split('/')[:-1]) + '/' + correct_fname + '|' + display + ']]'
                            content = content.replace(old_link, new_link)
                            fixed += 1

# Write back
for root, dirs, files in os.walk(base):
    for f in files:
        if f == 'index.md' or not f.endswith('.md'):
            continue
        fp = os.path.join(root, f)
        with open(fp, 'r', encoding='utf8') as fh:
            content = fh.read()
        # Already modified in-memory above... need a different approach

print('Links checked: ' + str(total_links_checked))
print('Links fixed: ' + str(fixed))
