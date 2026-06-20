"""Smart fix: Fix hierarchical links based on existing correct relationships.
Only fixes truly missing links (L2→L1, L3→L2, L3→L4, L4→L3).
Does NOT create spurious links between unrelated nodes."""
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

def get_links(content):
    return re.findall(r'\[\[([^\]]+)\]\]', content)

def add_link_after_frontmatter(content, link_text):
    """Add a link after frontmatter if not already present"""
    if link_text in content:
        return content, False
    frontmatter_end = content.find('---', 3)
    if frontmatter_end > 0:
        insert_pos = content.find('\n', frontmatter_end + 3) + 1
        content = content[:insert_pos] + '\n' + link_text + '\n' + content[insert_pos:]
    else:
        content = '\n' + link_text + '\n' + content
    return content, True

def add_link_in_section(content, section_name, link_text):
    """Add a link under a specific section heading"""
    if link_text in content:
        return content, False
    section_pos = content.find('## ' + section_name)
    if section_pos > 0:
        insert_pos = content.find('\n', section_pos) + 1
        content = content[:insert_pos] + '\n- ' + link_text + content[insert_pos:]
        return content, True
    # Fallback: add at end
    content += '\n- ' + link_text
    return content, True

total_fixes = 0

for root, dirs, files in os.walk(base):
    if '_references' in root:
        continue
    
    # Find L1 file
    l1_file = None
    for f in files:
        if f.endswith('.md'):
            fp = os.path.join(root, f)
            with open(fp, 'r', encoding='utf8') as fh:
                content = fh.read()
            if 'type: standard-node' in content:
                l1_file = f
                break
    
    if not l1_file:
        continue
    
    cat_dir = os.path.basename(os.path.dirname(root))
    std_dir = os.path.basename(root)
    prefix = 'wiki/indicators/' + cat_dir + '/' + std_dir + '/'
    
    # Classify all files by layer
    l1_content_map = {}
    l2_files = []
    l3_files = []
    l4_files = []
    
    for f in files:
        if not f.endswith('.md'):
            continue
        fp = os.path.join(root, f)
        with open(fp, 'r', encoding='utf8') as fh:
            content = fh.read()
        layer = get_layer(content)
        if layer == 1:
            l1_content_map[f] = content
        elif layer == 2:
            l2_files.append(f)
        elif layer == 3:
            l3_files.append(f)
        elif layer == 4:
            l4_files.append(f)
    
    if not l2_files:
        continue
    
    print(f'=== {std_dir} ===')
    
    # Build parent-child relationships from existing links
    # L2 → L3: which L3 does each L2 link to?
    l2_to_l3 = {}
    for l2f in l2_files:
        fp = os.path.join(root, l2f)
        with open(fp, 'r', encoding='utf8') as fh:
            content = fh.read()
        links = get_links(content)
        children = []
        for l3f in l3_files:
            l3_title = l3f.replace('.md', '')
            expected_link = '[[' + prefix + l3_title + '|' + l3_title + ']]'
            if expected_link in content:
                children.append(l3f)
        l2_to_l3[l2f] = children
    
    # L3 → L2: which L2 does each L3 link to?
    l3_to_l2 = {}
    for l3f in l3_files:
        fp = os.path.join(root, l3f)
        with open(fp, 'r', encoding='utf8') as fh:
            content = fh.read()
        links = get_links(content)
        parents = []
        for l2f in l2_files:
            l2_title = l2f.replace('.md', '')
            expected_link = '[[' + prefix + l2_title + '|' + l2_title + ']]'
            if expected_link in content:
                parents.append(l2f)
        l3_to_l2[l3f] = parents
    
    # L3 → L4: which L4 does each L3 link to?
    l3_to_l4 = {}
    for l3f in l3_files:
        fp = os.path.join(root, l3f)
        with open(fp, 'r', encoding='utf8') as fh:
            content = fh.read()
        links = get_links(content)
        children = []
        for l4f in l4_files:
            l4_title = l4f.replace('.md', '')
            expected_link = '[[' + prefix + l4_title + '|' + l4_title + ']]'
            if expected_link in content:
                children.append(l4f)
        l3_to_l4[l3f] = children
    
    # L4 → L3: which L3 does each L4 link to?
    l4_to_l3 = {}
    for l4f in l4_files:
        fp = os.path.join(root, l4f)
        with open(fp, 'r', encoding='utf8') as fh:
            content = fh.read()
        links = get_links(content)
        parents = []
        for l3f in l3_files:
            l3_title = l3f.replace('.md', '')
            expected_link = '[[' + prefix + l3_title + '|' + l3_title + ']]'
            if expected_link in content:
                parents.append(l3f)
        l4_to_l3[l4f] = parents
    
    # L4 → L2: which L2 does each L4 link to? (these are WRONG links that should be L3)
    l4_to_l2 = {}
    for l4f in l4_files:
        fp = os.path.join(root, l4f)
        with open(fp, 'r', encoding='utf8') as fh:
            content = fh.read()
        links = get_links(content)
        parents = []
        for l2f in l2_files:
            l2_title = l2f.replace('.md', '')
            expected_link = '[[' + prefix + l2_title + '|' + l2_title + ']]'
            if expected_link in content:
                parents.append(l2f)
        l4_to_l2[l4f] = parents
    
    # --- FIX 1: L2 → L1 (add backlink to L1 if missing) ---
    l1_title = l1_file.replace('.md', '')
    l1_link = '[[' + prefix + l1_title + '|' + l1_title + ']]'
    
    for l2f in l2_files:
        fp = os.path.join(root, l2f)
        with open(fp, 'r', encoding='utf8') as fh:
            content = fh.read()
        
        if l1_link not in content:
            content, changed = add_link_after_frontmatter(content, '**所属标准：** ' + l1_link)
            if changed:
                with open(fp, 'w', encoding='utf8') as fh:
                    fh.write(content)
                total_fixes += 1
                print(f'  FIX: L2 {l2f} → added backlink to L1 {l1_file}')
    
    # --- FIX 2: L3 → L2 (add parent L2 link if missing) ---
    for l3f in l3_files:
        fp = os.path.join(root, l3f)
        with open(fp, 'r', encoding='utf8') as fh:
            content = fh.read()
        
        # Find the correct L2 parent from l2_to_l3
        correct_parents = []
        for l2f, children in l2_to_l3.items():
            if l3f in children:
                correct_parents.append(l2f)
        
        if not correct_parents:
            # Try reverse: find L2 that this L3 should belong to
            # Look at the L3 title - if it matches a subcategory pattern
            l3_title = l3f.replace('.md', '')
            for l2f in l2_files:
                l2_title = l2f.replace('.md', '')
                expected_link = '[[' + prefix + l2_title + '|' + l2_title + ']]'
                if expected_link in content:
                    correct_parents.append(l2f)
        
        if correct_parents:
            for parent_l2 in correct_parents:
                l2_title = parent_l2.replace('.md', '')
                expected_link = '[[' + prefix + l2_title + '|' + l2_title + ']]'
                if expected_link not in content:
                    content, changed = add_link_after_frontmatter(content, '**所属类别：** ' + expected_link)
                    if changed:
                        with open(fp, 'w', encoding='utf8') as fh:
                            fh.write(content)
                        total_fixes += 1
                        print(f'  FIX: L3 {l3f} → added backlink to L2 {parent_l2}')
    
    # --- FIX 3: L3 → L4 (add child L4 links if missing) ---
    for l3f in l3_files:
        fp = os.path.join(root, l3f)
        with open(fp, 'r', encoding='utf8') as fh:
            content = fh.read()
        
        # Find L4 children from l4_to_l3 (reverse lookup)
        correct_children = []
        for l4f, parents in l4_to_l3.items():
            if l3f in parents:
                correct_children.append(l4f)
        
        # Also add L4s that already link to this L3's L2 parent (wrong links to fix)
        # But only if they don't already have a correct L3 parent
        for l4f in l4_files:
            if l4f not in correct_children:
                l4_parents = l4_to_l3.get(l4f, [])
                if not l4_parents:
                    # This L4 has no L3 parent - it might need one
                    # Check if it links to the same L2 as this L3
                    l4_l2_parents = l4_to_l2.get(l4f, [])
                    l3_l2_parents = l2_to_l3.get(l3f, [])  # This doesn't make sense
                    # Instead, find which L2 this L3 belongs to
                    for l2f in l2_files:
                        if l3f in l2_to_l3.get(l2f, []):
                            if l2f in l4_l2_parents:
                                correct_children.append(l4f)
                                break
        
        for child_l4 in correct_children:
            l4_title = child_l4.replace('.md', '')
            expected_link = '[[' + prefix + l4_title + '|' + l4_title + ']]'
            if expected_link not in content:
                content, changed = add_link_in_section(content, '指标值', expected_link)
                if changed:
                    with open(fp, 'w', encoding='utf8') as fh:
                        fh.write(content)
                    total_fixes += 1
                    print(f'  FIX: L3 {l3f} → added link to L4 {child_l4}')
    
    # --- FIX 4: L4 → L3 (replace L2 links with L3 links) ---
    for l4f in l4_files:
        fp = os.path.join(root, l4f)
        with open(fp, 'r', encoding='utf8') as fh:
            content = fh.read()
        
        # Find correct L3 parents
        correct_parents = []
        for l3f in l3_files:
            l3_title = l3f.replace('.md', '')
            expected_link = '[[' + prefix + l3_title + '|' + l3_title + ']]'
            if expected_link in content:
                correct_parents.append(l3f)
        
        # If no L3 parent found, check if this L4 links to an L2
        if not correct_parents:
            l4_l2_parents = l4_to_l2.get(l4f, [])
            if l4_l2_parents:
                # Find L3 children of those L2 parents
                for l2f in l4_l2_parents:
                    l3_children = l2_to_l3.get(l2f, [])
                    for l3f in l3_children:
                        l3_title = l3f.replace('.md', '')
                        expected_link = '[[' + prefix + l3_title + '|' + l3_title + ']]'
                        if expected_link not in content:
                            # Remove the L2 link
                            l2_title = l2f.replace('.md', '')
                            l2_link = '[[' + prefix + l2_title + '|' + l2_title + ']]'
                            content = content.replace('\n- ' + l2_link, '')
                            content = content.replace(l2_link, '')
                            # Add L3 link
                            content, _ = add_link_after_frontmatter(content, '**所属子类：** ' + expected_link)
                            correct_parents.append(l3f)
                            with open(fp, 'w', encoding='utf8') as fh:
                                fh.write(content)
                            total_fixes += 1
                            print(f'  FIX: L4 {l4f} → replaced L2 link with L3 link to {l3f}')
                            break
                    if correct_parents:
                        break
        
        # If still no L3 parent, try to find from L3→L4 links
        if not correct_parents:
            for l3f, children in l3_to_l4.items():
                if l4f in children:
                    l3_title = l3f.replace('.md', '')
                    expected_link = '[[' + prefix + l3_title + '|' + l3_title + ']]'
                    if expected_link not in content:
                        content, changed = add_link_after_frontmatter(content, '**所属子类：** ' + expected_link)
                        if changed:
                            with open(fp, 'w', encoding='utf8') as fh:
                                fh.write(content)
                            total_fixes += 1
                            print(f'  FIX: L4 {l4f} → added link to L3 {l3f}')
                    correct_parents.append(l3f)
                    break

print(f'\nTotal fixes: {total_fixes}')
