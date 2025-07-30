'''
Purchase Decision Judgment:
Function:Based on the value of the 'buyIsPositive' variable in the shared state, it returns a string that represents the branch to take.
Prep: Prepares the necessary variable for the decision from the shared state.
Exec: Executes the decision logic and returns "CASE_1" or "CASE_2".
Post: No operation is performed, as the decision result is used directly by the Flow controller.
'''

class PurchaseDecisionJudgment(Node):
    def prep(self, shared):
        return shared.get('buy_is_positive', '')

    def exec(self, prep_res):
        buy_is_positive = prep_res
        if buy_is_positive == '0':
            return "CASE_1"
        else:
            return "CASE_2"
        
'''
User Browse Judgment:
Function : Based on the users' Browsing action, it returns a string that represents the branch to take.
Prep: user_browse_check_output
Exec: "CASE_1","CASE_2"
Post:No operation is performed, as the decision result is used directly by the Flow controller.
'''        
        
class UserBrowseJudgment(Node):
    def prep(self,shared):
        return shared.get('user_browse_check_output','')
    def exec(self,prep_res):
        user_browse_check=prep_res
        if user_browse_check=='1':
            return "CASE_1"
        else:
            return "CASE_2"

'''
Interaction Judgment:
Function: Based on the users' interaction behavior, it returns a string that represents the branch to take.
Post: user_interaction_judge_output
Exec:"CASE_1","CASE_2"
'''
class InteractionJudgment(Node):
    def prep(self,shared):
        return shared.get('user_interaction_judge_output','')
    def exec(self,prep_res):
        user_interaction_judge=prep_res
        if user_interaction_judge=='0':
            return "CASE_2"
        else:
            return "CASE_1"

'''
Interaction Object Judgment:
Function: Based on the users' interaction object(poster or other users), it returns a string that represents the branch to take.
Post:user_interaction_judge_output
Exec:"CASE_1","CASE_2"
'''

class InteractionObjectJudgment(Node):
    def prep(self,shared):
        return shared.get('user_interaction_judge_output','')
    def exec(self,prep_res):
        user_interaction_judge=prep_res
        if user_interaction_judge=='1222':
            return "CASE_1"
        else:
            return "CASE_2"


"""
Loop Controller:
功能: Based on shared.'try_number' , it decides to continue or exit loop
Prep: 'try_number'
Exec: "CONTINUE_LOOP" , "EXIT_LOOP"
    """
class LoopController(Node):
    def prep(self, shared):
        shared.setdefault('try_number', 0)
    def exec(self, prep_res):
        current_try = shared['try_number']
        
        if current_try < 10:
            shared['try_number'] += 1
            return "CONTINUE_LOOP"
        else:
            return "EXIT_LOOP"


