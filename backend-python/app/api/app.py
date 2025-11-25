from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pandas as pd
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

WAREHOUSES = ["WH1", "WH2", "WH3", "WH5", "WH6", "WH7", "WH8"]

DATA_DIR = "data"


def excel_to_slots(path: str):
    df = pd.read_excel(path)

    required = ["Row", "Bay", "Level", "Occupied"]
    for col in required:
        if col not in df.columns:
            raise Exception(f"Excel 缺少必須欄位：{col}")

    slots = []
    for _, row in df.iterrows():
        try:
            r = int(row["Row"]) if isinstance(row["Row"], (int, float)) else row["Row"]
            b = int(row["Bay"])
            lv = int(row["Level"])
        except:
            continue

        slot = {
            "row": r,
            "bay": b - 1,
            "level": lv - 1,
            "occupied": int(row["Occupied"]) == 1,
            "meta": {
                "PN": row.get("PN", ""),
                "數量": row.get("數量", ""),
                "Batch": row.get("Batch", ""),
                "Expire Date": row.get("Expire Date", ""),
                "Manufacture Date": row.get("Manufacture Date", "")
            }
        }
        slots.append(slot)

    return slots


@app.get("/api/racks")
async def get_racks(site: str):
    if site not in WAREHOUSES:
        raise HTTPException(status_code=400, detail="Unknown site")

    path = os.path.join(DATA_DIR, f"{site}.xlsx")

    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Excel not found")

    try:
        slots = excel_to_slots(path)
        return JSONResponse({"site": site, "slots": slots})
    except Exception as e:
        return {"error": str(e)}


@app.post("/api/upload")
async def upload_excel(site: str, file: UploadFile=File(...)):
    if site not in WAREHOUSES:
        raise HTTPException(status_code=400, detail="Unknown site")

    save_path = os.path.join(DATA_DIR, f"{site}.xlsx")

    with open(save_path, "wb") as f:
        f.write(await file.read())

    return {"message": f"{site}.xlsx updated successfully"}
