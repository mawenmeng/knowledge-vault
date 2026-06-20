"""Push new files to GitHub - handles existing files with sha"""
import urllib.request, urllib.parse, json, base64, os

TOKEN = 'PLACEHOLDER_TOKEN…8CkR'
OWNER = 'mawenmeng'
REPO = 'knowledge-vault'
API = f'https://api.github.com/repos/{OWNER}/{REPO}/contents'
HEADERS = {
    'Authorization': f'token {TOKEN}',
    'Content-Type': 'application/json',
    'User-Agent': 'python'
}
BASE = 'D:/knowledge-vault'

# 先获取所有现有文件的 sha
def get_existing_shas():
    req = urllib.request.Request(
        f'https://api.github.com/repos/{OWNER}/{REPO}/git/trees/master?recursive=1',
        headers={'Authorization': f'token {TOKEN}', 'User-Agent': 'python'}
    )
    resp = urllib.request.urlopen(req)
    data = json.loads(resp.read())
    shas = {}
    for item in data['tree']:
        if item['type'] == 'blob':
            shas[item['path']] = item['sha']
    return shas

existing = get_existing_shas()
print(f'Found {len(existing)} existing files')

# 需要推送的新文件（标准页面和指标页面）
new_dirs = ['wiki/standards', 'wiki/indicators']
files_to_push = []

for d in new_dirs:
    full_dir = os.path.join(BASE, d)
    if os.path.exists(full_dir):
        for f in sorted(os.listdir(full_dir)):
            if f.endswith('.md'):
                files_to_push.append(os.path.join(d, f).replace('\\', '/'))

# 也推送更新过的文件
updated = ['wiki/index.md', 'wiki/log.md', 'VAULT-INDEX.md', 
           'wiki/syntheses/2026-06-20-technical-indicators-knowledge-graph.md']
files_to_push.extend(updated)

print(f'Pushing {len(files_to_push)} files...')

for fp in files_to_push:
    full = os.path.join(BASE, fp)
    if not os.path.exists(full):
        print(f'SKIP: {fp}')
        continue
    
    with open(full, 'rb') as f:
        content = base64.b64encode(f.read()).decode()
    
    data = {'message': f'Update {fp}', 'content': content, 'branch': 'master'}
    
    # 如果文件已存在，添加 sha
    if fp in existing:
        data['sha'] = existing[fp]
    
    encoded_path = urllib.parse.quote(fp, safe='')
    url = f'{API}/{encoded_path}'
    req = urllib.request.Request(url, data=json.dumps(data).encode(), headers=HEADERS, method='PUT')
    
    try:
        resp = urllib.request.urlopen(req)
        print(f'OK: {fp}')
    except urllib.error.HTTPError as e:
        body = e.read().decode()[:150]
        print(f'FAIL {e.code}: {fp} -> {body}')
