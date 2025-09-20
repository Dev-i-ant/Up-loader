# src/services/meta.py
from pathlib import Path
import csv

class MetaEntry(dict):
    # fields: title: str, tags: list[str]
    pass

def parse_meta_line(line: str) -> MetaEntry:
    line = line.strip()
    if not line:
        return None
    # простой текст -> извлекаем хэштеги #tag
    parts = [p for p in line.split() if p.startswith("#")]
    tags = [p.lstrip("#").strip() for p in parts]
    title = " ".join([p for p in line.split() if not p.startswith("#")]).strip()
    return MetaEntry(title=title or " ", tags=tags)

def load_meta_file(path: Path) -> list[MetaEntry]:
    text = path.read_text(encoding="utf-8").splitlines()
    # CSV? Проверим заголовок
    if text and ("," in text[0] or ";" in text[0]):
        # пробуем CSV с разделителем запятая/точка с запятой
        entries: list[MetaEntry] = []
        delim = ";" if ";" in text[0] and "," not in text[0] else ","
        reader = csv.DictReader(text, delimiter=delim)
        for row in reader:
            title = (row.get("title") or "").strip()
            raw_tags = (row.get("hashtags") or "").strip()
            tags = [t.strip().lstrip("#") for t in raw_tags.replace(" ", "").split(",") if t.strip()]
            entries.append(MetaEntry(title=title or " ", tags=tags))
        return entries
    else:
        # построчный текст
        return [m for m in (parse_meta_line(l) for l in text) if m]