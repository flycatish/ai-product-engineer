import sys; sys.stdout.reconfigure(encoding="utf-8")
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from dotenv import load_dotenv
load_dotenv()
import sqlite_vec, array
from hybrider import model, conn

q = "completion_tokens"
qv = sqlite_vec.serialize_float32(array.array("f", list(model.embed([q]))[0]))
rows = conn.execute(
    "SELECT id, key, +text, distance FROM chunks WHERE embedding MATCH ? ORDER BY distance LIMIT 46",
    (qv,),
).fetchall()
print(f"--- {q} ---")
for rank, (cid, key, text, dist) in enumerate(rows, 1):
    mark = ""
    if "completion_tokens" in text:
        mark = "  <== 正解块"
    if "chunking 策略" in text:
        mark = "  <== 干扰块(主题像,无答案)"
    if rank <= 5 or mark:
        print(f"{rank:2d} d={dist:.4f} {key[-28:]}{mark}")
