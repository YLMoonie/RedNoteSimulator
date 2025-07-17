from pocketflow import Node, Flow
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
CodeExecute Node
Function: execute code and save the outputs
Init: code, data_names (should APPEAR in the code)
Prep: None
Post: args
'''
class CodeExecute(Node):
    def __init__(self, code, *args):      #eg. a=CodeExecute(code, 'c', 'd')
        super().__init__()
        self.code = code
        self.outputs = args

    def exec(self,prep_res):
        local_scope={}
        exec(self.code, {}, local_scope)
        results = [local_scope[var] for var in self.outputs]
        return results;

    def post(self,shared,prep_res,exec_res):
        for i,j in zip(self.outputs, exec_res):
            shared[i] = j

code = "a,b = 3,4 \nc, d = a+b, a-b"       #There should be no blank after '\n', or you will get a Traceback!
flow = Flow()
a=CodeExecute(code, 'c', 'd')
flow.start(a)
shared={}
flow.run(shared)
print(shared)