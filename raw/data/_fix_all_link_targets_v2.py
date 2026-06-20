"""
Fix all wrong link targets - correct version.
The regex captures path including wiki/indicators/ prefix.
"""
import os
import re

base = 'D:\\knowledge-vault\\wiki\\indicators'

fixed = 0
for root, dirs, files in os.walk(base):
    for f in files:
        if f == 'index.md' or not f.endswith('.md'):
            continue
        fp = os.path.join(root, f)
        with open(fp, 'r', encoding='utf8') as fh:
            content = fh.read()
        
        if 'type: indicator-subcategory' not in content:
            continue
        
        old_content = content
        
        # Find all value links: [[wiki/indicators/.../target|display]]
        # The captured group already includes 'wiki/indicators/'
        links = re.findall(r'\[\[(wiki/indicators/[^\]|]+)\|([^\]]+)\]\]', content)
        
        for full_path, display in links:
            target_fname = full_path.split('/')[-1]
            if target_fname != display:
                old_link = '[[' + full_path + '|' + display + ']]'
                parts = full_path.split('/')
                parts[-1] = display
                new_path = '/'.join(parts)
                new_link = '[[' + new_path + '|' + display + ']]'
                content = content.replace(old_link, new_link)
                fixed += 1
        
        if content != old_content:
            with open(fp, 'w', encoding='utf8') as fh:
                fh.write(content)

print('Fixed link targets: ' + str(fixed))

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
                    print('  MISMATCH: ' + os.path.relpath(fp, base) + ' -> ' + full_path + '|' + display)

print('Remaining mismatches: ' + str(issues))

# Also verify all linked files exist
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
