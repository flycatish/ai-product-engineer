from chunker import chunk_files
import sqlite3

conn = sqlite3.connect("chunks.db")
conn.execute("DROP TABLE IF EXISTS chunks")
# conn.execute("CREATE VIRTUAL TABLE chunks USING fts5(key, text)")
conn.execute("CREATE VIRTUAL TABLE chunks USING fts5(key, text, tokenize='trigram')")

files=[r"D:\document\projects\教程\ai-product-engineer\AGENTS.md",r"D:\document\projects\教程\ai-product-engineer\01-学习路线.md",r"D:\document\projects\教程\ai-product-engineer\02-信息源.md"]
result=chunk_files(files)
conn.executemany(
    "INSERT INTO chunks VALUES(?, ?)",
    [(e['key'],e['text']) for e in result],
)
conn.commit()
rows = conn.execute(
    "SELECT count(*) FROM chunks "
).fetchall()
print("count:", rows)
rows = conn.execute(
    "SELECT key, text FROM chunks WHERE chunks MATCH '助手协作模式里验收类检查由谁跑' ORDER BY rank LIMIT 5",
).fetchall()
print("BM25 query:", rows)
rows = conn.execute(
    "SELECT key, text FROM chunks WHERE chunks MATCH '流式 reasoning' ORDER BY rank LIMIT 5",
).fetchall()
print("BM25 query:", rows)
rows = conn.execute(
    "SELECT key, text FROM chunks WHERE chunks MATCH 'postgresql' ORDER BY rank LIMIT 5",
).fetchall()
print("BM25 query:", rows)

conn.execute("DROP TABLE IF EXISTS vocab")
conn.execute("CREATE VIRTUAL TABLE vocab USING fts5vocab(chunks, row)")
print(conn.execute("SELECT term FROM vocab WHERE term LIKE '%流%'").fetchall())
print(conn.execute("SELECT term FROM vocab WHERE term LIKE '%流式打印%'").fetchall())
print(conn.execute("SELECT term FROM vocab WHERE term LIKE '%流式%'").fetchall())
print("vocab count:", conn.execute("select count(*) from vocab",).fetchall())