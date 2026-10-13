# ============================================================
# core/report.py — JSON-отчёт (правило 134)
# ============================================================
import json
import os
import datetime


def write_report(name, data, out_dir="reports"):
    os.makedirs(out_dir, exist_ok=True)
    data['timestamp'] = datetime.datetime.now().isoformat()
    data['protocol'] = '4.2.0'
    path = os.path.join(out_dir, f"{name}_report.json")
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"[REPORT] {path}")
    return path
