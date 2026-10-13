import sys,os
import json
sys.stdout.reconfigure(encoding='utf-8')
from gw import client

def list_files(path):
    if not os.path.isdir(path):
        return '文件夹路径不存在'
    return '\n'.join(os.listdir(path))

def read_file(path):
    if not os.path.isfile(path):
        return '文件路径不存在'
    text=''
    try:
        with open(path,'r',encoding='utf-8') as f:
            text+=f.read()
        return text[:2000]
    except OSError:
        return '读取失败'

tools = [{
    "type": "function",
    "function": {
        "name": "list_files",
        "description": "列出某文件夹下的文件和子目录名",  # 模型靠这句话决定什么时候调它
        "parameters": {                       # JSON Schema，描述参数长什么样
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "文件夹路径"}
            },
            "required": ["path"]
        }
    }
},
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "读取文件内容",  # 模型靠这句话决定什么时候调它
            "parameters": {  # JSON Schema，描述参数长什么样
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "文件路径"}
                },
                "required": ["path"]
            }
        }
    }
]
funcs = {"list_files": list_files,"read_file": read_file}

messages=[]
text = input("ask:")
messages.append({'role': 'system', 'content': f"当前工作目录是{os.getcwd()},工具参数里的相对路径都相对它解析"})
messages.append({'role': 'user', 'content': text})
count=0
while True:
    if count>9:
        print('轮次超限')
        break
    resp = client.chat.completions.create(model="GLM-5.3-Flash", messages=messages,
                                          stream=False, tools=tools)
    if resp.choices[0].finish_reason=='tool_calls':
        # print(resp)
        messages.append(resp.choices[0].message)
        for tool_call in resp.choices[0].message.tool_calls:
            function_name=tool_call.function.name
            func = funcs.get(function_name)
            if func is None:
                result = f"错误：工具 {function_name} 不存在"
            else:
                result = func(**json.loads(tool_call.function.arguments))
            messages.append({'role': 'tool', 'tool_call_id': tool_call.id, 'content': result})
    else:
        print(resp.choices[0].message.content)
        break
    count+=1
print(messages)