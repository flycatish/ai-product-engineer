from gw import client

resp=client.chat.completions.create(model="GLM-5.3-Flash",messages=[{'role':'user','content':'hi'}],stream=True)
switch=False
for chunk in resp:
    if not chunk.choices:
        continue
    delta=chunk.choices[0].delta
    if getattr(delta,'reasoning_content', None):
        text=f"\033[90m{delta.reasoning_content}\033[0m"
    elif delta.content:
        if not switch:
            text = f"\n{delta.content}"
            switch=True
        else:
            text=delta.content
    elif chunk.choices[0].finish_reason:
        text=f"\nfinish_reason={chunk.choices[0].finish_reason}"
    elif chunk.usage:
        text=f"\n{chunk.usage}"
    else:
        continue
    print(text,end='',flush=True)
