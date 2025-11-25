# excel_reader.py
# ---------------------------------------------------------
# 提供：read_excel_slots(excel_file)
# 回傳：標準化後的 slot list
# ---------------------------------------------------------

import pandas as pd
from datetime import datetime, timedelta

ROW_LABELS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def excel_serial_to_date(v):
    """將 Excel 序列日期 或 字串 → datetime.date"""
    if pd.isna(v):
        return None

    if isinstance(v, (int, float)):
        # Excel serial：1899-12-30 是 Day 0
        return (datetime(1899, 12, 30) + timedelta(days=float(v))).date()

    if isinstance(v, str):
        v = v.strip()
        if not v:
            return None

        # 支援 20251014 / 2025-10-14 / 2025/10/14
        for fmt in ("%Y%m%d", "%Y-%m-%d", "%Y/%m/%d"):
            try:
                return datetime.strptime(v, fmt).date()
            except:
                pass

        try:
            return pd.to_datetime(v).date()
        except:
            return None

    return None


def classify_expiry(exp_date):
    """回傳：ok / near / expired"""
    if exp_date is None:
        return "ok"

    today = datetime.now().date()
    diff = (exp_date - today).days

    if diff < 0:
        return "expired"
    if diff <= 30:
        return "near"
    return "ok"


def row_label_to_index(v):
    if isinstance(v, str) and len(v.strip()) == 1:
        s = v.strip().upper()
        if s in ROW_LABELS:
            return ROW_LABELS.index(s)
    try:
        return int(v)
    except:
        return None


def read_excel_slots(path):
    """讀取 rack_status.xlsx → 標準化 dictionary list"""
    df = pd.read_excel(path)

    required = ["Row", "Bay", "Level", "Occupied"]
    for col in required:
        if col not in df.columns:
            raise Exception(f"Excel 缺少必要欄位：{col}")

    slots = []

    for _, row in df.iterrows():

        r_index = row_label_to_index(row["Row"])
        if r_index is None:
            continue

        try:
            b_index = int(row["Bay"]) - 1
            lv_index = int(row["Level"]) - 1
        except:
            continue

        occ = bool(int(row["Occupied"]))

        exp_raw = row.get("Expire Date", "")
        exp_date = excel_serial_to_date(exp_raw)
        exp_status = classify_expiry(exp_date)

        meta = {
            "PN": row.get("PN", ""),
            "數量": row.get("數量", ""),
            "Batch": row.get("Batch", ""),
            "Expire Date": exp_raw if exp_raw is not None else "",
            "Manufacture Date": row.get("Manufacture Date", "")
        }

        slots.append({
            "row": r_index,
            "bay": b_index,
            "level": lv_index,
            "occupied": occ,
            "meta": meta,
            "expStatus": exp_status,
            "expDateISO": exp_date.isoformat() if exp_date else None
        })

    return slots
