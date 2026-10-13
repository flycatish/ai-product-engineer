import sys
import json
sys.stdout.reconfigure(encoding='utf-8')
from gw import client

def get_weather(city):
    return 'raining'
def get_time(city):
    return '25点'
tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "查询某城市当前天气",  # 模型靠这句话决定什么时候调它
        "parameters": {                       # JSON Schema，描述参数长什么样
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "城市名"}
            },
            "required": ["city"]
        }
    }
},
    {
        "type": "function",
        "function": {
            "name": "get_time",
            "description": "查询某城市当前时间",  # 模型靠这句话决定什么时候调它
            "parameters": {  # JSON Schema，描述参数长什么样
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "城市名"}
                },
                "required": ["city"]
            }
        }
    }
]
funcs = {"get_weather": get_weather,"get_time": get_time}

messages=[]
text = input("ask:")
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
# print(messages)