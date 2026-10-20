import os,sqlite3
from dotenv import load_dotenv
load_dotenv()
from chunker import chunk_files

conn = sqlite3.connect("chunks.db")
conn.execute("DROP TABLE IF EXISTS chunks_fts")
# conn.execute("CREATE VIRTUAL TABLE chunks_fts USING fts5(key, text)")
conn.execute("CREATE VIRTUAL TABLE chunks_fts USING fts5(key, text, tokenize='trigram')")

files=os.environ["CORPUS_FILES"].split(";")
result=chunk_files(files)
conn.executemany(
    "INSERT INTO chunks_fts(rowid,key, text) VALUES(?,?, ?)",
    [(i+1,result[i]['key'],result[i]['text']) for i in range(len(result))],
)
conn.commit()
rows = conn.execute(
    "SELECT count(*) FROM chunks_fts "
).fetchall()
print("count:", rows)
rows = conn.execute(
    "SELECT key, text FROM chunks_fts WHERE chunks_fts MATCH '助手协作模式里验收类检查由谁跑' ORDER BY rank LIMIT 5",
).fetchall()
print("BM25 query:", rows)
rows = conn.execute(
    "SELECT key, text FROM chunks_fts WHERE chunks_fts MATCH '流式 reasoning' ORDER BY rank LIMIT 5",
).fetchall()
print("BM25 query:", rows)
rows = conn.execute(
    "SELECT key, text FROM chunks_fts WHERE chunks_fts MATCH 'postgresql' ORDER BY rank LIMIT 5",
).fetchall()
print("BM25 query:", rows)

conn.execute("DROP TABLE IF EXISTS vocab")
conn.execute("CREATE VIRTUAL TABLE vocab USING fts5vocab(chunks_fts, row)")
print(conn.execute("SELECT term FROM vocab WHERE term LIKE '%流%'").fetchall())
print(conn.execute("SELECT term FROM vocab WHERE term LIKE '%流式打印%'").fetchall())
print(conn.execute("SELECT term FROM vocab WHERE term LIKE '%流式%'").fetchall())
print("vocab count:", conn.execute("select count(*) from vocab",).fetchall())