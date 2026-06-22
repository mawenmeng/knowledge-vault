"""Push restructured knowledge vault to GitHub via API (binary-safe, using blob SHA)"""
import os, json, base64, requests, subprocess, sys

TOKEN = os.environ.get('GITHUB_TOKEN', '') or os.environ.get('GH_TOKEN', '')
if not TOKEN:
    print("No GitHub token found")
    sys.exit(1)

REPO = 'mawenmeng/knowledge-vault'
HEADERS = {'Authorization': f'token {TOKEN}', 'Accept': 'application/vnd.github.v3+json'}
GIT_DIR = 'D:/knowledge-vault'

# Get remote latest commit SHA
r = requests.get(f'https://api.github.com/repos/{REPO}/git/refs/heads/master', headers=HEADERS)
if r.status_code != 200:
    print(f"Failed to get ref: {r.status_code} {r.text[:200]}")
    sys.exit(1)
latest_sha = r.json()['object']['sha']
print(f"Remote latest commit: {latest_sha}")

# Get local HEAD
result = subprocess.run(['git', 'rev-parse', 'HEAD'], capture_output=True, text=True, cwd=GIT_DIR)
local_head = result.stdout.strip()
print(f"Local HEAD: {local_head}")

# Get all blobs from tree
result = subprocess.run(['git', 'ls-tree', '-r', local_head], capture_output=True, text=True, cwd=GIT_DIR)
blobs = []
for line in result.stdout.strip().split('\n'):
    if not line.strip():
        continue
    parts = line.split('\t')
    if len(parts) == 2:
        meta = parts[0].split()
        blob_sha = meta[2]
        path = parts[1]
        blobs.append({'path': path, 'sha': blob_sha, 'mode': meta[0]})

print(f"Total blobs: {len(blobs)}")

# Filter: skip .obsidian
filtered = [b for b in blobs if not b['path'].startswith('.obsidian')]
print(f"Filtered: {len(filtered)}")

# Build tree items using blob SHA (direct binary read)
tree_items = []
for i, b in enumerate(filtered):
    # Use git cat-file -p with blob SHA (no path encoding issues)
    result = subprocess.run(['git', 'cat-file', '-p', b['sha']],
                          capture_output=True, cwd=GIT_DIR)
    raw_bytes = result.stdout
    encoded = base64.b64encode(raw_bytes).decode('ascii')
    tree_items.append({
        'path': b['path'],
        'mode': b['mode'],
        'type': 'blob',
        'content': encoded
    })
    if (i+1) % 50 == 0:
        print(f"  Processed {i+1}/{len(filtered)}...")

print(f"Creating tree with {len(tree_items)} items...")

# Create tree via GitHub API with base64 encoding
tree_payload = []
for t in tree_items:
    entry = {
        'path': t['path'],
        'mode': t['mode'],
        'type': 'blob',
        'content': t['content'],
        'encoding': 'base64'
    }
    tree_payload.append(entry)

# Split into chunks of 100
chunk_size = 100
final_tree_sha = None

for chunk_idx in range(0, len(tree_payload), chunk_size):
    chunk = tree_payload[chunk_idx:chunk_idx + chunk_size]
    if final_tree_sha:
        payload = {'tree': chunk, 'base_tree': final_tree_sha}
    else:
        payload = {'tree': chunk}
    
    r = requests.post(f'https://api.github.com/repos/{REPO}/git/trees',
                     headers=HEADERS, json=payload)
    if r.status_code != 201:
        print(f"Failed to create tree chunk {chunk_idx}: {r.status_code} {r.text[:500]}")
        sys.exit(1)
    final_tree_sha = r.json()['sha']
    total_chunks = (len(tree_payload)-1)//chunk_size + 1
    print(f"  Tree chunk {chunk_idx//chunk_size + 1}/{total_chunks}: {final_tree_sha}")

print(f"Final tree SHA: {final_tree_sha}")

# Create commit
commit_data = {
    'message': '[Graph] 重构为5层知识图谱：12个产品类别(L0)→标准(L1)→指标类别(L2)→子类(L3)→指标值(L4)',
    'tree': final_tree_sha,
    'parents': [latest_sha]
}
r = requests.post(f'https://api.github.com/repos/{REPO}/git/commits', headers=HEADERS, json=commit_data)
if r.status_code != 201:
    print(f"Failed to create commit: {r.status_code} {r.text[:500]}")
    sys.exit(1)
new_commit_sha = r.json()['sha']
print(f"New commit SHA: {new_commit_sha}")

# Update ref (force)
r = requests.patch(f'https://api.github.com/repos/{REPO}/git/refs/heads/master',
    headers=HEADERS,
    json={'sha': new_commit_sha, 'force': True})
if r.status_code == 200:
    print("SUCCESS: Pushed to GitHub!")
else:
    print(f"Failed to update ref: {r.status_code} {r.text[:500]}")
