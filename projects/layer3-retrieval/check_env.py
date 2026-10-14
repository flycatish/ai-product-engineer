import sqlite3
import sys

sys.stdout.reconfigure(encoding="utf-8")

import sqlite_vec

conn = sqlite3.connect(":memory:")
conn.enable_load_extension(True)
sqlite_vec.load(conn)
conn.enable_load_extension(False)

print(f"sqlite library: {sqlite3.sqlite_version}")
(v,) = conn.execute("SELECT vec_version()").fetchone()
print(f"sqlite-vec:            {v}")

fts5 = conn.execute(
    "SELECT COUNT(*) FROM pragma_compile_options "
    "WHERE compile_options = 'ENABLE_FTS5'"
).fetchone()[0]
print(f"FTS5:                  {'yes' if fts5 else 'NO'}")

conn.execute(
    "CREATE VIRTUAL TABLE demo USING vec0(id INTEGER PRIMARY KEY, embedding FLOAT[4])"
)
conn.executemany(
    "INSERT INTO demo VALUES(?, ?)",
    [(1, "[1, 2, 3, 4]"), (2, "[1, 1, 1, 1]"), (3, "[10, 10, 10, 10]")],
)
rows = conn.execute(
    "SELECT id, distance FROM demo WHERE embedding MATCH '[1, 1, 1, 1]' "
    "ORDER BY distance LIMIT 3"
).fetchall()
print("KNN query:", rows)
print("ALL OK")
