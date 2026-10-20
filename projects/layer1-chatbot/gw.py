import os

import httpx2 as httpx
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url=os.environ["OPENAI_BASE_URL"],
    api_key=os.environ["OPENAI_API_KEY"],
    default_headers={os.environ["GATEWAY_AUTH_HEADER"]: os.environ["GATEWAY_TOKEN"]},
    http_client=httpx.Client(trust_env=False),  # 不信任何环境/注册表代理，永远直连
)