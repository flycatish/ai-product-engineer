import sys; sys.stdout.reconfigure(encoding="utf-8")
from chunker import chunk_files
import os; from dotenv import load_dotenv; load_dotenv()
anchor = "KNN 查询必须带 LIMIT"          # ← 换着试
hits = [c for c in chunk_files(os.environ["CORPUS_FILES"].split(";")) if anchor in c['text']]
print(len(hits)); [print(h['key'], '|', h['text'].replace('\n',' ')) for h in hits]