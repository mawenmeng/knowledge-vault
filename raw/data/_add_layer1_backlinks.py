import os, re

base = 'D:\\knowledge-vault\\wiki\\indicators'

updated = 0
for root, dirs, files in os.walk(base):
    if '_references' in root:
        continue
    
    # Find Layer 1 file (has type: standard-node)
    layer1_file = None
    for f in files:
        if f.endswith('.md'):
            fp = os.path.join(root, f)
            with open(fp, 'r', encoding='utf8') as fh:
                content = fh.read()
            if 'type: standard-node' in content:
                layer1_file = f
                break
    
    if not layer1_file:
        continue
    
    cat_dir = os.path.basename(os.path.dirname(root))
    std_dir = os.path.basename(root)
    rel_prefix = 'wiki/indicators/' + cat_dir + '/' + std_dir + '/'
    layer1_title = layer1_file.replace('.md', '')
    
    for f in files:
        if f == layer1_file or not f.endswith('.md'):
            continue
        fp = os.path.join(root, f)
        with open(fp, 'r', encoding='utf8') as fh:
            content = fh.read()
        
        # Only process Layer 2 nodes (技术指标类别)
        if '技术指标类别' not in content:
            continue
        
        # Check if already links to Layer 1
        link_pattern = '[[' + rel_prefix + layer1_file + '|'
        if link_pattern in content:
            continue
        
        # Add backlink after frontmatter
        frontmatter_end = content.find('---', 3)
        if frontmatter_end > 0:
            insert_pos = content.find('\n', frontmatter_end + 3) + 1
        else:
            insert_pos = 0
        
        backlink = '\n**所属标准：** [[' + rel_prefix + layer1_file + '|' + layer1_title + ']]\n'
        
        # Insert after the title heading
        title_end = content.find('\n## ', insert_pos)
        if title_end > 0:
            new_content = content[:title_end] + backlink + content[title_end:]
        else:
            new_content = content + backlink
        
        with open(fp, 'w', encoding='utf8') as fh:
            fh.write(new_content)
        updated += 1
        print('Added backlink in ' + os.path.relpath(fp, base) + ' -> ' + layer1_file)

print('\nUpdated ' + str(updated) + ' Layer 2 files')
