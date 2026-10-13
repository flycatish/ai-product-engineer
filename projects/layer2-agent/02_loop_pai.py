import sys
sys.stdout.reconfigure(encoding='utf-8')
import os,json
from dotenv import load_dotenv
load_dotenv()

import httpx2 as httpx
from openai import AsyncOpenAI
from pydantic_ai import Agent,UsageLimits
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

class GatewayModel(OpenAIChatModel):
    def _validate_completion(self, response):
        # 填空：遍历 response.choices，把 message.metadata 里非 str 的值剥掉
        stringified_metadata = {
            k: json.dumps(v) for k, v in response.metadata.items()
        }

        response.metadata = stringified_metadata
        # 提示：response 是 openai SDK 的模型（没校验过的），属性可以直接改
        return super()._validate_completion(response)



# 填空1：对照 gw.py 的 OpenAI(...)，改成异步版 —— 改哪三处？
async_client = AsyncOpenAI(
    base_url=os.environ["OPENAI_BASE_URL"],
    api_key=os.environ["OPENAI_API_KEY"],
    default_headers={"X-Codehub-Token": os.environ["CODEHUB_TOKEN"]},
    http_client=httpx.AsyncClient(trust_env=False),
)

# 填空2：Provider 包 client，Model 包 Provider，Agent 包 Model
provider = OpenAIProvider(openai_client=async_client)
model = GatewayModel("GLM-5.3-Flash", provider=provider)
agent = Agent(model)

@agent.tool_plain
def get_weather(city:str):
    """查询某城市当前天气"""
    return 'raining'

@agent.tool_plain
def get_time(city:str):
    """查询某城市当前时间"""
    return '25点'

# 填空3：跑一次对话，把回答打出来（查 result 对象上哪个属性是文本）
# result = agent.run_sync("用一句话介绍你自己")
result = agent.run_sync("上海现在几点？天气咋样？上海湿度多少", usage_limits=UsageLimits(request_limit=10))
print(result.all_messages())
