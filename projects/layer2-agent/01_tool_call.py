from gw import client
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

def get_weather(city):
    return 'sunny'
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
}]
messages=[{'role':'user','content':'上海天气咋样'}]
resp = client.chat.completions.create(model="GLM-5.3-Flash", messages=messages,
                                          stream=False, tools=tools)
print(resp)
# print(resp.choices[0].finish_reason)
# print(resp.choices[0].message)

messages.append(resp.choices[0].message)
result=get_weather(json.loads(resp.choices[0].message.tool_calls[0].function.arguments)['city'])
messages.append({'role':'tool','tool_call_id':resp.choices[0].message.tool_calls[0].id,'content':result})
print(messages)
resp2 = client.chat.completions.create(model="GLM-5.3-Flash", messages=messages,
                                          stream=False, tools=tools)
print(resp2)
print(resp2.choices[0].message.content)