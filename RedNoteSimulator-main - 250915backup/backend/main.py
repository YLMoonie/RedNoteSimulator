# file: backend/main.py

import asyncio
import json
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from flow import ProgressFlow, purchase_decision_judgment
import os

# --- 新增代码：获取正确的路径 ---
# 获取 main.py 文件所在的目录
current_dir = os.path.dirname(os.path.abspath(__file__))
# 构建到 frontend 目录的绝对路径
frontend_dir = os.path.join(current_dir, "..", "frontend")
# 构建到 index.html 的绝对路径
index_html_path = os.path.join(frontend_dir, "index.html")


# 创建 FastAPI 应用
app = FastAPI()

# --- 修改代码：使用绝对路径挂载静态文件目录 ---
app.mount("/frontend", StaticFiles(directory=frontend_dir), name="frontend")


# --- 修改代码：使用绝对路径返回 index.html ---
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    try:
        with open(index_html_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read(), status_code=200)
    except FileNotFoundError:
        return HTMLResponse(content="<h1>错误：找不到 index.html</h1><p>请确保您的 frontend 文件夹和 index.html 文件位于正确的位置。</p>", status_code=404)


# 模拟器运行接口 (使用 SSE) - 此部分无变化
@app.get("/run-simulation/")
async def run_simulation(buy_intention: str):
    
    async def event_stream():
        # 初始化 Flow
        shared = {'buy_is_positive_output': buy_intention, 'try_number': 0}
        flow = ProgressFlow()
        flow.start(purchase_decision_judgment)

        # 调用修改后的 run 方法，它现在是一个生成器
        # 这个生成器会持续 yield 更新信息
        try:
            # 使用 async for 循环来接收来自 flow 的实时更新
            async for update in flow.run(shared):
                # 将更新数据转换为 JSON 字符串并通过 SSE 发送
                yield f"data: {json.dumps(update)}\n\n"
            
            # 发送一个结束信号
            yield f"data: {json.dumps({'status': 'finished'})}\n\n"
        
        except Exception as e:
            import traceback
            # 如果出错，发送详细的错误信息
            error_message = {'status': 'error', 'error': str(e), 'traceback': traceback.format_exc()}
            yield f"data: {json.dumps(error_message)}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")


if __name__ == "__main__":
    import uvicorn
    # 运行服务器
    uvicorn.run(app, host="0.0.0.0", port=8000)