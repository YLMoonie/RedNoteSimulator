import os
from openai import OpenAI
from dotenv import load_dotenv

# 确保加载了 .env 文件
load_dotenv()

# 从 .env 文件中获取配置
# 只用列表中的第一个key来测试
api_key = os.getenv("API_LIST", "").split(',')[0]
base_url = os.getenv("BASE_URL")
model_name = os.getenv("MODEL_NAME")

print("--- 正在使用以下配置测试API ---")
if api_key:
    print(f"API Key (前4位): {api_key[:4]}...")
else:
    print("API Key: 未找到!")
print(f"Base URL: {base_url}")
print(f"Model Name: {model_name}")
print("---------------------------------")

if not all([api_key, base_url, model_name]):
    print("\n❌ 错误: .env 文件中的 API_LIST, BASE_URL, 或 MODEL_NAME 未正确配置。")
else:
    try:
        # 创建客户端
        client = OpenAI(api_key=api_key, base_url=base_url)

        # 发送一个最简单的请求
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": "Hello!"}]
        )

        print("\n✅ API 调用成功!")
        print("模型回复:", response.choices[0].message.content)

    except Exception as e:
        print(f"\n❌ API 调用失败!")
        print("错误详情:", e)