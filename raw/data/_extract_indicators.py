"""
批量提取国家标准 PDF 中的技术指标
输出：JSON 格式的结构化数据
"""

import fitz, pytesseract, json, os, re
from PIL import Image

DATA_DIR = 'D:/knowledge-vault/raw/data'
OUTPUT_DIR = 'D:/knowledge-vault/raw/data/_extracted'

os.makedirs(OUTPUT_DIR, exist_ok=True)

def ocr_pdf(pdf_path, max_pages=10):
    """OCR 提取 PDF 文本，最多 max_pages 页"""
    doc = fitz.open(pdf_path)
    total = min(len(doc), max_pages)
    full_text = ''
    for i in range(total):
        mat = fitz.Matrix(2, 2)
        pix = doc[i].get_pixmap(matrix=mat)
        img = Image.frombytes('RGB', [pix.width, pix.height], pix.samples)
        text = pytesseract.image_to_string(img, lang='chi_sim+eng')
        full_text += f'\n===PAGE {i+1}===\n{text}'
    doc.close()
    return full_text

def extract_std_info(text):
    """提取标准号、名称、发布/实施日期"""
    info = {}
    # 标准号
    m = re.search(r'(GB[／/]?T?|GB|NY[／/]?T?)\s*(\d+[-\d]*)', text)
    info['std_no'] = m.group(0).replace(' ', '') if m else ''
    
    # 中文名称 - 从正文中找
    lines = text.split('\n')
    for line in lines:
        line = line.strip().replace(' ', '')
        if len(line) > 4 and any(c > '\u4e00' for c in line):
            if not any(kw in line for kw in ['ICS', 'GB', '代替', '前言', '本标准', '发布', '实施', '中华', '人民']):
                if not info.get('cn_name'):
                    info['cn_name'] = line
                    break
    
    # 日期
    for line in lines:
        l = line.replace(' ', '')
        m1 = re.search(r'(\d{4})[-\u2014](\d{2})[-\u2014](\d{2})\s*发布', l)
        if m1: info['pub_date'] = m1.group(0)
        m2 = re.search(r'(\d{4})[-\u2014](\d{2})[-\u2014](\d{2})\s*实施', l)
        if m2: info['impl_date'] = m2.group(0)
    
    return info

def extract_technical_indicators(text):
    """
    从标准文本中提取技术指标
    返回: [{indicator, value, unit, condition, grade}]
    """
    indicators = []
    lines = text.split('\n')
    
    # 找"要求"或"技术指标"后面的表格区域
    in_table = False
    table_lines = []
    
    for i, line in enumerate(lines):
        line_stripped = line.strip()
        # 检测表格开始
        if re.search(r'表\s*\d+\s', line_stripped) and ('要求' in line_stripped or '指标' in line_stripped):
            in_table = True
            table_lines.append(line_stripped)
            continue
        if in_table:
            # 检测表格结束（遇到章节号或空行后）
            if re.match(r'^\d+\s', line_stripped) and len(line_stripped) < 10:
                in_table = False
                continue
            if line_stripped and len(line_stripped) > 3:
                table_lines.append(line_stripped)
    
    # 从表格行中解析指标
    for line in table_lines:
        l = line.replace(' ', '')
        # 匹配模式: 指标名 数值 单位 条件
        # 如: 总氮(N)的质量分数 ≥ 46.0 %
        m = re.match(r'([\u4e00-\u9fff\w（）()\u2014\-\u2013]+?)\s*([≥≤><＝=])\s*([\d.]+)\s*([\u4e00-\u9fff\w%／/]+)', l)
        if m:
            indicators.append({
                'indicator': m.group(1).strip(),
                'condition': m.group(2),
                'value': m.group(3),
                'unit': m.group(4).strip()
            })
            continue
        
        # 匹配: 指标名 数值(无单位) 或 指标名 < 数值
        m2 = re.match(r'([\u4e00-\u9fff\w（）()]+)\s*[<≤]\s*([\d.]+)\s*([\u4e00-\u9fff\w%／/]*)', l)
        if m2:
            indicators.append({
                'indicator': m2.group(1).strip(),
                'condition': '≤',
                'value': m2.group(2),
                'unit': m2.group(3).strip() if m2.group(3) else ''
            })
    
    return indicators

def extract_referenced_standards(text):
    """提取规范性引用文件中的标准号"""
    refs = []
    lines = text.split('\n')
    in_ref_section = False
    
    for line in lines:
        l = line.strip().replace(' ', '')
        if '规范性引用文件' in l:
            in_ref_section = True
            continue
        if in_ref_section:
            # 遇到下一个章节号退出
            if re.match(r'^\d+\s', l) and '术语' not in l and '定义' not in l:
                break
            # 提取标准号
            m = re.findall(r'(GB[／/]?T?\s*\d+[-\d]*|GB\s*\d+[-\d]*|NY[／/]?T?\s*\d+[-\d]*|HG[／/]?T?\s*\d+[-\d]*)', l)
            for ref in m:
                refs.append(ref.replace(' ', ''))
    
    return list(set(refs))

# 批量处理
files = sorted([f for f in os.listdir(DATA_DIR) if f.endswith('.pdf') and not f.startswith('_')])
all_results = []

for idx, fname in enumerate(files):
    pdf_path = os.path.join(DATA_DIR, fname)
    print(f'[{idx+1}/{len(files)}] {fname[:50]}...', end=' ')
    
    try:
        text = ocr_pdf(pdf_path, max_pages=10)
        info = extract_std_info(text)
        indicators = extract_technical_indicators(text)
        refs = extract_referenced_standards(text)
        
        result = {
            'file': fname,
            'std_no': info.get('std_no', ''),
            'cn_name': info.get('cn_name', ''),
            'pub_date': info.get('pub_date', ''),
            'impl_date': info.get('impl_date', ''),
            'indicators': indicators,
            'referenced_standards': refs,
            'ocr_text_length': len(text)
        }
        all_results.append(result)
        print(f'OK | {len(indicators)} indicators, {len(refs)} refs')
    except Exception as e:
        print(f'ERROR: {e}')
        all_results.append({'file': fname, 'error': str(e)})

# 保存
with open(os.path.join(OUTPUT_DIR, 'all_indicators.json'), 'w', encoding='utf-8') as f:
    json.dump(all_results, f, ensure_ascii=False, indent=2)

print(f'\nDone! {len(all_results)} files processed.')
print(f'Output: {OUTPUT_DIR}/all_indicators.json')
