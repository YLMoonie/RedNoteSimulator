# file: backend/rns_utils/ToolNode.py

from pocketflow import Node, Flow
from rns_utils.llm import Pooling
from dotenv import load_dotenv

import os

load_dotenv()

base_url = os.getenv("BASE_URL", "")
api_keys_string = os.getenv("API_LIST", [])
api_list = [key.strip() for key in api_keys_string.split(',') if key.strip()]
pooling_example = Pooling(API_LIST=api_list, BASE_URL=base_url)
# call_llm 实例将由 flow.py 覆盖
call_llm = pooling_example.call_llm


'''
CodeExecute Node
Function: execute code and save the outputs
Init: code, data_names (should APPEAR in the code)
Prep: None
Post: args
'''
class CodeExecute(Node):
    def __init__(self, code, *args):
        super().__init__()
        self.code = code
        self.outputs = args

    def exec(self,prep_res):
        # prep_res 就是 shared 字典
        local_scope = {'shared': prep_res}
        try:
            exec(self.code, {}, local_scope)
            # CodeExecute 节点不直接返回给前端有意义的输出
            # 它的主要作用是修改 shared 状态
            return "Code executed successfully", None
        except Exception as e:
            error_message = f"Error executing code: {e}"
            print(error_message)
            return error_message, None

    def post(self,shared,prep_res,exec_res):
        # exec 已经通过 local_scope['shared'] 修改了 shared 字典
        # post 方法在这里的任务是确保流程可以继续
        # 它不需要返回特定的动作，所以返回 None 即可
        return None