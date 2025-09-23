# file: backend/flow.py

from pocketflow import Node, Flow
from rns_utils.llm import Pooling
from dotenv import load_dotenv
from rns_utils.ToolNode import CodeExecute
import openai
import os
import re  # <--- 这是新添加的导入，解决错误的关键
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
def call_llm_and_log(prompt, instruction="You are an AI assistant.", **kwargs):
    response = original_call_llm(prompt=prompt, instruction=instruction, stream=False, **kwargs)
    
    log_data = {
        "node_name": CURRENT_NODE_NAME,
        "instruction": instruction,
        "prompt": prompt,
        "llm_response": response
    }
    
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
        
        PRE_LOOP_WEIGHT = 15
        LOOP_WEIGHT = 80
        POST_LOOP_WEIGHT = 5

        pre_loop_node_count = 0
        PRE_LOOP_NODES_ESTIMATE = 7

        curr = self.start_node
        p = {**self.params}
        last_action = None
        
        node_index = 0
        while curr:
            CURRENT_NODE_NAME = curr.__class__.__name__
            node_index += 1
            
            progress = 0
            if CURRENT_NODE_NAME != "LoopController" and shared.get('try_number', 0) == 0:
                pre_loop_node_count += 1
                progress = (pre_loop_node_count / PRE_LOOP_NODES_ESTIMATE) * PRE_LOOP_WEIGHT
            elif CURRENT_NODE_NAME == "UserDecisionReportCreate":
                progress = PRE_LOOP_WEIGHT + LOOP_WEIGHT
            else:
                loop_num = shared.get('try_number', 0)
                progress = PRE_LOOP_WEIGHT + (loop_num / 10) * LOOP_WEIGHT

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
            
            prep_res = curr.prep(shared)
            # 在执行 exec 之前捕获异常
            try:
                exec_res = curr.exec(prep_res)
            except Exception as e:
                # 如果 exec 失败，立即报告错误并停止流程
                error_update = {
                    "id": node_index,
                    "node_name": CURRENT_NODE_NAME,
                    "progress": progress,
                    "status": "error",
                    "output": f"节点执行失败: {e}",
                    "log": {"error": str(e), "traceback": traceback.format_exc()}
                }
                yield error_update
                import traceback
                traceback.print_exc() # 在服务器端也打印错误
                break # 终止循环

            last_action = curr.post(shared, prep_res, exec_res)
            
            run_result, full_log = exec_res if isinstance(exec_res, tuple) and len(exec_res) == 2 else (exec_res, None)

            done_update = {
                "id": node_index,
                "node_name": CURRENT_NODE_NAME,
                "progress": min(progress, 100),
                "status": "completed",
                "output": str(run_result),
                "log": full_log
            }
            yield done_update
            
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
class ParameterExtractor(Node):
    def __init__(self, code_to_run: str):
        super().__init__()
        self.code_string = code_to_run

    def prep(self, shared):
        return shared

    def exec(self, prep_res):
        shared_dict = prep_res
        try:
            # vvvv 这是关键的修正 vvvv
            # 1. 我们创建一个包含 Python 内置函数的全局作用域
            # 2. 我们将导入的 're' 模块和 'shared' 字典都注入到这个作用域中
            exec_globals = {
                "__builtins__": __builtins__,
                "re": re,  # <--- 将导入的 're' 模块传入
                "shared": shared_dict
            }
            # 当 exec_globals 包含 "shared" 时，locals 可以为空
            exec(self.code_string, exec_globals)
            # ^^^^ 修正结束 ^^^^

        except Exception as e:
            # 这个 UserWarning 会被 FastAPI 捕获并通过 SSE 发送
            warnings.warn(f"CodeExecute in {self.__class__.__name__} failed: {e}")
            raise # 重新引发异常，以便上面的 run 方法能捕获到它

        return "Parameters extracted", None # 成功执行的返回

    def post(self, shared, prep_res, exec_res):
        # prep_res (也就是 shared_dict) 已经被 exec_globals 中的代码修改了
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


# --- 6. 启动工作流 (此部分仅用于本地测试) ---
if __name__ == "__main__":
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