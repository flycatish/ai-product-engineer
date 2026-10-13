from gw import client

resp=client.chat.completions.create(model="GLM-5.3-Flash",messages=[{'role':'user','content':'hi'}],stream=True)
for chunk in resp:
    print(chunk)