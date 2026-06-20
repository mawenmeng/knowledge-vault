import os, json, base64, requests, subprocess, re

os.chdir('D:\\knowledge-vault')

# Get token from the v2 script
with open('raw/data/_push_to_github_v2.py', 'r', encoding='utf8') as f:
    script = f.read()
m = re.search(r"TOKEN = '([^']+)'", script)
token = m.group(1)
print(f'Token: {token[:5]}...{token[-4:]}')

# Get changed files
result = subprocess.run(['git', 'diff', '--name-only', 'HEAD~1'], capture_output=True, text=True)
files = [f.strip() for f in result.stdout.split('\n') if f.strip()]
print(f'Changed files: {len(files)}')

headers = {'Authorization': f'token {token}', 'Accept': 'application/vnd.github.v3+json'}

# Get latest commit SHA
r = requests.get('https://api.github.com/repos/mawenmeng/knowledge-vault/commits/master', headers=headers)
if r.status_code != 200:
    print(f'Error: {r.status_code} {r.text[:200]}')
    exit(1)
latest_sha = r.json()['sha']
print(f'Latest commit: {latest_sha}')

# Create blobs
tree = []
for fp in files:
    if not os.path.exists(fp):
        continue
    with open(fp, 'rb') as f:
        content = f.read()
    data = {'content': base64.b64encode(content).decode(), 'encoding': 'base64'}
    r = requests.post('https://api.github.com/repos/mawenmeng/knowledge-vault/git/blobs', json=data, headers=headers)
    if r.status_code not in (200, 201):
        print(f'Blob error {fp}: {r.status_code}')
        continue
    tree.append({'path': fp, 'mode': '100644', 'type': 'blob', 'sha': r.json()['sha']})
    print(f'  blob: {fp}')

# Create tree
r = requests.post('https://api.github.com/repos/mawenmeng/knowledge-vault/git/trees', json={'base_tree': latest_sha, 'tree': tree}, headers=headers)
if r.status_code not in (200, 201):
    print(f'Tree error: {r.status_code} {r.text[:300]}')
    exit(1)
tree_sha = r.json()['sha']
print(f'Tree: {tree_sha}')

# Create commit
r = requests.post('https://api.github.com/repos/mawenmeng/knowledge-vault/git/commits', json={'message': '[Fix] 全面修复图谱层级链接', 'tree': tree_sha, 'parents': [latest_sha]}, headers=headers)
if r.status_code not in (200, 201):
    print(f'Commit error: {r.status_code} {r.text[:300]}')
    exit(1)
commit_sha = r.json()['sha']
print(f'Commit: {commit_sha}')

# Update ref
r = requests.patch('https://api.github.com/repos/mawenmeng/knowledge-vault/git/refs/heads/master', json={'sha': commit_sha, 'force': False}, headers=headers)
if r.status_code not in (200, 201):
    print(f'Ref error: {r.status_code} {r.text[:300]}')
    exit(1)

print(f'SUCCESS! Pushed {len(tree)} files.')
