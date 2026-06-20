"""Comprehensive fix: ensure all hierarchical links are correct
L1 (standard) → L2 (indicator category) → L3 (subcategory) → L4 (value)
Each level links to its parent and children, but NOT to grandparent"""
import os, re

base = 'D:\\knowledge-vault\\wiki\\indicators'

def get_layer(content):
    if 'type: standard-node' in content:
        return 1
    if '技术指标值' in content or 'value-node' in content:
        return 4
    if '技术指标子类' in content:
        return 3
    if '技术指标类别' in content:
        return 2
    return 0

def get_title(content):
    m = re.search(r'^title: (.+)$', content, re.M)
    return m.group(1) if m else ''

def get_std_name(content):
    m = re.search(r'^std_name: (.+)$', content, re.M)
    return m.group(1) if m else ''

def get_referenced_standards(content):
    """Extract referenced standards from L1 content"""
    refs = []
    in_ref_section = False
    for line in content.split('\n'):
        if '## 引用标准' in line or '## 参考标准' in line:
            in_ref_section = True
            continue
        if in_ref_section:
            if line.startswith('## '):
                break
            # Look for wiki links to _references
            refs_in_line = re.findall(r'\[\[([^\]]+)\]\]', line)
            for r in refs_in_line:
                if '_references' in r:
                    refs.append(r)
    return refs

def add_link_if_missing(content, link_text):
    """Add a link to the content if it's not already present"""
    if link_text not in content:
        # Add after the title heading
        title_end = content.find('\n## ')
        if title_end > 0:
            next_section = content.find('\n## ', title_end + 1)
            if next_section > 0:
                insert_pos = next_section
            else:
                insert_pos = len(content)
            content = content[:insert_pos] + '\n- ' + link_text + content[insert_pos:]
        else:
            content += '\n- ' + link_text
    return content

def remove_link(content, link_text):
    """Remove a specific link from content"""
    pattern = r'\n- ' + re.escape(link_text) + r'\n?'
    content = re.sub(pattern, '\n', content)
    # Also try without newline
    content = content.replace('\n- ' + link_text, '')
    return content

total_fixes = 0

