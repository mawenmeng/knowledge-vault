"""Push knowledge-vault to GitHub via API"""
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

files = [
    'README.md', 'VAULT-INDEX.md', 'CLAUDE.md',
    'wiki/index.md', 'wiki/log.md',
    'wiki/syntheses/2026-06-20-technical-indicators-knowledge-graph.md',
    'wiki/syntheses/2026-06-20-national-standards-comprehensive-report.md',
    'wiki/concepts/national-standards-gb.md',
    'wiki/concepts/肥料.md',
    'wiki/concepts/水泥.md',
    'wiki/concepts/聚乙烯（PE）管材.md',
    'wiki/concepts/液化天然气（LNG）.md',
    'wiki/concepts/液化石油气（LPG）.md',
    'wiki/concepts/电线电缆试验方法.md',
    'wiki/entities/SAC-TC105.md',
    'wiki/entities/SAC-TC213.md',
    'wiki/entities/CPCIF.md',
    'wiki/sources/2026-06-20-national-standards-collection.md',
]

for fp in files:
    full = os.path.join(BASE, fp)
    if not os.path.exists(full):
        print(f'SKIP (not found): {fp}')
        continue
    with open(full, 'rb') as f:
        content = base64.b64encode(f.read()).decode()
    data = json.dumps({
        'message': f'Add {fp}',
        'content': content,
        'branch': 'master'
    }).encode()
    url = f'{API}/{urllib.parse.quote(fp.replace(os.sep, "/"), safe="/")}'
    req = urllib.request.Request(url, data=data, headers=HEADERS, method='PUT')
    try:
        resp = urllib.request.urlopen(req)
        print(f'OK: {fp}')
    except urllib.error.HTTPError as e:
        body = e.read().decode()[:150]
        print(f'FAIL {e.code}: {fp} -> {body}')
