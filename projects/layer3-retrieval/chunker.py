import re,statistics,random,sys
from collections import defaultdict
sys.stdout.reconfigure(encoding="utf-8")


def chunk_files(files:list[str])-> list[dict]:
    chunks = defaultdict(list)
    hh = defaultdict(str)
    for file in files:
        fname=file.split("\\")[-1]
        h1 = None
        h2 = None
        h3 = None
        text=""
        with open(file,"r",encoding="utf-8") as f:
            text+=f.read()
        for line in text.splitlines():
            m = re.match(r'^(#{1,3})\s+(.*)',line)
            if m:
                if len(m[1])==1:
                    h1=m[2]
                    h2=h3=None
                elif len(m[1])==2:
                    h2=m[2]
                    h3 = None
                elif len(m[1])==3:
                    h3=m[2]
                else:
                    pass
            else:
                if line.strip():
                    hh[f"{fname}>{h1}>{h2}>{h3}"]+=line+"\n"
    for k,v in hh.items():
        if len(v)>1000:
            v2s = v.split("- ")
            for v2 in v2s:
                if not v2.strip(): continue
                if len(v2) > 1000:
                    v3s = v2.split("。")
                    for v3 in v3s:
                        if not v3.strip(): continue
                        if len(v3) < 100:
                            if chunks[k]:
                                chunks[k][-1] += v3+"。"
                            else:
                                chunks[k].append(f"{k}: {v3}。")
                        else:
                            chunks[k].append(f"{k}: {v3}。")
                elif len(v2)<100:
                    if chunks[k]:
                        chunks[k][-1] += v2
                    else:
                        chunks[k].append(f"{k}: {v2}")
                else:
                    chunks[k].append(f"{k}: {v2}")
        elif len(v)<100:
            if chunks[k]:
                chunks[k][-1]+=v
            else:
                chunks[k].append(f"{k}: {v}")
        else:
            chunks[k].append(f"{k}: {v}")
    result=[]
    for k,v in chunks.items():
        for e in v:
            result.append({'key':k, 'text':e})

    return result

if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    load_dotenv()
    files=os.environ["CORPUS_FILES"].split(";")
    result=chunk_files(files)
    flatten_chunk=[e['text'] for e in result]
    lens = [len(e) for e in flatten_chunk]
    print(f"blocks: {len(flatten_chunk)}")
    print(f"min: {min(lens)}")
    print(f"max: {max(lens)}")
    print(f"median: {statistics.median(lens)}")
    print(random.sample(flatten_chunk, 3))