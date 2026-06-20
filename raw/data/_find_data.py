import os, re

# Read the hierarchical indicators script
with open('D:\\knowledge-vault\\raw\\data\\_create_hierarchical_indicators.py', 'r', encoding='utf8') as f:
    content = f.read()

# Find 'standards_data' or 'data' or similar
for kw in ['standards_data', 'standards =', 'standards_data =', 'data =', 'std_names', 'std_refs']:
    idx = content.find(kw)
    if idx > 0:
        print(f'Found "{kw}" at position {idx}')
        print(content[idx:idx+200])
        print()
