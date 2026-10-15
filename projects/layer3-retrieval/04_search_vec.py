import os,sys
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
import truststore
truststore.inject_into_ssl()   # Python 改用 Windows 证书库验 SSL，治自签证书
from fastembed import TextEmbedding
import sqlite3,sqlite_vec,array
sys.stdout.reconfigure(encoding="utf-8")
conn = sqlite3.connect("chunks.db")
conn.enable_load_extension(True); sqlite_vec.load(conn); conn.enable_load_extension(False)
model = TextEmbedding("BAAI/bge-small-zh-v1.5")

rows = conn.execute(
    "SELECT count(*) FROM chunks "
).fetchall()
print("count:", rows)

PREFIX = "为这个句子生成表示以用于检索相关文章："   # 空1：前缀常量（指令文本我已给出，确认首尾要不要空格）
queries=['流式','助手协作模式里验收类检查由谁跑','流式 reasoning','postgresql']
for q in queries:
    for label, embed_input in [("裸", q), ("前缀", f"{PREFIX}{q}")]:  # 空2：两个分支各喂什么给 embed
        rows = conn.execute(
                "SELECT id,key,SUBSTR(+text, 1, 80), distance FROM chunks WHERE embedding MATCH ? ORDER BY distance LIMIT 5",
        (sqlite_vec.serialize_float32(array.array("f", list(model.embed([embed_input]))[0])),),
            ).fetchall()
        print(f"[{label}] {q}: {rows}")