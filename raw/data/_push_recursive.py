"""Push ALL files recursively to GitHub"""
import urllib.request, urllib.parse, json, base64, os

TOKEN = 'PLACEHOLDER_TOKEN'
OWNER = 'mawenmeng'
REPO = 'knowledge-vault'
API = f'https://api.github.com/repos/{OWNER}/{REPO}/contents'
HEADERS = {
    'Authorization': f'token {TOKEN}',
    'Content-Type': 'application/json',
    'User-Agent': 'python'
}
BASE = 'D:/knowledge-vault'

# Get existing shas
req = urllib.request.Request(
    f'https://api.github.com/repos/{OWNER}/{REPO}/git/trees/master?recursive=1',
    headers={'Authorization': f'token {TOKEN}', 'User-Agent': 'python'}
)
resp = urllib.request.urlopen(req)
data = json.loads(resp.read())
existing = {}
for item in data['tree']:
    if item['type'] == 'blob':
        existing[item['path']] = item['sha']
print(f'Found {len(existing)} existing files')

# Collect all files recursively
files_to_push = []
for root, dirs, files in os.walk(BASE):
    for f in files:
        if not f.endswith('.md'):
            continue
        full = os.path.join(root, f)
        rel = os.path.relpath(full, BASE).replace('\\', '/')
        # Skip .obsidian, .git, raw, .claude
        if rel.startswith('.obsidian/') or rel.startswith('.git/') or rel.startswith('raw/') or rel.startswith('.claude/'):
            continue
        files_to_push.append(rel)

print(f'Pushing {len(files_to_push)} files...')

pushed = 0
failed = 0
for fp in files_to_push:
    full = os.path.join(BASE, fp)
    with open(full, 'rb') as f:
        content = base64.b64encode(f.read()).decode()
    
    data = {'message': f'Update {fp}', 'content': content, 'branch': 'master'}
    if fp in existing:
        data['sha'] = existing[fp]
    
    encoded_path = urllib.parse.quote(fp, safe='')
    url = f'{API}/{encoded_path}'
    req = urllib.request.Request(url, data=json.dumps(data).encode(), headers=HEADERS, method='PUT')
    
    try:
        resp = urllib.request.urlopen(req)
        pushed += 1
        if pushed % 20 == 0:
            print(f'  Progress: {pushed}/{len(files_to_push)}')
    except urllib.error.HTTPError as e:
        body = e.read().decode()[:150]
        print(f'FAIL {e.code}: {fp} -> {body}')
        failed += 1

print(f'\nDone: {pushed} pushed, {failed} failed')
