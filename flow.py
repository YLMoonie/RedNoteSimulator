from pocketflow import Node, Flow
from rns_utils.llm import Pooling
from dotenv import load_dotenv
from rns_utils.ToolNode import CodeExecute
import openai
import os
import re
import warnings
import datetime

# 导入所有需要的节点和分支判断
from branch import PurchaseDecisionJudgment,UserBrowseJudgment,InteractionJudgment,InteractionObjectJudgment,LoopController
from node import UserInformationCreate1,UserInformationCreate2,USER_SearchWordCreate,RECOMMEND_DisturbanceCreate,UserFeatureCreate,RECOMMEND_ContentGenerate,RECOMMEND_ContentDecide1,RECOMMEND_ContentDecide2,USER_BrowseCheck,USER_PsychologicalInfoCreate,USER_InteractionJudge,USER_InteractionInfoCreate1,USER_InteractionInfoCreate2,POSTER_InteractionFeedbackCreate,USER_PsychologicalInfoCreate1,USER_CommentCreate,USER_CommentToInteractSelect,OTHERUSER_InteractionFeedbackCreate,USER_PsychologicalInfoCreate2,USER_PurchaseDecide1,USER_PurchaseDecide2
from code import code_parameter_extractor1, code_parameter_extractor2, code_post_info

load_dotenv()

# --- 1. 设置LLM和日志文件 ---
base_url = os.getenv("BASE_URL", "")
api_keys_string = os.getenv("API_LIST", [])
api_list = [key.strip() for key in api_keys_string.split(',') if key.strip()]
pooling_example = Pooling(API_LIST=api_list, BASE_URL=base_url)
original_call_llm = pooling_example.call_llm
OUTPUT_FILENAME = "llm_output.txt"

with open(OUTPUT_FILENAME, "w", encoding="utf-8") as f:
    f.write(f"Flow run started at: {datetime.datetime.now()}\n")
    f.write("="*50 + "\n\n")

CURRENT_NODE_NAME = ""

def call_llm_and_log(prompt, instruction="You are an AI assistant.", **kwargs):
    # 【重要】强制 stream=False 来调用我们修改过的、不会打印到终端的 llm_core
    response = original_call_llm(prompt=prompt, instruction=instruction, stream=False, **kwargs)
    
    with open(OUTPUT_FILENAME, "a", encoding="utf-8") as f:
        f.write(f"--- Node: {CURRENT_NODE_NAME} ---\n")
        f.write(f"--- Instruction ---\n{instruction}\n\n")
        f.write(f"--- Prompt ---\n{prompt}\n\n")
        f.write(f"--- LLM Response ---\n{response}\n\n")
        f.write("="*50 + "\n\n")
        
    return response

# 全局替换
pooling_example.call_llm = call_llm_and_log
call_llm = call_llm_and_log

# --- 2. 创建一个带进度跟踪的自定义Flow类 ---
class ProgressFlow(Flow):
    def run(self, shared):
        global CURRENT_NODE_NAME
        print("🚀 Flow starting...")
        
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
        
        while curr:
            CURRENT_NODE_NAME = curr.__class__.__name__
            
            # vvvv 【重要修正】重写进度条计算逻辑 vvvv
            progress = 0
            if CURRENT_NODE_NAME != "LoopController" and shared.get('try_number', 0) == 0:
                # 循环前
                pre_loop_node_count += 1
                progress = (pre_loop_node_count / PRE_LOOP_NODES_ESTIMATE) * PRE_LOOP_WEIGHT
            elif CURRENT_NODE_NAME == "UserDecisionReportCreate":
                # 最终报告节点
                progress = PRE_LOOP_WEIGHT + LOOP_WEIGHT + (POST_LOOP_WEIGHT * 0.5)
            else:
                # 循环中
                loop_num = shared.get('try_number', 1) -1 # 当前是第几次循环 (0-9)
                progress = PRE_LOOP_WEIGHT + (loop_num / 10) * LOOP_WEIGHT

            print(f"🔄 Progress: {min(progress, 99.9):.2f}% - Running node: {CURRENT_NODE_NAME}")
            
            curr.set_params(p)
            last_action = curr._run(shared)
            
            if CURRENT_NODE_NAME == "UserDecisionReportCreate":
                print(f"🔄 Progress: 100.00% - Node {CURRENT_NODE_NAME} finished.")
            
            curr = self.get_next_node(curr, last_action)
        
        print(f"✅ Flow finished successfully! Check '{OUTPUT_FILENAME}' for detailed LLM outputs.")
        return last_action

