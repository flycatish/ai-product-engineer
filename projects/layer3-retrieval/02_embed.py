import os
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
import truststore
truststore.inject_into_ssl()   # Python 改用 Windows 证书库验 SSL，治自签证书
from fastembed import TextEmbedding
from chunker import chunk_files
import sqlite3,sys
sys.stdout.reconfigure(encoding="utf-8")
import sqlite_vec,array
# # 先看支持列表里有哪些中文模型（自己找带 zh / multilingual 的）
# for m in TextEmbedding.list_supported_models():
#     if "zh" in m["model"] or "multilingual" in m["model"]:
#         print(m["model"], m["dim"])
model = TextEmbedding("BAAI/bge-small-zh-v1.5")
# print(len(list(model.embed(["你好"]))[0]))

files=[r"D:\document\projects\教程\ai-product-engineer\AGENTS.md",r"D:\document\projects\教程\ai-product-engineer\01-学习路线.md",r"D:\document\projects\教程\ai-product-engineer\02-信息源.md"]
chunks=chunk_files(files)
texts = [c['text'] for c in chunks]
vectors = list(model.embed(texts))


conn = sqlite3.connect("chunks.db")
conn.enable_load_extension(True); sqlite_vec.load(conn); conn.enable_load_extension(False)
conn.execute("DROP TABLE IF EXISTS chunks")
conn.execute(
    "CREATE VIRTUAL TABLE chunks USING vec0(id INTEGER PRIMARY KEY, embedding FLOAT[512], key TEXT, +text TEXT)"
)
conn.executemany(
    "INSERT INTO chunks VALUES(?, ?,?,?)",
    [(i+1,sqlite_vec.serialize_float32(array.array('f', vectors[i])),chunks[i]['key'],chunks[i]['text']) for i in range(len(vectors))]
)
conn.commit()

print(conn.execute("SELECT count(*) FROM chunks;").fetchall())
q=vectors[0]
row = conn.execute(
        "SELECT id,key, distance FROM chunks WHERE embedding MATCH ? ORDER BY distance LIMIT 1",
(sqlite_vec.serialize_float32(array.array("f", q)),),
    ).fetchone()
print(row)