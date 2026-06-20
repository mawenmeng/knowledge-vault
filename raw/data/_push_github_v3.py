"""Push new standard/indicator pages to GitHub"""
import urllib.request, urllib.parse, json, base64, os

# 请替换为你的完整 token
TOKEN = 'ghp_jf…8CkR'

OWNER = 'mawenmeng'
REPO = 'knowledge-vault'
API = f'https://api.github.com/repos/{OWNER}/{REPO}/contents'
HEADERS = {
    'Authorization': f'token {TOKEN}',
    'Content-Type': 'application/json',
    'User-Agent': 'python'
}
BASE = 'D:/knowledge-vault'

# 获取现有文件 sha
req = urllib.request.Request(
    f'https://api.github.com/repos/{OWNER}/{REPO}/git/trees/master?recursive=1',
    headers={'Authorization': f'token {TOKEN}', 'User-Agent': 'python'}
)
resp = urllib.request.urlopen(req)
data = json.loads(resp.read())
existing = {item['path']: item['sha'] for item in data['tree'] if item['type'] == 'blob'}
print(f'Existing files: {len(existing)}')

# 新文件：标准页面 + 指标页面
new_files = []
for d in ['wiki/standards', 'wiki/indicators']:
    full_dir = os.path.join(BASE, d)
    for f in sorted(os.listdir(full_dir)):
        if f.endswith('.md'):
            new_files.append(f'{d}/{f}')

# 更新的文件
updated = ['wiki/index.md', 'wiki/log.md', 'VAULT-INDEX.md',
           'wiki/syntheses/2026-06-20-technical-indicators-knowledge-graph.md']

all_files = new_files + updated
print(f'Total to push: {len(all_files)}')

success = 0
fail = 0
for fp in all_files:
    full = os.path.join(BASE, fp)
    if not os.path.exists(full):
        continue
    
    with open(full, 'rb') as f:
        content = base64.b64encode(f.read()).decode()
    
    data = {'message': f'Update {fp}', 'content': content, 'branch': 'master'}
    if fp in existing:
        data['sha'] = existing[fp]
    
    url = f'{API}/{urllib.parse.quote(fp, safe="")}'
    req = urllib.request.Request(url, data=json.dumps(data).encode(), headers=HEADERS, method='PUT')
    
    try:
        resp = urllib.request.urlopen(req)
        success += 1
        print(f'OK [{success}]: {fp}')
    except urllib.error.HTTPError as e:
        fail += 1
        body = e.read().decode()[:100]
        print(f'FAIL [{fail}]: {fp} -> {e.code}')

print(f'\nDone: {success} OK, {fail} FAIL')
