from pocketflow import Node
from rns_utils.llm import Pooling
from dotenv import load_dotenv

import os

load_dotenv()

base_url = os.getenv("BASE_URL", "")
api_keys_string = os.getenv("API_LIST", [])
api_list = [key.strip() for key in api_keys_string.split(',') if key.strip()]
pooling_example = Pooling(API_LIST=api_list, BASE_URL=base_url)
call_llm = pooling_example.call_llm

'''
Purchase Decision Judgment:
Function:Based on the value of the 'buy_Is_positive_output' variable in the shared state, it returns a string that represents the branch to take.
Prep: Prepares the necessary variable for the decision from the shared state.
Exec: Executes the decision logic and returns "CASE_1" or "CASE_2".
Post: No operation is performed, as the decision result is used directly by the Flow controller.
'''

class PurchaseDecisionJudgment(Node):
    def prep(self, shared):
        return shared.get('buy_is_positive_output', '')

    def exec(self, prep_res):
        buy_is_positive = prep_res
        if buy_is_positive == '1':
            return "CASE_1"
        else:
            return "CASE_2"
            
    # vvvv 添加这个 post 方法 vvvv
    def post(self, shared, prep_res, exec_res):
        return exec_res # 直接返回 exec 的结果 ('CASE_1' 或 'CASE_2')
        
'''
User Browse Judgment:
Function : Based on the users' Browsing action, it returns a string that represents the branch to take.
Prep: USER_browse_check_output
Exec: "CASE_1","CASE_2"
Post:No operation is performed, as the decision result is used directly by the Flow controller.
'''        
        
class UserBrowseJudgment(Node):
    def prep(self,shared):
        return shared.get('USER_browse_check_output','')
    def exec(self,prep_res):
        user_browse_check=prep_res
        if user_browse_check=='0':
            return "CASE_1"
        else:
            return "CASE_2"
    def post(self, shared, prep_res, exec_res):
        return exec_res

'''
Interaction Judgment:
Function: Based on the users' interaction behavior, it returns a string that represents the branch to take.
Post: USER_interaction_judge_output
Exec:"CASE_1","CASE_2"
'''
class InteractionJudgment(Node):
    def prep(self,shared):
        return shared.get('USER_interaction_judge_output','')
    def exec(self,prep_res):
        user_interaction_judge=prep_res
        if user_interaction_judge=='0':
            return "CASE_2"
        else:
            return "CASE_1"
            
    # vvvv 添加这个 post 方法 vvvv
    def post(self, shared, prep_res, exec_res):
        return exec_res

'''
Interaction Object Judgment:
Function: Based on the users' interaction object(poster or other users), it returns a string that represents the branch to take.
Post:user_interaction_judge_output
Exec:"CASE_1","CASE_2"
'''

class InteractionObjectJudgment(Node):
    def prep(self,shared):
        return shared.get('USER_interaction_judge_output','')
    def exec(self,prep_res):
        user_interaction_judge=prep_res
        if user_interaction_judge=='1222':
            return "CASE_1"
        else:
            return "CASE_2"

    # vvvv 添加这个 post 方法 vvvv
    def post(self, shared, prep_res, exec_res):
        return exec_res


"""
Loop Controller:
功能: Based on shared.'try_number' , it decides to continue or exit loop
Prep: 'try_number'
Exec: "CONTINUE_LOOP" , "EXIT_LOOP"
    """
class LoopController(Node):
    def prep(self, shared):
        # 准备当前循环次数给 exec
        return shared.get('try_number', 0)

    def exec(self, prep_res):
        current_try = prep_res # 从 prep 获取当前次数

        if current_try < 10:
            return "CONTINUE_LOOP"
        else:
            return "EXIT_LOOP"

    def post(self, shared, prep_res, exec_res):
        # 在 post 方法中安全地更新 shared 字典
        current_try = prep_res
        shared['try_number'] = current_try + 1
        return exec_res

