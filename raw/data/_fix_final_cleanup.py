"""Final cleanup:
1. L1 nodes: move references after indicator links (not before)
2. L4 nodes: clean up stray '所属子类' labels
3. L3 nodes: clean up duplicate backlinks
"""
import os, re

base = 'D:\\knowledge-vault\\wiki\\indicators'

total = 0

# ========== 1. Fix L1 nodes: reorder ==========
print("=== 1. Fixing L1 node ordering ===")
for root, dirs, files in os.walk(base):
    if '_references' in root:
        continue
    for f in files:
        if not f.endswith('.md'):
            continue
        fp = os.path.join(root, f)
        with open(fp, 'r', encoding='utf8') as fh:
            content = fh.read()
        if 'type: standard-node' not in content:
            continue
        
        # Check if references section is between ## 技术指标 and the actual links
        tech_idx = content.find('## 技术指标')
        ref_idx = content.find('## 引用标准')
        
        if tech_idx > 0 and ref_idx > 0:
            # Find the end of references section
            ref_end = content.find('\n## ', ref_idx + 1)
            if ref_end < 0:
                ref_end = len(content)
            
            ref_section = content[ref_idx:ref_end]
            
            # Find the end of tech section
            tech_end = content.find('\n## ', tech_idx + 1)
            if tech_end < 0:
                tech_end = len(content)
            
            # If references is between tech header and tech content
            if ref_idx > tech_idx and ref_idx < tech_end:
                # Move references to after tech section
                content = content[:ref_idx] + content[ref_end:]
                # Find new tech end
                new_tech_end = content.find('\n## ', tech_idx + 1)
                if new_tech_end < 0:
                    new_tech_end = len(content)
                # Insert references after tech section
                content = content[:new_tech_end] + '\n\n' + ref_section.strip() + '\n' + content[new_tech_end:]
                
                with open(fp, 'w', encoding='utf8') as fh:
                    fh.write(content)
                total += 1
                print(f'  Fixed: {os.path.basename(root)}/{f}')

# ========== 2. Clean up L4 nodes ==========
print("\n=== 2. Cleaning up L4 nodes ===")
for root, dirs, files in os.walk(base):
    for f in files:
        if not f.endswith('.md'):
            continue
        fp = os.path.join(root, f)
        with open(fp, 'r', encoding='utf8') as fh:
            content = fh.read()
        if 'type: indicator-value' not in content:
            continue
        
        modified = False
        
        # Remove stray "**所属子类：** " with nothing after it
        content = re.sub(r'\*\*所属子类：\*\* \n', '', content)
        if '**所属子类：**' in content and '[[' not in content[content.find('**所属子类：**'):content.find('**所属子类：**')+50]:
            content = re.sub(r'\*\*所属子类：\*\* \[\[[^\]]*\]\]\n', '', content)
            modified = True
        
        # Remove empty "**所属子类：**" lines
        content = re.sub(r'^\*\*所属子类：\*\*\s*$', '', content, flags=re.M)
        
        if modified:
            with open(fp, 'w', encoding='utf8') as fh:
                fh.write(content)
            total += 1

# ========== 3. Clean up L3 nodes: remove duplicate backlinks ==========
print("\n=== 3. Cleaning up L3 nodes ===")
for root, dirs, files in os.walk(base):
    for f in files:
        if not f.endswith('.md'):
            continue
        fp = os.path.join(root, f)
        with open(fp, 'r', encoding='utf8') as fh:
            content = fh.read()
        if 'type: indicator-subcategory' not in content:
            continue
        
        modified = False
        
        # Find all backlinks (lines starting with **所属类别：** or **指标类别：**)
        backlinks = re.findall(r'(\*\*(?:所属类别|指标类别)：\*\* \[\[[^\]]+\]\])\n', content)
        if len(backlinks) > 1:
            # Keep only unique ones
            seen = set()
            for bl in backlinks:
                if bl in seen:
                    content = content.replace(bl + '\n', '')
                    modified = True
                seen.add(bl)
        
        # Clean up blank lines
        if modified:
            content = re.sub(r'\n{3,}', '\n\n', content)
            with open(fp, 'w', encoding='utf8') as fh:
                fh.write(content)
            total += 1

print(f"\nTotal: {total} fixes")
