# RedNote 用户决策模拟器

## 项目简介
RedNote 用户决策模拟器是一个基于 [PocketFlow](https://github.com/datawhalechina/pocketflow) 构建的多智能体流程系统，用于模拟用户在小红书（RedNote）上的浏览、互动以及最终购买决策的全过程。系统通过串联多个智能体节点，逐步生成用户画像、推荐内容、心理活动以及决策报告，帮助运营或产品人员在离线环境下复现真实用户的决策链路。

- **核心目标**：还原用户从看到帖子、产生心理变化、到做出购买与否的路径，并输出可下载的完整报告。
- **主要特性**：
  - PocketFlow 多节点流程编排，包含用户信息生成、推荐扰动、互动判断、循环尝试等 20+ 个节点。
  - FastAPI 后端提供事件流（Server-Sent Events, SSE）接口，实时推送节点执行进度与输出。
  - 前端单页应用展示执行时间线、节点日志、Markdown 报告，并支持 JSON/ZIP 导出。
  - 支持多模型 API Key 池轮询与自动降级，兼容自建或第三方大模型 API。

### 关键参数与输入输出
| 名称 | 类型 | 默认值 / 示例 | 说明 |
| --- | --- | --- | --- |
| `buy_intention` | Query 参数 | `1` 或 `0` | 用户初始购买意向，`1` 表示“明确想买”，`0` 表示“随便看看”。该参数由前端在调用 `/run-simulation/` 时传入，并写入共享状态 `shared['buy_is_positive_output']`。 |
| `try_number` | 共享状态 | `0` | 循环控制计数器，控制流程在特定分支中的重试次数。 |
| `.env` 配置 | 文件 | 见下 | 后端读取 `backend/.env` 中的配置完成模型调用。核心字段包括：<br>• `BASE_URL`：大模型服务的基础地址。<br>• `API_LIST`：逗号分隔的多个 API Key，系统会在调用失败时自动轮换。<br>• `MODEL_NAME`：调用的大模型名称。 |
| SSE 事件 | JSON | 见示例 | 每个节点执行时通过 SSE 推送包含 `id`、`node_name`、`status`、`progress`、`output`、`log` 等字段的事件；流程结束后会推送 `{"status": "finished"}`。 |

**SSE 事件示例：**
```json
{
  "id": 7,
  "node_name": "USER_BrowseCheck",
  "status": "completed",
  "progress": 34.2,
  "output": "用户决定完整浏览推荐的笔记。",
  "log": {
    "prompt": "...",
    "response": "...",
    "latency": 2.41
  }
}
```

### 节点流程概览
PocketFlow 将整个模拟拆解为以下主要阶段：

1. **用户画像阶段**：`UserInformationCreate1/2` 通过大模型生成基础画像、兴趣点和消费意向，并由 `ParameterExtractor` 解析结构化标签。
2. **内容推荐阶段**：`USER_SearchWordCreate` 生成搜索词，`RECOMMEND_DisturbanceCreate` 构造噪声输入，`RECOMMEND_ContentGenerate` 根据画像生成候选笔记，再由 `RECOMMEND_ContentDecide1/2` 决定最终推荐的笔记列表。
3. **浏览与心理阶段**：`USER_BrowseCheck` 记录是否浏览、笔记元数据；`USER_PsychologicalInfoCreate` 捕捉用户的心理变化。
4. **互动阶段**：`USER_InteractionJudge` 判断是否互动，`USER_InteractionInfoCreate*`、`POSTER_InteractionFeedbackCreate`、`OTHERUSER_InteractionFeedbackCreate` 等节点模拟评论互动与反馈。
5. **购买决策阶段**：`USER_PurchaseDecide1/2` 综合前置心理变化输出最终购买结论。
6. **循环与分支控制**：`LoopController`、`UserBrowseJudgment`、`InteractionJudgment`、`InteractionObjectJudgment` 等节点根据用户行为决定是否继续下一轮推荐尝试。
7. **结果汇总**：`UserDecisionReportCreate` 将所有关键数据渲染为 Markdown 报告，供前端以排版良好的形式展示和下载。

完整的节点执行顺序可在前端“模拟路径”时间线中查看，同时也会写入 `backend/llm_output.txt` 作为离线日志备份。

### 目录结构
```
RedNoteSimulator/
├─ backend/               # FastAPI 服务与 PocketFlow 流程定义
│  ├─ main.py             # HTTP 入口，暴露静态页面与 SSE 接口
│  ├─ llm_output.txt      # 最近一次流程的离线日志示例
│  ├─ pocketflow/         # PocketFlow 基础能力封装
│  └─ rns_utils/          # LLM 调度、工具节点等公共模块
└─ frontend/              # 静态前端资源
   ├─ index.html          # 单页应用骨架
   ├─ script.js           # UI 逻辑与 SSE 事件处理
   └─ style.css           # 样式文件
```

## 快速开始
### 1. 环境准备
1. 准备 Python 3.9 及以上版本环境。
2. 安装依赖（FastAPI、Uvicorn、python-dotenv、openai 等）：
   ```bash
   pip install fastapi uvicorn[standard] python-dotenv openai
   ```
3. 在 `backend/` 目录下创建 `.env` 文件，填写模型调用配置：
   ```ini
   BASE_URL=https://your-model-host
   API_LIST=sk-xxx1,sk-xxx2
   MODEL_NAME=gpt-4o-mini
   ```

### 2. 启动后端服务
```bash
cd backend
python main.py
```
- `/`：返回前端页面。
- `/run-simulation/?buy_intention=1`：触发 PocketFlow 流程（SSE）。
- `/get-env-config/`：下载 `.env` 配置（服务端会自动脱敏 API Key）。

在控制台可观察到节点日志；若需要复现日志，可查看 `backend/llm_output.txt`。

## 前端使用指南
1. 浏览器访问 `http://127.0.0.1:8000/`，进入模拟器首页。
2. 在“用户初始购买意愿”下拉框中选择 `明确想买` 或 `随便看看`，点击“开始模拟”。
3. 页面右侧“模拟路径”时间线会实时刷新：
   - 新节点开始执行时标记为 `running`，完成后标记为 `completed`，并按阶段折叠显示。
   - 当前聚焦节点会自动高亮，可点击省略号查看完整历史。
4. 主内容区逐条展示节点的输出结果：
   - 若节点成功，输出区域会展示文字结果，并提供“查看详情(Log)”按钮打开弹窗查看原始 Prompt/Response。
   - 可点击“下载此节点 JSON”将当前节点的结构化数据保存到本地。
5. 当流程完成时，页面底部出现“下载完整报告 (JSON)”“下载节点压缩包 (ZIP)”“下载环境配置 (JSON)”三项操作：
   - **下载完整报告**：导出所有节点的执行记录。
   - **下载节点压缩包**：将已完成节点的 JSON 打包成 ZIP。
   - **下载环境配置**：调用 `/get-env-config/` 获取服务器上的 `.env` 配置（API Key 会被脱敏显示）。
6. 若流程中断或后端报错，页面会以红色节点提示错误信息和堆栈，便于排查。

### 界面交互小贴士
- 时间线采用 IntersectionObserver 自动聚焦当前可视节点，可通过点击时间线中的“...”临时展开全部节点。
- 最终报告为 Markdown 渲染，适合直接复制或导出，默认采用红色主题标题突出重点。
- 若需重新模拟，只需再次选择意向后点击“开始模拟”，系统会自动重置时间线与结果区。

## 深度定制建议
- PocketFlow 节点定义位于 `backend/node.py`、`backend/branch.py` 等文件，可新增或调整节点以覆盖更多用户行为场景。
- `rns_utils/llm.py` 支持多 Key 轮询与流式回调，如需对接私有化模型，可在该模块内扩展调用逻辑。
- 前端的样式和交互可在 `frontend/style.css` 与 `frontend/script.js` 内调整，已预留下载、弹窗等功能接口。

如需进一步的二次开发或集成，可在当前 README 的基础上补充更详细的 API 说明与节点文档。
