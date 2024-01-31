import os
from dotenv import load_dotenv

load_dotenv()
zhipu_apikey = os.getenv('ZHIPU_API_KEY')
#print(zhipu_apikey)

# 流式调用：就是一个字一个字输出结果
'''
from zhipuai import ZhipuAI
client = ZhipuAI(api_key=zhipu_apikey) # 请填写您自己的APIKey
response = client.chat.completions.create(
    model="glm-4",  # 填写需要调用的模型名称
    messages=[
        {"role": "system", "content": "你是一个乐于解答各种问题的助手，你的任务是为用户提供专业、准确、有见地的建议。"},
        {"role": "user", "content": "我对太阳系的行星非常感兴趣，特别是土星。请提供关于土星的基本信息，包括其大小、组成、环系统和任何独特的天文现象。"},
    ],
    stream=True,
)
for chunk in response:
    print(chunk.choices[0].delta)
'''

# 同步调用
'''
from zhipuai import ZhipuAI
client = ZhipuAI(api_key=zhipu_apikey) # 填写您自己的APIKey
response = client.chat.completions.create(
    model="glm-4",  # 填写需要调用的模型名称
    messages=[
        {"role": "user", "content": "作为一名营销专家，请为我的产品创作一个吸引人的slogan"},
        {"role": "assistant", "content": "当然，为了创作一个吸引人的slogan，请告诉我一些关于您产品的信息"},
        {"role": "user", "content": "智谱AI开放平台"},
        {"role": "assistant", "content": "智启未来，谱绘无限一智谱AI，让创新触手可及!"},
        {"role": "user", "content": "创造一个更精准、吸引人的slogan"}
    ],
)
print(response)
'''

# 测试并发超过QPS=5
import threading
from zhipuai import ZhipuAI

def call_api():
    client = ZhipuAI(api_key=zhipu_apikey)
    response = client.chat.completions.create(
        model="glm-4",
        messages=[
            {"role": "user", "content": "作为一名营销专家，请为我的产品创作一个吸引人的slogan"},
            {"role": "assistant", "content": "当然，为了创作一个吸引人的slogan，请告诉我一些关于您产品的信息"},
            {"role": "user", "content": "智谱AI开放平台"},
            {"role": "assistant", "content": "智启未来，谱绘无限一智谱AI，让创新触手可及!"},
            {"role": "user", "content": "创造一个更精准、吸引人的slogan"}
        ]
    )
    print(response)

# 创建并启动 6 个线程
threads = []
for i in range(4):
    thread = threading.Thread(target=call_api)
    threads.append(thread)
    thread.start()

# 等待所有线程完成
for thread in threads:
    thread.join()

#