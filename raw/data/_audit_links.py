"""Audit all indicator files for correct hierarchical linking"""
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

issues = []
for root, dirs, files in os.walk(base):
    if '_references' in root:
        continue
    
    # Find Layer 1 file
    layer1_file = None
    layer1_title = None
    for f in files:
        if f.endswith('.md'):
            fp = os.path.join(root, f)
            with open(fp, 'r', encoding='utf8') as fh:
                content = fh.read()
            if 'type: standard-node' in content:
                layer1_file = f
                m = re.search(r'^title: (.+)$', content, re.M)
                layer1_title = m.group(1) if m else f.replace('.md', '')
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
    
    for f in files:
        if not f.endswith('.md'):
            continue
        fp = os.path.join(root, f)
        with open(fp, 'r', encoding='utf8') as fh:
            content = fh.read()
        
        layer = get_layer(content)
        links = re.findall(r'\[\[([^\]]+)\]\]', content)
        rel = os.path.relpath(fp, base)
        
        if layer == 1:
            # L1 should link to L2 nodes
            for l2f in layer_files[2]:
                l2_link = '[[' + prefix + l2f + '|' + l2f.replace('.md', '') + ']]'
                if l2_link not in content:
                    issues.append('L1 ' + rel + ': missing link to L2 ' + l2f)
        
        elif layer == 2:
            # L2 should link to L1
            l1_link = '[[' + prefix + layer1_file + '|' + layer1_title + ']]'
            if l1_link not in content:
                issues.append('L2 ' + rel + ': missing link to L1 ' + layer1_file)
            
            # L2 should link to L3
            for l3f in layer_files[3]:
                l3_link = '[[' + prefix + l3f + '|' + l3f.replace('.md', '') + ']]'
                if l3_link not in content:
                    issues.append('L2 ' + rel + ': missing link to L3 ' + l3f)
        
        elif layer == 3:
            # L3 should link to L2
            for l2f in layer_files[2]:
                l2_link = '[[' + prefix + l2f + '|' + l2f.replace('.md', '') + ']]'
                if l2_link not in content:
                    issues.append('L3 ' + rel + ': missing link to L2 ' + l2f)
            
            # L3 should link to L4
            for l4f in layer_files[4]:
                l4_link = '[[' + prefix + l4f + '|' + l4f.replace('.md', '') + ']]'
                if l4_link not in content:
                    issues.append('L3 ' + rel + ': missing link to L4 ' + l4f)
        
        elif layer == 4:
            # L4 should link to L3 if exists, else L2
            if layer_files[3]:
                for l3f in layer_files[3]:
                    l3_link = '[[' + prefix + l3f + '|' + l3f.replace('.md', '') + ']]'
                    if l3_link not in content:
                        issues.append('L4 ' + rel + ': missing link to L3 ' + l3f)
            elif layer_files[2]:
                for l2f in layer_files[2]:
                    l2_link = '[[' + prefix + l2f + '|' + l2f.replace('.md', '') + ']]'
                    if l2_link not in content:
                        issues.append('L4 ' + rel + ': missing link to L2 ' + l2f)

if issues:
    print('Found ' + str(len(issues)) + ' issues:')
    for i in issues:
        print('  ' + i)
else:
    print('All links look correct!')
