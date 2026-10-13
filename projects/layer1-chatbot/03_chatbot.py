import sys
sys.stdout.reconfigure(encoding='utf-8')
from gw import client
messages=[]
while True:
    text=input("ask:")
    if text=='q':
        break
    messages.append({'role':'user','content':text})
    resp = client.chat.completions.create(model="GLM-5.3-Flash", messages=messages,
                                          stream=True)
    switch = False
    content=""
    for chunk in resp:
        if not chunk.choices:
            continue
        delta = chunk.choices[0].delta
        if getattr(delta, 'reasoning_content', None):
            text = f"\033[90m{delta.reasoning_content}\033[0m"
        elif delta.content:
            content+=delta.content
            if not switch:
                text = f"\n{delta.content}"
                switch = True
            else:
                text = delta.content
        elif chunk.choices[0].finish_reason:
            text = f"\nfinish_reason={chunk.choices[0].finish_reason}"
        elif chunk.usage:
            text = f"\n{chunk.usage}"
        else:
            continue
        print(text, end='', flush=True)

    messages.append({'role': 'assistant', 'content': content})
