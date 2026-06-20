"""
Fix links that use regular slash / instead of fullwidth solidus ／
to match actual filenames.
"""
import os
import re

base = 'D:\\knowledge-vault\\wiki\\indicators'

# Step 1: Find all files with fullwidth solidus in their name
fw_slash_files = {}  # (root, fw_name) -> actual_name
for root, dirs, files in os.walk(base):
    for f in files:
        if '\uff0f' in f:  # fullwidth solidus
            fw_slash_files[(root, f.replace('\uff0f', '/'))] = f

print('Files with fullwidth solidus: ' + str(len(fw_slash_files)))

# Step 2: Fix links - replace / with ／ in the last path segment
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
            # Check if the last segment contains /
            parts = link.split('|')[0]  # path only
            segments = parts.split('/')
            if len(segments) >= 5:
                last_seg = segments[-1]
                if '/' in last_seg:
                    # This link has a slash in the filename - fix it
                    fixed_last = last_seg.replace('/', '\uff0f')
                    old_link = '[[' + link + ']]'
                    new_link = link.replace(last_seg, fixed_last)
                    new_link = '[[' + new_link + ']]'
                    content = content.replace(old_link, new_link)
                    fixed += 1
        
        if content != old_content:
            with open(fp, 'w', encoding='utf8') as fh:
                fh.write(content)

print('Fixed links with slash in filename: ' + str(fixed))

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
