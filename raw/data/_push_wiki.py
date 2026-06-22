"""Push wiki files from local disk to GitHub via API"""
import urllib.request, urllib.parse, json, base64, os

TOKEN = 'PLACEHOLDER_TOKEN'
OWNER = 'mawenmeng'
REPO = 'knowledge-vault'
HEADERS = {
    'Authorization': f'token {TOKEN}',
    'Content-Type': 'application/json',
    'User-Agent': 'python'
}
BASE = 'D:/knowledge-vault'

# Get existing file SHAs
def get_existing_shas():
    url = f'https://api.github.com/repos/{OWNER}/{REPO}/git/trees/master?recursive=1'
    req = urllib.request.Request(url, headers={'Authorization': f'token {TOKEN}', 'User-Agent': 'python'})
    resp = urllib.request.urlopen(req, timeout=30)
    data = json.loads(resp.read())
    shas = {}
    for item in data['tree']:
        if item['type'] == 'blob':
            shas[item['path']] = item['sha']
    return shas

print("Fetching existing file SHAs...")
existing = get_existing_shas()
print(f"Found {len(existing)} existing files")

# Collect only wiki/ files and root files
files_to_push = []
for root, dirs, files in os.walk(BASE):
    for f in files:
        full = os.path.join(root, f)
        rel = os.path.relpath(full, BASE).replace('\\', '/')
        # Only push wiki/ and root-level files
        if rel.startswith('wiki/') or rel in ('index.md', 'README.md', 'CLAUDE.md', 'VAULT-INDEX.md'):
            files_to_push.append(rel)

print(f"Files to push: {len(files_to_push)}")

# Push files
success = 0
failed = 0
for i, rel_path in enumerate(files_to_push):
    full_path = os.path.join(BASE, rel_path)
    with open(full_path, 'rb') as f:
        content_b64 = base64.b64encode(f.read()).decode('utf-8')
    
    data = {
        'message': f'Update {rel_path}',
        'content': content_b64,
        'sha': existing.get(rel_path)
    }
    
    url = f'https://api.github.com/repos/{OWNER}/{REPO}/contents/{urllib.parse.quote(rel_path, safe="")}'
    req = urllib.request.Request(url, json.dumps(data).encode('utf-8'), HEADERS, method='PUT')
    
    try:
        resp = urllib.request.urlopen(req, timeout=30)
        success += 1
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8')[:100]
        print(f"  FAIL: {rel_path} ({e.code} {body})")
        failed += 1
    except Exception as e:
        print(f"  ERROR: {rel_path} ({e})")
        failed += 1
    
    if (i+1) % 10 == 0:
        print(f"  Progress: {i+1}/{len(files_to_push)} (OK: {success}, FAIL: {failed})")

print(f"\nDone! OK: {success}, FAIL: {failed}")