for root, dirs, files in os.walk(base):
    if '_references' in root:
        continue
    
    # Find Layer 1 file
    layer1_file = None
    layer1_title = None
    layer1_std_name = None
    for f in files:
        if f.endswith('.md'):
            fp = os.path.join(root, f)
            with open(fp, 'r', encoding='utf8') as fh:
                content = fh.read()
            if 'type: standard-node' in content:
                layer1_file = f
                layer1_title = get_title(content)
                layer1_std_name = get_std_name(content)
                break
    
    if not layer1_file:
        continue
    
    cat_dir = os.path.basename(os.path.dirname(root))
    std_dir = os.path.basename(root)
    prefix = 'wiki/indicators/' + cat_dir + '/' + std_dir + '/'
    
    # Collect all files by layer
    layer_files = {1: [], 2: [], 3: [], 4: []}
    for f in files:
        if not f.endswith('.md'):
            continue
        fp = os.path.join(root, f)
        with open(fp, 'r', encoding='utf8') as fh:
            content = fh.read()
        layer = get_layer(content)
        layer_files[layer].append(f)
    
    print(f'Processing {std_dir}: L1={len(layer_files[1])} L2={len(layer_files[2])} L3={len(layer_files[3])} L4={len(layer_files[4])}')
    
    for f in files:
        if not f.endswith('.md'):
            continue
        fp = os.path.join(root, f)
        with open(fp, 'r', encoding='utf8') as fh:
            content = fh.read()
        
        layer = get_layer(content)
        changed = False
        
        if layer == 1:
            # L1 should link to all L2 nodes
            for l2f in layer_files[2]:
                l2_title = l2f.replace('.md', '')
                link = '[[' + prefix + l2_title + '|' + l2_title + ']]'
                if link not in content:
                    # Add to the 技术指标 section
                    tech_section = content.find('## 技术指标')
                    if tech_section > 0:
                        insert_pos = content.find('\n', tech_section) + 1
                        content = content[:insert_pos] + '\n- ' + link + content[insert_pos:]
                    else:
                        content += '\n- ' + link
                    changed = True
                    total_fixes += 1
                    print(f'  L1 {f}: added link to L2 {l2f}')
            
            # Add standard name link
            if layer1_std_name:
                std_name_link = '[[' + prefix + layer1_title + '|' + layer1_std_name + ']]'
                if std_name_link not in content:
                    # Add near the title
                    title_line = content.find('# ' + layer1_title)
                    if title_line > 0:
                        insert_pos = content.find('\n', title_line) + 1
                        content = content[:insert_pos] + '\n**标准名称：** ' + std_name_link + '\n' + content[insert_pos:]
                        changed = True
                        total_fixes += 1
                        print(f'  L1 {f}: added standard name link')
        
        elif layer == 2:
            # L2 should link to L1
            l1_link = '[[' + prefix + layer1_title + '|' + layer1_title + ']]'
            if l1_link not in content:
                # Add after frontmatter
                frontmatter_end = content.find('---', 3)
                if frontmatter_end > 0:
                    insert_pos = content.find('\n', frontmatter_end + 3) + 1
                    content = content[:insert_pos] + '\n**所属标准：** ' + l1_link + '\n' + content[insert_pos:]
                    changed = True
                    total_fixes += 1
                    print(f'  L2 {f}: added link to L1 {layer1_file}')
            
            # L2 should link to all L3 nodes
            for l3f in layer_files[3]:
                l3_title = l3f.replace('.md', '')
                link = '[[' + prefix + l3_title + '|' + l3_title + ']]'
                if link not in content:
                    # Add to 子指标 section
                    sub_section = content.find('## 子指标')
                    if sub_section > 0:
                        insert_pos = content.find('\n', sub_section) + 1
                        content = content[:insert_pos] + '\n- ' + link + content[insert_pos:]
                    else:
                        content += '\n- ' + link
                    changed = True
                    total_fixes += 1
                    print(f'  L2 {f}: added link to L3 {l3f}')
        
        elif layer == 3:
            # L3 should link to L2 (parent)
            for l2f in layer_files[2]:
                l2_title = l2f.replace('.md', '')
                link = '[[' + prefix + l2_title + '|' + l2_title + ']]'
                if link not in content:
                    frontmatter_end = content.find('---', 3)
                    if frontmatter_end > 0:
                        insert_pos = content.find('\n', frontmatter_end + 3) + 1
                        content = content[:insert_pos] + '\n**所属类别：** ' + link + '\n' + content[insert_pos:]
                    else:
                        content = '\n**所属类别：** ' + link + '\n' + content
                    changed = True
                    total_fixes += 1
                    print(f'  L3 {f}: added link to L2 {l2f}')
            
            # L3 should link to all L4 nodes
            for l4f in layer_files[4]:
                l4_title = l4f.replace('.md', '')
                link = '[[' + prefix + l4_title + '|' + l4_title + ']]'
                if link not in content:
                    sub_section = content.find('## 指标值')
                    if sub_section > 0:
                        insert_pos = content.find('\n', sub_section) + 1
                        content = content[:insert_pos] + '\n- ' + link + content[insert_pos:]
                    else:
                        content += '\n- ' + link
                    changed = True
                    total_fixes += 1
                    print(f'  L3 {f}: added link to L4 {l4f}')
        
        elif layer == 4:
            # L4 should link to L3 (parent) if exists, else L2
            if layer_files[3]:
                for l3f in layer_files[3]:
                    l3_title = l3f.replace('.md', '')
                    link = '[[' + prefix + l3_title + '|' + l3_title + ']]'
                    if link not in content:
                        frontmatter_end = content.find('---', 3)
                        if frontmatter_end > 0:
                            insert_pos = content.find('\n', frontmatter_end + 3) + 1
                            content = content[:insert_pos] + '\n**所属子类：** ' + link + '\n' + content[insert_pos:]
                        else:
                            content = '\n**所属子类：** ' + link + '\n' + content
                        changed = True
                        total_fixes += 1
                        print(f'  L4 {f}: added link to L3 {l3f}')
            
            # Remove L2 links from L4 (should only link to L3)
            for l2f in layer_files[2]:
                l2_title = l2f.replace('.md', '')
                link = '[[' + prefix + l2_title + '|' + l2_title + ']]'
                if link in content:
                    content = content.replace('\n- ' + link, '')
                    content = content.replace(link, '')
                    changed = True
                    total_fixes += 1
                    print(f'  L4 {f}: removed redundant L2 link to {l2f}')
        
        if changed:
            with open(fp, 'w', encoding='utf8') as fh:
                fh.write(content)

print(f'\nTotal fixes: {total_fixes}')
