import json,os,sys
from chunker import chunk_files
from dotenv import load_dotenv
load_dotenv()
from hybrider import hybrid_search
def check():

    with open("eval.json",'r',encoding='utf-8') as f:
        data = json.load(f)
    queries = data['data'].keys()
    files = os.environ["CORPUS_FILES"].split(";")
    chunks = chunk_files(files)
    # 过期没？
    if len(chunks)!=data['blocks']:
        print(f'语料 {len(chunks)} 块 ≠ 表里 {data['blocks']} 块，请重跑 02/03 + 重判期望表')
        sys.exit(1)
    results=hybrid_search(queries)

    for query in queries:
        expect_ids = data['data'][query]['expect_ids']
        flag=False
        for i in range(data['data'][query]['k']):
            e = results['data'][query][i][0]
            if e in expect_ids:
                print(f'{query}:pass')
                flag=True
                break
        if not flag:
            print(f'{query}:fail')
check()