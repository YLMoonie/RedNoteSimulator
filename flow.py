from pocketflow import Node, Flow
from rns_utils.llm import Pooling
from dotenv import load_dotenv
from rns_utils.ToolNode import CodeExecute
import openai
import os
import re
import warnings

load_dotenv()

#定义llm调用函数，复制粘贴就行
base_url = os.getenv("BASE_URL", "")
api_keys_string = os.getenv("API_LIST", [])
api_list = [key.strip() for key in api_keys_string.split(',') if key.strip()]
pooling_example = Pooling(API_LIST=api_list, BASE_URL=base_url)
call_llm = pooling_example.call_llm


purchase_decision_judgment = PurchaseDecisionJudgment()
user_information_create1=UserInformationCreate1()
user_information_create2=UserInformationCreate2()
USER_search_word_create=USER_SearchWordCreate()
RECOMMEND_disturbance_create=RECOMMEND_DisturbanceCreate()
user_feature_create=UserFeatureCreate()
RECOMMEND_content_generate=RECOMMEND_ContentGenerate()
RECOMMEND_content_decide1=RECOMMEND_ContentDecide1()
RECOMMEND_content_decide2=RECOMMEND_ContentDecide2()
user_decision_report_create=UserDecisionReportCreate()


USER_browse_check=USER_BrowseCheck()
USER_psychological_info_create=USER_PsychologicalInfoCreate()
USER_interaction_judge=USER_InteractionJudge()
USER_interaction_info_create=USER_InteractionInfoCreate()
POSTER_interaction_feedback_create=POSTER_InteractionFeedbackCreate()
USER_psychological_info_create1=USER_PsychologicalInfoCreate1()
USER_comment_create=USER_CommentCreate()
USER_comment_to_interact_select=USER_CommentToInteractSelect()
USER_interaction_info_create=USER_InteractionInfoCreate()
OTHERUSER_interaction_feedback_create=OTHERUSER_InteractionFeedbackCreate()
USER_psychological_info_create2=USER_PsychologicalInfoCreate2()
USER_purchase_decide1=USER_PurchaseDecide1()
USER_purchase_decide2=USER_PurchaseDecide2()
user_browse_judgment=User_Browse_Judgment()
interaction_judgment=InteractionJudgment()
interaction_object_judgment=InteractionObjectJudgment()
loop_controller=LoopController()

class ParameterExtractor(Node):
    def __init__(self, code_to_run: str):
        super().__init__()
        self.code_string = code_to_run

    def prep(self, shared):
        return shared

    def exec(self, prep_res):
        shared_dict = prep_res
        # UPDATED: 调用从 rns_utils 库导入的 CodeExecute 函数
        execution_results = CodeExecute(self.code_string, shared_dict)
        # 假设该函数在成功时返回真值，失败时返回假值
        if not execution_results:
            warnings.warn(f"CodeExecute 函数执行失败: {self.code_string[:50]}...")

parameter_extractor_1 = ParameterExtractor(code_parameter_extractor1)
parameter_extractor_2 = ParameterExtractor(code_parameter_extractor2)
post_info=ParameterExtractor(code_post_info)


(purchase_decision_judgment - "CASE_1" >> user_information_create1
                                       >> parameter_extractor_1
                                       >> USER_search_word_create
                                       >> RECOMMEND_content_generate
                                       >> RECOMMEND_content_decide1)

(purchase_decision_judgment - "CASE_2" >> user_information_create2
                                       >> parameter_extractor_2
                                       >> RECOMMEND_disturbance_create
                                       >> user_feature_create
                                       >> RECOMMEND_content_decide2)

# --- Both branches now converge on post_info before entering the loop ---
RECOMMEND_content_decide1 >> post_info
RECOMMEND_content_decide2 >> post_info
post_info >> loop_controller

# --- Loop exit path ---
loop_controller - "EXIT_LOOP" >> user_decision_report_create

# --- Loop body path (logic remains the same as before) ---
(loop_controller - "CONTINUE_LOOP" >> USER_browse_check >> user_browse_judgment)
user_browse_judgment - "CASE_1" >> loop_controller
(user_browse_judgment - "CASE_2" >> USER_psychological_info_create >> USER_interaction_judge >> interaction_judgment)
(interaction_judgment - "CASE_2" >> USER_purchase_decide1 >> loop_controller)
(interaction_judgment - "CASE_1" >> interaction_object_judgment)
(interaction_object_judgment - "CASE_1" >> USER_interaction_info_create >> POSTER_interaction_feedback_create >> USER_psychological_info_create1 >> USER_purchase_decide2 >> loop_controller)
(interaction_object_judgment - "CASE_2" >> USER_comment_create >> USER_comment_to_interact_select >> USER_interaction_info_create >> OTHERUSER_interaction_feedback_create >> USER_psychological_info_create2 >> USER_purchase_decide2 >> loop_controller)

flow = Flow()
flow.start(purchase_decision_judgment)
purchase_decision_judgment_output=str(input())
shared = {'purchase_decision_judgment_output': purchase_decision_judgment_output}
flow.run(shared)  


