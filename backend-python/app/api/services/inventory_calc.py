# inventory_calc.py
# ---------------------------------------------------------
# 提供：calculate_inventory(slots)
# 內容：計算倉庫 KPI：總位數、空位、有貨、及期、過期
# ---------------------------------------------------------


def calculate_inventory(slots):
    total = len(slots)
    occupied = sum(1 for s in slots if s["occupied"])
    empty = total - occupied

    near = sum(1 for s in slots if s["expStatus"] == "near")
    expired = sum(1 for s in slots if s["expStatus"] == "expired")

    return {
        "total_slots": total,
        "occupied": occupied,
        "empty": empty,
        "near_expiry": near,
        "expired": expired,
        "occupancy_rate": round((occupied / total) * 100, 2) if total > 0 else 0
    }
