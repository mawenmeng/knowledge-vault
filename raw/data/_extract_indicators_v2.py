"""
批量提取国家标准 PDF 中的技术指标 - 优化版
分批处理，每批保存
"""

import fitz, pytesseract, json, os, re
from PIL import Image

DATA_DIR = 'D:/knowledge-vault/raw/data'
OUTPUT_DIR = 'D:/knowledge-vault/raw/data/_extracted'
os.makedirs(OUTPUT_DIR, exist_ok=True)

def ocr_pdf_fast(pdf_path, max_pages=6):
    """快速 OCR，只提取关键页"""
    doc = fitz.open(pdf_path)
    total = min(len(doc), max_pages)
    full_text = ''
    for i in range(total):
        mat = fitz.Matrix(1.5, 1.5)  # 降低分辨率加速
        pix = doc[i].get_pixmap(matrix=mat)
        img = Image.frombytes('RGB', [pix.width, pix.height], pix.samples)
        text = pytesseract.image_to_string(img, lang='chi_sim+eng')
        full_text += f'\n===PAGE {i+1}===\n{text}'
    doc.close()
    return full_text

def extract_std_info(text):
    info = {}
    m = re.search(r'(GB[／/]?T?|GB|NY[／/]?T?)\s*(\d+[-\d]*)', text)
    info['std_no'] = m.group(0).replace(' ', '') if m else ''
    
    lines = text.split('\n')
    for line in lines:
        line = line.strip().replace(' ', '')
        if len(line) > 4 and any(c > '\u4e00' for c in line):
            if not any(kw in line for kw in ['ICS', 'GB', '代替', '前言', '本标准', '发布', '实施', '中华', '人民']):
                if not info.get('cn_name'):
                    info['cn_name'] = line
                    break
    
    for line in lines:
        l = line.replace(' ', '')
        m1 = re.search(r'(\d{4})[-\u2014](\d{2})[-\u2014](\d{2})\s*发布', l)
        if m1: info['pub_date'] = m1.group(0)
        m2 = re.search(r'(\d{4})[-\u2014](\d{2})[-\u2014](\d{2})\s*实施', l)
        if m2: info['impl_date'] = m2.group(0)
    
    return info

def extract_indicators(text):
    """从表格文本中提取技术指标"""
    indicators = []
    lines = text.split('\n')
    
    for line in lines:
        l = line.strip().replace(' ', '')
        if not l or len(l) < 5:
            continue
        
        # 跳过表头/非指标行
        if any(kw in l for kw in ['表', '项目', '等级', '优等品', '合格品', '指标', '要求', '外观']):
            continue
        
        # 模式1: 指标名 ≥/≤ 数值 单位
        m = re.search(r'([\u4e00-\u9fff\w（）()\u2014\-]+?)\s*([≥≤><＝=])\s*([\d.]+)\s*([\u4e00-\u9fff\w%／/μ°²³¹²]+)', l)
        if m:
            indicators.append({
                'indicator': m.group(1).strip(),
                'condition': m.group(2),
                'value': m.group(3),
                'unit': m.group(4).strip()
            })
            continue
        
        # 模式2: 指标名 < 数值 (省略≥符号)
        m2 = re.search(r'([\u4e00-\u9fff\w（）()]+)\s*[<≤]\s*([\d.]+)\s*([\u4e00-\u9fff\w%／/]*)', l)
        if m2 and len(m2.group(1)) > 1:
            indicators.append({
                'indicator': m2.group(1).strip(),
                'condition': '≤',
                'value': m2.group(2),
                'unit': m2.group(3).strip() if m2.group(3) else ''
            })
    
    return indicators

def extract_refs(text):
    """提取引用的标准"""
    refs = []
    lines = text.split('\n')
    in_ref = False
    for line in lines:
        l = line.strip().replace(' ', '')
        if '规范性引用文件' in l:
            in_ref = True
            continue
        if in_ref:
            if re.match(r'^\d\s', l) and '术语' not in l and '定义' not in l:
                break
            ms = re.findall(r'(GB[／/]?T?\s*\d+[-\d]*|GB\s*\d+[-\d]*|NY[／/]?T?\s*\d+[-\d]*|HG[／/]?T?\s*\d+[-\d]*)', l)
            for ref in ms:
                refs.append(ref.replace(' ', ''))
    return list(set(refs))

# 分批处理
files = sorted([f for f in os.listdir(DATA_DIR) if f.endswith('.pdf') and not f.startswith('_')])
batch_size = 10
all_results = []

for batch_start in range(0, len(files), batch_size):
    batch = files[batch_start:batch_start + batch_size]
    print(f'\nBatch {batch_start//batch_size + 1}/{(len(files)-1)//batch_size + 1}')
    
    for idx, fname in enumerate(batch):
        pdf_path = os.path.join(DATA_DIR, fname)
        global_idx = batch_start + idx + 1
        print(f'  [{global_idx}/{len(files)}] {fname[:45]}...', end=' ')
        
        try:
            text = ocr_pdf_fast(pdf_path, max_pages=6)
            info = extract_std_info(text)
            indicators = extract_indicators(text)
            refs = extract_refs(text)
            
            result = {
                'file': fname,
                'std_no': info.get('std_no', ''),
                'cn_name': info.get('cn_name', ''),
                'pub_date': info.get('pub_date', ''),
                'impl_date': info.get('impl_date', ''),
                'indicators': indicators,
                'referenced_standards': refs,
                'ocr_len': len(text)
            }
            all_results.append(result)
            print(f'{len(indicators)} ind, {len(refs)} refs')
        except Exception as e:
            print(f'ERROR: {e}')
            all_results.append({'file': fname, 'error': str(e)})
    
    # 每批保存一次
    batch_file = os.path.join(OUTPUT_DIR, f'batch_{batch_start//batch_size + 1}.json')
    with open(batch_file, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
    print(f'  Saved: {batch_file}')

# 最终合并
with open(os.path.join(OUTPUT_DIR, 'all_indicators.json'), 'w', encoding='utf-8') as f:
    json.dump(all_results, f, ensure_ascii=False, indent=2)

print(f'\nDone! {len(all_results)} files processed.')
