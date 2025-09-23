# file: backend/main.py

import asyncio
import json
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from flow import ProgressFlow, purchase_decision_judgment
import os
import traceback
from dotenv import dotenv_values 

# --- 路径代码 ---
current_dir = os.path.dirname(os.path.abspath(__file__))
frontend_dir = os.path.join(current_dir, "..", "frontend")
index_html_path = os.path.join(frontend_dir, "index.html")

# vvvv 这是关键的修正 vvvv
# 将 .env 文件的路径指向当前目录 (backend/)，而不是上一级目录
env_path = os.path.join(current_dir, ".env")
# ^^^^ 修正结束 ^^^^


# 创建 FastAPI 应用
app = FastAPI()

# 挂载静态文件目录
app.mount("/frontend", StaticFiles(directory=frontend_dir), name="frontend")

# 返回 index.html
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    try:
        with open(index_html_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read(), status_code=200)
    except FileNotFoundError:
        return HTMLResponse(content="<h1>错误：找不到 index.html</h1><p>请确保您的 frontend 文件夹和 index.html 文件位于正确的位置。</p>", status_code=404)


# 获取 .env 配置文件的 API 接口 (增强了错误处理)
@app.get("/get-env-config/")
async def get_env_config():
    # 1. 首先，检查 .env 文件是否存在
    if not os.path.exists(env_path):
        error_msg = {
            "error": "File Not Found",
            "message": f"在预期的位置找不到 .env 文件。请确保它位于 backend 文件夹内: {env_path}"
        }
        return JSONResponse(content=error_msg, status_code=404)

    try:
        # 2. 读取 .env 文件
        config = dotenv_values(env_path)
        
        # 3. 检查文件是否为空或格式错误 (读取后是空字典)
        if not config:
            empty_msg = {
                "error": "Empty or Malformed File",
                "message": ".env 文件存在，但内容为空或格式不正确。请确保文件内至少有一行有效的 KEY=VALUE 配置。"
            }
            return JSONResponse(content=empty_msg)

        # 4. 安全处理：隐藏真实的 API 密钥
        if "API_LIST" in config and config["API_LIST"]:
            api_keys = [key.strip() for key in config["API_LIST"].split(',') if key.strip()]
            sanitized_keys = [f"API_KEY_{i+1}" for i in range(len(api_keys))]
            config["API_LIST"] = ", ".join(sanitized_keys)
        
        return JSONResponse(content=config)
        
    except Exception as e:
        # 捕获其他可能的读取错误
        return JSONResponse(content={"error": f"读取 .env 文件时发生未知错误: {e}"}, status_code=500)


# 模拟器运行接口 (使用 SSE) - 此部分无变化
@app.get("/run-simulation/")
async def run_simulation(buy_intention: str):
    
    async def event_stream():
        # 初始化 Flow
        shared = {'buy_is_positive_output': buy_intention, 'try_number': 0}
        flow = ProgressFlow()
        flow.start(purchase_decision_judgment)

        try:
            async for update in flow.run(shared):
                yield f"data: {json.dumps(update)}\n\n"
            
            yield f"data: {json.dumps({'status': 'finished'})}\n\n"
        
        except Exception as e:
            tb_str = traceback.format_exc()
            print(f"\n--- FastAPI Stream 捕获到致命错误 ---")
            print(tb_str)
            print(f"--- 流程已强行终止 ---\n")
            
            error_message = {
                'status': 'error',
                'output': f"服务器流程意外终止: {e}", 
                'log': { 
                    'error': str(e), 
                    'traceback': tb_str
                }
            }
            yield f"data: {json.dumps(error_message)}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)