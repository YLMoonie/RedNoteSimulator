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
[USER] Search Word Create
Function: Simulate user draft search words
Prep: user_prompt_output, buy_item_output
Post: USER_search_word_create
'''
class USER_SearchWordCreate(Node):
    def prep(self, shared):
        return shared.get("user_prompt_output", ""), shared.get("buy_item_output", "")

    def exec(self,prep_res):
        user_prompt, buy_item = prep_res
        instruction = user_prompt
        prompt = f"现在，你想购买{buy_item}，你决定现在小红书上搜索有关的帖子，来帮助你决定是否真的需要购买。\n请你给出搜索词"
        response = call_llm(prompt = prompt, instruction = instruction)

        return response

    def post(self,shared,prep_res,exec_res):
        shared['USER_search_word_create_output'] = exec_res