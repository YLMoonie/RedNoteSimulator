# file: backend/flow.py

from pocketflow import Node, Flow
from rns_utils.llm import Pooling
from dotenv import load_dotenv
from rns_utils.ToolNode import CodeExecute
import openai
import os
import re
import warnings
import datetime
import asyncio

# 导入所有需要的节点和分支判断
from branch import PurchaseDecisionJudgment,UserBrowseJudgment,InteractionJudgment,InteractionObjectJudgment,LoopController
from node import UserInformationCreate1,UserInformationCreate2,USER_SearchWordCreate,RECOMMEND_DisturbanceCreate,UserFeatureCreate,RECOMMEND_ContentGenerate,RECOMMEND_ContentDecide1,RECOMMEND_ContentDecide2,USER_BrowseCheck,USER_PsychologicalInfoCreate,USER_InteractionJudge,USER_InteractionInfoCreate1,USER_InteractionInfoCreate2,POSTER_InteractionFeedbackCreate,USER_PsychologicalInfoCreate1,USER_CommentCreate,USER_CommentToInteractSelect,OTHERUSER_InteractionFeedbackCreate,USER_PsychologicalInfoCreate2,USER_PurchaseDecide1,USER_PurchaseDecide2, UserDecisionReportCreate
from code import code_parameter_extractor1, code_parameter_extractor2, code_post_info

load_dotenv()

# --- 1. 设置LLM ---
base_url = os.getenv("BASE_URL", "")
api_keys_string = os.getenv("API_LIST", [])
api_list = [key.strip() for key in api_keys_string.split(',') if key.strip()]
pooling_example = Pooling(API_LIST=api_list, BASE_URL=base_url)
original_call_llm = pooling_example.call_llm

CURRENT_NODE_NAME = ""

# --- 修改 call_llm_and_log 函数 ---
# 它不再写入文件，而是返回一个包含日志信息的字典
def call_llm_and_log(prompt, instruction="You are an AI assistant.", **kwargs):
    # 【重要】强制 stream=False
    response = original_call_llm(prompt=prompt, instruction=instruction, stream=False, **kwargs)
    
    log_data = {
        "node_name": CURRENT_NODE_NAME,
        "instruction": instruction,
        "prompt": prompt,
        "llm_response": response
    }
    
    # 将日志数据作为函数结果的一部分返回
    return response, log_data

# 全局替换
pooling_example.call_llm = call_llm_and_log
# 更新 node.py 中使用的 call_llm 实例
import node
node.call_llm = call_llm_and_log


# --- 2. 创建一个带进度跟踪的自定义Flow类 ---
class ProgressFlow(Flow):
    async def run(self, shared):
        global CURRENT_NODE_NAME
        
        # 定义流程阶段的权重
        PRE_LOOP_WEIGHT = 15  # 前置节点占15%
        LOOP_WEIGHT = 80      # 10次循环占80%
        POST_LOOP_WEIGHT = 5  # 最终报告占5%

        # 估算前置节点的数量
        pre_loop_node_count = 0
        PRE_LOOP_NODES_ESTIMATE = 7

        curr = self.start_node
        p = {**self.params}
        last_action = None
        
        node_index = 0
        while curr:
            CURRENT_NODE_NAME = curr.__class__.__name__
            node_index += 1
            
            # vvvv 进度计算逻辑 vvvv
            progress = 0
            if CURRENT_NODE_NAME != "LoopController" and shared.get('try_number', 0) == 0:
                # 循环前
                pre_loop_node_count += 1
                progress = (pre_loop_node_count / PRE_LOOP_NODES_ESTIMATE) * PRE_LOOP_WEIGHT
            elif CURRENT_NODE_NAME == "UserDecisionReportCreate":
                # 最终报告节点
                progress = PRE_LOOP_WEIGHT + LOOP_WEIGHT
            else:
                # 循环中
                loop_num = shared.get('try_number', 0) # 当前是第几次循环 (0-9)
                progress = PRE_LOOP_WEIGHT + (loop_num / 10) * LOOP_WEIGHT

            # --- 关键修改 ---
            # 使用 yield 返回当前节点的启动信息
            start_update = {
                "id": node_index,
                "node_name": CURRENT_NODE_NAME,
                "progress": min(progress, 100),
                "status": "running",
                "output": None,
                "log": None
            }
            yield start_update

            curr.set_params(p)
            
            # 运行节点
            prep_res = curr.prep(shared)
            exec_res = curr.exec(prep_res)
            last_action = curr.post(shared, prep_res, exec_res)
            
            # 从 exec_res 中解包结果和日志
            run_result, full_log = exec_res if isinstance(exec_res, tuple) and len(exec_res) == 2 else (exec_res, None)

            # --- 关键修改 ---
            # 使用 yield 返回当前节点的完成信息和输出
            done_update = {
                "id": node_index,
                "node_name": CURRENT_NODE_NAME,
                "progress": min(progress, 100),
                "status": "completed",
                "output": str(run_result), # 确保输出是可序列化的字符串
                "log": full_log
            }
            yield done_update
            
            # 模拟异步延迟，防止事件发送过快
            await asyncio.sleep(0.1)

            if CURRENT_NODE_NAME == "UserDecisionReportCreate":
                final_progress_update = {
                    "id": node_index,
                    "node_name": CURRENT_NODE_NAME,
                    "progress": 100,
                    "status": "completed",
                    "output": str(run_result),
                    "log": full_log
                }
                yield final_progress_update

            curr = self.get_next_node(curr, last_action)


