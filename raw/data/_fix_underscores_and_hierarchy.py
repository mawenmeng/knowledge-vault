"""
Comprehensive fix:
1. Remove underscores from filenames (replace with space)
2. Update all links to use new filenames
3. Fix hierarchy: index.md -> Layer2 only, remove standard page cross-links
"""
import os
import re

base = 'D:\\knowledge-vault\\wiki\\indicators'

# Step 1: Build rename mapping
rename_map = {}
for root, dirs, files in os.walk(base):
    for f in files:
        if not f.endswith('.md'):
            continue
        if '_' not in f:
            continue
        new_f = f.replace('_', ' ')
        if new_f != f:
            old_fp = os.path.join(root, f)
            new_fp = os.path.join(root, new_f)
            rename_map[old_fp] = new_fp

print('Files to rename: ' + str(len(rename_map)))

# Step 2: Build old_bn -> new_bn mapping
bn_map = {}
for old_fp, new_fp in rename_map.items():
    old_bn = os.path.basename(old_fp).replace('.md', '')
    new_bn = os.path.basename(new_fp).replace('.md', '')
    bn_map[old_bn] = new_bn

# Step 3: Update links in ALL files
link_fixed = 0
for root, dirs, files in os.walk(base):
    for f in files:
        if not f.endswith('.md'):
            continue
        fp = os.path.join(root, f)
        with open(fp, 'r', encoding='utf8') as fh:
            content = fh.read()
        
        old_content = content
        
        for old_bn, new_bn in bn_map.items():
            content = content.replace('/' + old_bn + '|', '/' + new_bn + '|')
            content = content.replace('/' + old_bn + ']', '/' + new_bn + ']')
        
        if content != old_content:
            with open(fp, 'w', encoding='utf8') as fh:
                fh.write(content)
            link_fixed += 1

print('Files with fixed links: ' + str(link_fixed))

# Step 4: Rename files
renamed = 0
for old_fp, new_fp in rename_map.items():
    if os.path.exists(old_fp):
        os.rename(old_fp, new_fp)
        renamed += 1

print('Files renamed: ' + str(renamed))

# Step 5: Fix index.md - only link to Layer 2 nodes
layer2_nodes = {}
for root, dirs, files in os.walk(base):
    for f in files:
        if f == 'index.md' or not f.endswith('.md'):
            continue
        fp = os.path.join(root, f)
        with open(fp, 'r', encoding='utf8') as fh:
            content = fh.read()
        if 'type: indicator-category' in content:
            title = ''
            for line in content.split('\n'):
                if line.startswith('title:'):
                    title = line.split(':', 1)[1].strip()
                    break
            if root not in layer2_nodes:
                layer2_nodes[root] = []
            layer2_nodes[root].append((f.replace('.md', ''), title))

for root, dirs, files in os.walk(base):
    for f in files:
        if f != 'index.md':
            continue
        fp = os.path.join(root, f)
        with open(fp, 'r', encoding='utf8') as fh:
            content = fh.read()
        
        # Extract frontmatter
        fm_lines = []
        in_fm = False
        lines = content.split('\n')
        for line in lines:
            if line.strip() == '---':
                if not in_fm:
                    in_fm = True
                else:
                    break
            elif in_fm:
                fm_lines.append(line)
        
        title = ''
        for line in fm_lines:
            if line.startswith('title:'):
                title = line.split(':', 1)[1].strip()
                break
        
        # Build new body: only link to Layer 2 nodes
        dir_l2 = layer2_nodes.get(root, [])
        rel = os.path.relpath(root, base)
        new_body = '# ' + title + '\n\n## 技术指标\n\n'
        for bn, t in sorted(dir_l2):
            new_body += '- [[wiki/indicators/' + rel + '/' + bn + '|' + t + ']]\n'
        
        new_content = '---\n' + '\n'.join(fm_lines) + '\n---\n\n' + new_body
        
        with open(fp, 'w', encoding='utf8') as fh:
            fh.write(new_content)

count_idx = sum(1 for r, d, f in os.walk(base) for fn in f if fn == 'index.md')
print('index.md files rewritten')

# Step 6: Remove standard page cross-links from indicator nodes
removed = 0
for root, dirs, files in os.walk(base):
    for f in files:
        if f == 'index.md' or not f.endswith('.md'):
            continue
        fp = os.path.join(root, f)
        with open(fp, 'r', encoding='utf8') as fh:
            content = fh.read()
        
        old_content = content
        lines = content.split('\n')
        new_lines = [l for l in lines if 'wiki/standards/' not in l]
        new_content = '\n'.join(new_lines)
        
        if new_content != content:
            with open(fp, 'w', encoding='utf8') as fh:
                fh.write(new_content)
            removed += 1

print('Files with standard links removed: ' + str(removed))

# Verification
print('\n=== Verification ===')
fp = os.path.join(base, '工业生产资料', 'GB 175-2023', 'index.md')
with open(fp, 'r', encoding='utf8') as f:
    print(f.read())

print('=== 抗压强度.md ===')
fp = os.path.join(base, '工业生产资料', 'GB 175-2023', '抗压强度.md')
with open(fp, 'r', encoding='utf8') as f:
    print(f.read())

print('=== 3d.md ===')
fp = os.path.join(base, '工业生产资料', 'GB 175-2023', '3d.md')
with open(fp, 'r', encoding='utf8') as f:
    print(f.read())

print('=== 强度等级42.5 ≥42.5MPa.md ===')
fp = os.path.join(base, '工业生产资料', 'GB 175-2023', '强度等级42.5 ≥42.5MPa.md')
with open(fp, 'r', encoding='utf8') as f:
    print(f.read())
