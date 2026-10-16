import os,sys
sys.stdout.reconfigure(encoding="utf-8")
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
import truststore
truststore.inject_into_ssl()   # Python 改用 Windows 证书库验 SSL，治自签证书
from fastembed import TextEmbedding
import sqlite3,sqlite_vec,array
conn = sqlite3.connect("chunks.db")
conn.enable_load_extension(True); sqlite_vec.load(conn); conn.enable_load_extension(False)
from collections import defaultdict

# reciprocal_rank_fusion:倒数秩融合
def get_rrf(ranks):
    result=0
    for rank in ranks:
        result+=1.0/(60+rank)
    return result

model = TextEmbedding("BAAI/bge-small-zh-v1.5")
queries=['流式','助手协作模式里验收类检查由谁跑','流式 reasoning','postgresql']
for q in queries:
    hh=defaultdict(list)
    detail_hh={}
    vec_top = conn.execute(
            "SELECT id,key FROM chunks WHERE embedding MATCH ? ORDER BY distance LIMIT 5",
    (sqlite_vec.serialize_float32(array.array("f", list(model.embed([q]))[0])),),
        ).fetchall()
    for i in range(len(vec_top)):
        key=vec_top[i][0]
        hh[key].append(i+1)
        if not detail_hh.get(key,None):
            detail_hh[key]=vec_top[i][1]
    fts_top = conn.execute(
        "SELECT rowid,key FROM chunks_fts WHERE chunks_fts MATCH ? ORDER BY rank LIMIT 5",(q,)
    ).fetchall()
    for i in range(len(fts_top)):
        key = fts_top[i][0]
        hh[key].append(i + 1)
        if not detail_hh.get(key,None):
            detail_hh[key]=fts_top[i][1]
    rrfs=[]
    for k,v in hh.items():
        rrfs.append((k,get_rrf(v),detail_hh[k]))
    rrfs.sort(key=lambda x:-x[1])
    print(f"{q}: {rrfs}")