# --- 3. 节点定义 (ParameterExtractor) ---
# 注意：UserDecisionReportCreate 已移至 node.py
class ParameterExtractor(Node):
    def __init__(self, code_to_run: str):
        super().__init__()
        self.code_string = code_to_run

    def prep(self, shared):
        return shared

    def exec(self, prep_res):
        shared_dict = prep_res
        try:
            # 创建一个临时的 `shared` 变量用于 exec
            exec_globals = {'shared': shared_dict}
            exec(self.code_string, {}, exec_globals)
        except Exception as e:
            warnings.warn(f"CodeExecute in {self.__class__.__name__} failed: {e}")
        
        # 这个节点不直接返回有意义的结果给前端，主要是修改 shared 状态
        return "Parameters extracted", None

    def post(self, shared, prep_res, exec_res):
        # exec 已经修改了 prep_res (shared_dict)，所以这里不需要额外操作
        pass


# --- 4 & 5. 实例化节点和定义工作流路径（无变化） ---
purchase_decision_judgment = PurchaseDecisionJudgment()
user_information_create1=UserInformationCreate1()
parameter_extractor_1 = ParameterExtractor(code_parameter_extractor1)
user_information_create2=UserInformationCreate2()
parameter_extractor_2 = ParameterExtractor(code_parameter_extractor2)
USER_search_word_create=USER_SearchWordCreate()
RECOMMEND_disturbance_create=RECOMMEND_DisturbanceCreate()
user_feature_create=UserFeatureCreate()
RECOMMEND_content_generate=RECOMMEND_ContentGenerate()
RECOMMEND_content_decide1=RECOMMEND_ContentDecide1()
RECOMMEND_content_decide2=RECOMMEND_ContentDecide2()
post_info=ParameterExtractor(code_post_info)
USER_browse_check=USER_BrowseCheck()
USER_psychological_info_create=USER_PsychologicalInfoCreate()
USER_interaction_judge=USER_InteractionJudge()
USER_interaction_info_create1=USER_InteractionInfoCreate1()
POSTER_interaction_feedback_create=POSTER_InteractionFeedbackCreate()
USER_psychological_info_create1=USER_PsychologicalInfoCreate1()
USER_interaction_info_create2=USER_InteractionInfoCreate2()
USER_comment_create=USER_CommentCreate()
USER_comment_to_interact_select=USER_CommentToInteractSelect()
OTHERUSER_interaction_feedback_create=OTHERUSER_InteractionFeedbackCreate()
USER_psychological_info_create2=USER_PsychologicalInfoCreate2()
USER_purchase_decide1=USER_PurchaseDecide1()
USER_purchase_decide2=USER_PurchaseDecide2()
user_browse_judgment=UserBrowseJudgment()
interaction_judgment=InteractionJudgment()
interaction_object_judgment=InteractionObjectJudgment()
loop_controller=LoopController()
user_decision_report_create=UserDecisionReportCreate()

(purchase_decision_judgment - "CASE_1" >> user_information_create1 >> parameter_extractor_1 >> USER_search_word_create >> RECOMMEND_content_generate >> RECOMMEND_content_decide1)
(purchase_decision_judgment - "CASE_2" >> user_information_create2 >> parameter_extractor_2 >> RECOMMEND_disturbance_create >> user_feature_create >> RECOMMEND_content_decide2)
RECOMMEND_content_decide1 >> post_info
RECOMMEND_content_decide2 >> post_info
post_info >> loop_controller
loop_controller - "EXIT_LOOP" >> user_decision_report_create
(loop_controller - "CONTINUE_LOOP" >> USER_browse_check >> user_browse_judgment)
user_browse_judgment - "CASE_1" >> loop_controller
(user_browse_judgment - "CASE_2" >> USER_psychological_info_create >> USER_interaction_judge >> interaction_judgment)
(interaction_judgment - "CASE_2" >> USER_purchase_decide1 >> loop_controller)
(interaction_judgment - "CASE_1" >> interaction_object_judgment)
(interaction_object_judgment - "CASE_1" >> USER_interaction_info_create1 >> POSTER_interaction_feedback_create >> USER_psychological_info_create1 >> USER_purchase_decide2 >> loop_controller)
(interaction_object_judgment - "CASE_2" >> USER_comment_create >> USER_comment_to_interact_select >> USER_interaction_info_create2 >> OTHERUSER_interaction_feedback_create >> USER_psychological_info_create2 >> USER_purchase_decide2 >> loop_controller)


# --- 6. 启动工作流 (此部分仅用于本地测试，FastAPI会直接调用ProgressFlow) ---
if __name__ == "__main__":
    # 这个部分现在由 FastAPI 的 main.py 控制，可以保留用于独立的后端测试
    async def main():
        try:
            purchase_decision_judgment_output = "1"
            shared = {'buy_is_positive_output': purchase_decision_judgment_output, 'try_number': 0}
            
            flow = ProgressFlow()
            flow.start(purchase_decision_judgment)
            
            print("🚀 Flow starting for local test...")
            async for update in flow.run(shared):
                print(f"🔄 Update: {update['node_name']} - {update['status']} - Progress: {update['progress']:.2f}%")
                if update['status'] == 'completed':
                    print(f"   Output: {update['output']}")
            print("✅ Flow finished successfully!")

        except Exception as e:
            print(f"\n程序运行出错: {e}")

    asyncio.run(main())