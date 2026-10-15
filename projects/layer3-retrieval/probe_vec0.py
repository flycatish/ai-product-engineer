# probe_vec0.py
import sqlite3, sys
sys.stdout.reconfigure(encoding="utf-8")
import sqlite_vec

conn = sqlite3.connect(":memory:")
conn.enable_load_extension(True); sqlite_vec.load(conn); conn.enable_load_extension(False)

try:
    # 普通列 = metadata 列，+ 前缀 = auxiliary 列，两种都试
    conn.execute("CREATE VIRTUAL TABLE t USING vec0(embedding float[4], key TEXT, +note TEXT)")
    conn.execute("INSERT INTO t(embedding, key, note) VALUES(?, ?, ?)", ("[1,2,3,4]", "abc", "hello"))
    print(conn.execute(
        "SELECT rowid, key, note, distance FROM t WHERE embedding MATCH ? ORDER BY distance LIMIT 1",
        ("[1,2,3,4]",)
    ).fetchall())
    print("SUPPORTED")
except Exception as e:
    print("NOT supported:", e)