import urllib.request, urllib.parse, json, base64, os, subprocess, re

with open('D:\\knowledge-vault\\raw\\data\\_push_to_github_v2.py', 'r', encoding='utf8') as f:
    script = f.read()

m = re.search(r"TOKEN = '([^']+)'", script)
token = m.group(1) if m else None
print(f'Token: {token[:5]}...{token[-4:]}')

OWNER = 'mawenmeng'
REPO = 'knowledge-vault'
API = f'https://api.github.com/repos/{OWNER}/{REPO}/contents'
HEADERS = {
    'Authorization': f'token {token}',
    'Content-Type': 'application/json',
    'User-Agent': 'python'
}
BASE = 'D:/knowledge-vault'

# Get changed files - use --name-only -z to handle special chars
result = subprocess.run(['git', 'diff', '--name-only', '-z', 'HEAD~1', 'HEAD'], capture_output=True, cwd=BASE)
files = [f for f in result.stdout.decode('utf-8').strip().split('\0') if f]
print(f'Changed files: {len(files)}')

# Get existing shas
req = urllib.request.Request(
    f'https://api.github.com/repos/{OWNER}/{REPO}/git/trees/master?recursive=1',
    headers={'Authorization': f'token {token}', 'User-Agent': 'python'}
)
resp = urllib.request.urlopen(req)
data = json.loads(resp.read())
existing = {}
for item in data['tree']:
    if item['type'] == 'blob':
        existing[item['path']] = item['sha']
print(f'Existing files: {len(existing)}')

pushed = 0
failed = 0
for fp in files:
    full = BASE + '/' + fp
    if not os.path.exists(full):
        print(f'SKIP (not found): {fp}')
        continue
    
    with open(full, 'rb') as f:
        content = base64.b64encode(f.read()).decode('ascii')
    
    payload = {'message': f'Update {fp}', 'content': content, 'branch': 'master'}
    if fp in existing:
        payload['sha'] = existing[fp]
    
    encoded_path = urllib.parse.quote(fp, safe='')
    url = f'{API}/{encoded_path}'
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=HEADERS, method='PUT')
    
    try:
        resp = urllib.request.urlopen(req)
        pushed += 1
        if pushed % 10 == 0:
            print(f'  Progress: {pushed}/{len(files)}')
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8')[:200]
        print(f'FAIL {e.code}: {fp} -> {body}')
        failed += 1

print(f'Done: {pushed} pushed, {failed} failed')
