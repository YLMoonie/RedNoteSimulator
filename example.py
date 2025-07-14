from pocketflow import Node, Flow
from rns_utils.llm import Pooling
from dotenv import load_dotenv

import os

load_dotenv()

#定义llm调用函数，复制粘贴就行
base_url = os.getenv("BASE_URL", "")
api_keys_string = os.getenv("API_LIST", [])
api_list = [key.strip() for key in api_keys_string.split(',') if key.strip()]
pooling_example = Pooling(API_LIST=api_list, BASE_URL=base_url)
call_llm = pooling_example.call_llm

#定义节点：prep、exct、post三函数及各自的参数，其中prep_res、exct_res分别是prep、exct函数的返回值
#注意类定义时选择基类，即Pockeflow的Node
#记得写每个节点的注释，四行：节点名、功能、prep读取shared中的参数、post到shared的参数
'''
Joke Generate Node
Function: Use LLM generate a joke in specific topic
Prep: topic
Post: joke
'''
class JokeGenerate(Node):
    def prep(self,shared):
        topic = shared.get("topic", "Work")
        prompt = f"Please generate a joke about {topic}"
        print()
        return prompt

    def exec(self,prep_res):
        print("### The joke generated is:")
        joke = call_llm(prep_res)
        print()
        return joke

    def post(self,shared,prep_res,exec_res):
        joke = exec_res
        shared['joke'] = joke

'''
Content Check Node
Function: Use LLM check the content of the joke
Prep: joke
Post: result
'''
class ContentCheck(Node):
    def prep(self,shared):
        joke = shared.get("joke", "Please output 'There is no joke, please check.'")
        prompt = f"Please check the following content if it has illegal or sensitive content: \n {joke}"
        return prompt

    def exec(self,prep_res):
        prompt = prep_res
        print("### The check result is:")
        check_result = call_llm(prompt)
        print()
        return check_result

    def post(self,shared,prep_res,exec_res):
        shared['result'] = exec_res

#将节点从类实体化
joke_generate = JokeGenerate()
content_check = ContentCheck()

#编排节点顺序
joke_generate >> content_check

flow = Flow()              #实体化流
flow.start(joke_generate)  #设置流起点

topic=input("### Please input the topic of the joke:\n")
shared = {'topic': topic}  #设置shared，shared是字典类型（名称不一定是shared，可以自定义）

flow.run(shared)           #运行流，传入的参数是shared字典