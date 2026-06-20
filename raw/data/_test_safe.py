def safe(text):
    s = text.replace('/', '／').replace('\\', '／').replace(':', '：')
    s = s.replace('*', '★').replace('?', '？').replace('"', '＂').replace('<', '＜').replace('>', '＞').replace('|', '｜')
    return s.strip()

print(repr(safe('通用 ≤343mg/m³')))
print(repr(safe('C₅及C₅以上组分含量 ≤3.0%(体积分数)')))
