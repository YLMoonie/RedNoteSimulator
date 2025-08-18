from pocketflow import Node, Flow
from rns_utils.llm import Pooling
from dotenv import load_dotenv
from rns_utils.ToolNode import CodeExecute
import openai
import os
import re
import warnings

from branch import PurchaseDecisionJudgment,UserBrowseJudgment,InteractionJudgment,InteractionObjectJudgment,LoopController
from node_l import UserInformationCreate1,UserInformationCreate2,USER_SearchWordCreate,RECOMMEND_DisturbanceCreate,UserFeatureCreate,RECOMMEND_ContentGenerate,RECOMMEND_ContentDecide1,RECOMMEND_ContentDecide2
from node_s import USER_BrowseCheck,USER_PsychologicalInfoCreate,USER_InteractionJudge,USER_InteractionInfoCreate1,USER_InteractionInfoCreate2,POSTER_InteractionFeedbackCreate,USER_PsychologicalInfoCreate1,USER_CommentCreate,USER_CommentToInteractSelect,OTHERUSER_InteractionFeedbackCreate,USER_PsychologicalInfoCreate2,USER_PurchaseDecide1,USER_PurchaseDecide2
from code import code_parameter_extractor1, code_parameter_extractor2, code_post_info
load_dotenv()

#定义llm调用函数，复制粘贴就行
base_url = os.getenv("BASE_URL", "")
api_keys_string = os.getenv("API_LIST", [])
api_list = [key.strip() for key in api_keys_string.split(',') if key.strip()]
pooling_example = Pooling(API_LIST=api_list, BASE_URL=base_url)
call_llm = pooling_example.call_llm

class UserDecisionReportCreate(Node):
    def prep(self,shared):
        return shared.get("post_info_output",""),shared.get("poster_identity_output",""),shared.get("post_title_output",""),shared.get("post_classification_output",""),shared.get("post_content_output",""),shared.get("like_num_output",""),shared.get("cmt_num_output",""),shared.get("fwd_num_output",""),shared.get("USER_browse_check_output", ""),shared.get("USER_interaction_judge_output", ""),shared.get("USER_purchase_decide2_output",""),shared.get("USER_psychological_info_create_output",""),shared.get("USER_psychological_info_create2_output","")

    def exec(self, prep_res):
        post_info,poster_identity,post_title,post_classification,post_content,like_num,cmt_num,fwd_num,is_browse,is_interact,is_buy,browse_psychology_infomation,interact_psychology_information =prep_res
        instruction=f'''用户在浏览小红书时浏览了这些帖子{post_info},根据帖子做了些是否购买该产品的决策，具体内容如下。基于以下内容生成一份用户决策报告。
        {post_info},{poster_identity},{post_title},{post_classification},{post_content},{like_num},{cmt_num},{fwd_num},
        是否浏览：{is_browse}\n 是否交互：{is_interact}\n 是否购买：{is_buy}\n浏览时的心理信息：{browse_psychology_infomation}\n
        帖子中交互产生的心理信息：{interact_psychology_information}
        '''
        prompt=""
        response = call_llm(prompt=prompt, instruction=instruction)
        return response

    def post(self, shared, prep_res, exec_res):
        shared['user_decision_report_create_output'] = exec_res


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
(interaction_object_judgment - "CASE_1" >> USER_interaction_info_create1 >> POSTER_interaction_feedback_create >> USER_psychological_info_create1 >> USER_purchase_decide2 >> loop_controller)
(interaction_object_judgment - "CASE_2" >> USER_comment_create >> USER_comment_to_interact_select >> USER_interaction_info_create2 >> OTHERUSER_interaction_feedback_create >> USER_psychological_info_create2 >> USER_purchase_decide2 >> loop_controller)

purchase_decision_judgment_output = str(input("程序已准备就绪，请输入用户初始购买意愿 (1 表示想买, 0 表示随便看看): "))
shared = {'buy_is_positive_output': purchase_decision_judgment_output}
flow = Flow()
flow.start(purchase_decision_judgment)
flow.run(shared)