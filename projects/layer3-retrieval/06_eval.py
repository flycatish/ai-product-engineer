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

    rrs=[]
    for query in queries:
        expect_keys = data['data'][query]['expect_keys']
        anchor = data['data'][query]['anchor']
        flag=False
        for i in range(len(results['data'][query])):
            e = results['data'][query][i][2]
            text = results['data'][query][i][3]
            if e in expect_keys and anchor in text:
                rrs.append(1.0/(i+1))
                print(f'{query}:{i+1}')
                flag=True
                break
        if not flag:
            rrs.append(0)
            print(f'{query}:miss')
    mrr=sum(rrs)/len(rrs)
    print(f'mrr:{mrr}')
if __name__=='__main__':
    check()