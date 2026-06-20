"""
Fix links where / appears in the filename (should be fullwidth solidus ／).
The link path looks like: wiki/indicators/cat/std/通用 ≤5mg/100mL
But the actual file is: 通用 ≤5mg／100mL.md
"""
import os
import re

base = 'D:\\knowledge-vault\\wiki\\indicators'

# Find all files with fullwidth solidus
fw_files = {}
for root, dirs, files in os.walk(base):
    for f in files:
        if '\uff0f' in f:
            # Map: (root, display_name_with_slash) -> actual_name
            display_name = f.replace('\uff0f', '/')
            fw_files[(root, display_name)] = f

print('Files with fullwidth solidus: ' + str(len(fw_files)))

# For each file, find what display text it should have
# The display text is the filename without .md
fw_display_map = {}
for (root, display_name), actual_name in fw_files.items():
    fw_display_map[display_name.replace('.md', '')] = actual_name.replace('.md', '')

print('Display names: ' + str(list(fw_display_map.keys())))

# Fix links: find links where the last segment before |display has fewer segments
# than expected (because / was interpreted as path separator)
fixed = 0
for root, dirs, files in os.walk(base):
    for f in files:
        if not f.endswith('.md'):
            continue
        fp = os.path.join(root, f)
        with open(fp, 'r', encoding='utf8') as fh:
            content = fh.read()
        
        old_content = content
        
        # Find all wiki/indicators links
        links = re.findall(r'\[\[(wiki/indicators/[^\]]+)\]\]', content)
        
        for link in links:
            path = link.split('|')[0]
            display = link.split('|')[1] if '|' in link else ''
            
            # Count segments: wiki/indicators/cat/std/filename
            segments = path.split('/')
            # If we have more than 5 segments, the filename had / in it
            # Normal: wiki/indicators/cat/std/filename (5 segments)
            # Broken: wiki/indicators/cat/std/通用 ≤5mg/100mL (6 segments)
            if len(segments) > 5:
                # The filename was split by /
                # Reconstruct: segments[4:] joined with /
                broken_fname = '/'.join(segments[4:])
                # Check if this matches any fw_display_map entry
                if broken_fname in fw_display_map:
                    correct_fname = fw_display_map[broken_fname]
                    old_link = '[[' + link + ']]'
                    new_path = '/'.join(segments[:4]) + '/' + correct_fname
                    new_link = '[[' + new_path
                    if display:
                        new_link += '|' + display
                    new_link += ']]'
                    content = content.replace(old_link, new_link)
                    fixed += 1
                    print('Fixed: ' + broken_fname + ' -> ' + correct_fname)
        
        if content != old_content:
            with open(fp, 'w', encoding='utf8') as fh:
                fh.write(content)

print('\nFixed links: ' + str(fixed))

# Verify
print('\n=== Verification ===')
issues = 0
for root, dirs, files in os.walk(base):
    for f in files:
        if not f.endswith('.md'):
            continue
        fp = os.path.join(root, f)
        with open(fp, 'r', encoding='utf8') as fh:
            content = fh.read()
        
        links = re.findall(r'\[\[(wiki/indicators/[^\]|]+)\|([^\]]+)\]\]', content)
        for full_path, display in links:
            target_fname = full_path.split('/')[-1]
            if target_fname != display:
                issues += 1
                if issues <= 5:
                    print('  MISMATCH: ' + os.path.relpath(fp, base))
                    print('    target: ' + repr(target_fname))
                    print('    display: ' + repr(display))

print('Remaining mismatches: ' + str(issues))

# Verify all linked files exist
missing = 0
for root, dirs, files in os.walk(base):
    for f in files:
        if not f.endswith('.md'):
            continue
        fp = os.path.join(root, f)
        with open(fp, 'r', encoding='utf8') as fh:
            content = fh.read()
        
        links = re.findall(r'\[\[(wiki/indicators/[^\]|]+)\]\]', content)
        for full_path in links:
            target_path = os.path.join(base, full_path.replace('wiki/indicators/', ''))
            if not os.path.exists(target_path + '.md'):
                missing += 1
                if missing <= 5:
                    print('  MISSING: ' + full_path + ' (from ' + os.path.relpath(fp, base) + ')')

print('Missing target files: ' + str(missing))