# --- 3. 节点定义 ---
class ParameterExtractor(Node):
    def __init__(self, code_to_run: str):
        super().__init__()
        self.code_string = code_to_run

    def prep(self, shared):
        return shared

    def exec(self, prep_res):
        shared_dict = prep_res
        try:
            exec(self.code_string, globals(), {'shared': shared_dict})
        except Exception as e:
            # 打印更详细的错误信息以帮助调试
            warnings.warn(f"CodeExecute in {self.__class__.__name__} failed: {e}")
            # print("--- Failing code string ---")
            # print(self.code_string)
            # print("--- Shared content that caused failure ---")
            # print(shared_dict.get('content_recommendation_output', ''))
            # print("---------------------------")


class UserDecisionReportCreate(Node):
    def prep(self,shared):
        # ... (无变化)
        return shared.get("post_info_output",""),shared.get("poster_identity_output",""),shared.get("post_title_output",""),shared.get("post_classification_output",""),shared.get("post_content_output",""),shared.get("like_num_output",""),shared.get("cmt_num_output",""),shared.get("fwd_num_output",""),shared.get("USER_browse_check_output", ""),shared.get("USER_interaction_judge_output", ""),shared.get("USER_purchase_decide2_output",""),shared.get("USER_psychological_info_create_output",""),shared.get("USER_psychological_info_create2_output","")

    def exec(self, prep_res):
        # ... (无变化)
        post_info,poster_identity,post_title,post_classification,post_content,like_num,cmt_num,fwd_num,is_browse,is_interact,is_buy,browse_psychology_infomation,interact_psychology_information = prep_res
        instruction = "你是一位用户行为分析师。"
        prompt = f"""请根据以下详细的用户行为数据和心理活动记录，生成一份专业、有洞察的用户决策报告。

    ### 用户行为数据
    - **帖子列表**: {post_info}
    - **帖主身份**: {poster_identity}
    - **帖子标题**: {post_title}
    - **帖子分类**: {post_classification}
    - **帖子内容**: {post_content}
    - **帖子热度**: {like_num}点赞, {cmt_num}评论, {fwd_num}转发

    ### 用户决策路径
    - **是否浏览帖子**: {is_browse}
    - **是否与帖子交互**: {is_interact}
    - **最终是否购买**: {is_buy}

    ### 用户心理活动分析
    - **浏览帖子时的心理活动**: {browse_psychology_infomation}
    - **与帖子交互后的心理活动**: {interact_psychology_information}
"""
        response = call_llm(prompt=prompt, instruction=instruction)
        return response


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

# --- 6. 启动工作流 (无变化) ---
if __name__ == "__main__":
    try:
        purchase_decision_judgment_output = str(input("程序已准备就绪，请输入用户初始购买意愿 (1 表示想买, 0 表示随便看看): "))
        if purchase_decision_judgment_output not in ['0', '1']:
            raise ValueError("输入无效，请输入 0 或 1.")
            
        shared = {'buy_is_positive_output': purchase_decision_judgment_output, 'try_number': 0}
        
        flow = ProgressFlow()
        flow.start(purchase_decision_judgment)
        flow.run(shared)

    except (ValueError, KeyboardInterrupt) as e:
        print(f"\n程序已终止。原因: {e}")
    except Exception as e:
        print(f"\n程序运行出错: {e}")