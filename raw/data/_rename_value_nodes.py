"""Rename Layer 4 value node files to include full expression in filename"""
import os
import re

base_dir = 'D:\\knowledge-vault\\wiki\\indicators'

# Mapping: grade -> display expression
# We need to read each file's frontmatter to get constraint, value, unit
# Then rename the file to include the expression

rename_map = {}  # old_path -> new_path

for root, dirs, files in os.walk(base_dir):
    for f in files:
        if not f.endswith('.md'):
            continue
        fp = os.path.join(root, f)
        
        with open(fp, 'r', encoding='utf8') as fh:
            content = fh.read()
        
        # Only process Layer 4 value nodes (type: indicator-value)
        if 'type: indicator-value' not in content:
            continue
        
        # Extract frontmatter values
        m_grade = re.search(r'^grade: (.+)$', content, re.M)
        m_constraint = re.search(r'^constraint: (.+)$', content, re.M)
        m_value = re.search(r'^value: (.+)$', content, re.M)
        m_unit = re.search(r'^unit: (.+)$', content, re.M)
        
        if not all([m_grade, m_constraint, m_value, m_unit]):
            continue
        
        grade = m_grade.group(1).strip()
        constraint = m_constraint.group(1).strip()
        value = m_value.group(1).strip()
        unit = m_unit.group(1).strip()
        
        # Build expression for filename
        # Replace special chars that can't be in filenames
        if constraint == '≥':
            expr = f'ge{value}'
        elif constraint == '≤':
            expr = f'le{value}'
        elif constraint == '=':
            expr = f'eq{value}'
        else:
            expr = f'{constraint}{value}'
        
        # Clean unit for filename
        unit_clean = unit.replace('³', '3').replace('²', '2').replace('⁻', '-')
        unit_clean = re.sub(r'[^\w]', '', unit_clean)
        
        if unit_clean:
            expr += f'_{unit_clean}'
        
        # Build new filename
        # Get the parent dir and the base name parts
        dirname = os.path.dirname(fp)
        basename = os.path.basename(fp)
        
        # Split the basename: std_slug__cat_slug__subcat_slug__grade_slug.md
        parts = basename.replace('.md', '').split('__')
        if len(parts) >= 4:
            # Replace the last part (grade_slug) with grade + expression
            grade_slug = parts[-1]
            # Clean grade for filename
            grade_clean = grade.replace('.', '_').replace(' ', '_').replace('(', '').replace(')', '').replace('·', '')
            grade_clean = re.sub(r'[^\w\u4e00-\u9fff]', '_', grade_clean)
            grade_clean = re.sub(r'_+', '_', grade_clean).strip('_')
            
            new_basename = f'{parts[0]}__{parts[1]}__{parts[2]}__{grade_clean}__{expr}.md'
            new_fp = os.path.join(dirname, new_basename)
            
            if fp != new_fp and not os.path.exists(new_fp):
                rename_map[fp] = new_fp

print(f'Files to rename: {len(rename_map)}')

# Also update all links in all files to point to new names
# Build old->new basename mapping
old_to_new_basename = {}
for old_fp, new_fp in rename_map:
    old_basename = os.path.basename(old_fp).replace('.md', '')
    new_basename = os.path.basename(new_fp).replace('.md', '')
    old_to_new_basename[old_basename] = new_basename

print(f'Link mappings: {len(old_to_new_basename)}')

# Update links in ALL indicator files
link_fixed = 0
for root, dirs, files in os.walk(base_dir):
    for f in files:
        if not f.endswith('.md'):
            continue
        fp = os.path.join(root, f)
        with open(fp, 'r', encoding='utf8') as fh:
            content = fh.read()
        
        old_content = content
        for old_bn, new_bn in old_to_new_basename.items():
            content = content.replace(f'|{old_bn}', f'|{new_bn}')
        
        if content != old_content:
            with open(fp, 'w', encoding='utf8') as fh:
                fh.write(content)
            link_fixed += 1

print(f'Link references updated: {link_fixed} files')

# Now rename files
renamed = 0
for old_fp, new_fp in rename_map:
    os.rename(old_fp, new_fp)
    renamed += 1

print(f'Files renamed: {renamed}')

# Verify a sample
print('\n=== Sample new filenames ===')
sample_dir = 'D:\\knowledge-vault\\wiki\\indicators\\工业生产资料'
for f in sorted(os.listdir(sample_dir)):
    if f.startswith('GB_175-2023__抗压强度__3d__') and f.endswith('.md'):
        print(f)
