from pocketflow import Node, Flow
from rns_utils.llm import Pooling
from dotenv import load_dotenv
from rns_utils.ToolNode import CodeExecute
import openai
import os
import re
import warnings

'''
Parameter Extractor 1:
Function: extract parameter from user_information_create1
Prep:user_information_create1_output
Post:user_profile_output
user_prompt_output 
user_hobby_output 
user_identity_output 
broswer_time_output 
buy_item_output 
willing_output 
'''

code_parameter_extractor1 = """
import re
input_text = shared['user_information_create1_output']

def extract_with_regex(text, tag_number):
    pattern = f'%{tag_number}%(.*?)%{tag_number}%'
    match = re.search(pattern, text, re.DOTALL)
    
    if match:
        return match.group(1).strip()
    return ""

shared['user_profile_output'] = extract_with_regex(input_text, '0')
shared['user_prompt_output'] = extract_with_regex(input_text, '1')
shared['user_hobby_output'] = extract_with_regex(input_text, '2')
shared['user_identity_output'] = extract_with_regex(input_text, '3')
shared['broswer_time_output'] = extract_with_regex(input_text, '4') 
shared['buy_item_output'] = extract_with_regex(input_text, '5')
shared['willing_output'] = extract_with_regex(input_text, '6')
"""
execution_results = CodeExcute(code_parameter_extractor1,'shared')


'''
Parameter Extractor 2:
Function: extract parameter from user_information_create1
Prep:user_information_create2_output
Post:user_profile_output
user_prompt_output 
user_hobby_output 
user_identity_output 
broswer_time_output 
buy_item_output 
willing1_output 
'''


code_parameter_extractor2 = """
import re
input_text = shared['user_information_create2_output']

def extract_with_regex(text, tag_number):
    pattern = f'%{tag_number}%(.*?)%{tag_number}%'
    match = re.search(pattern, text, re.DOTALL)
    
    if match:
        return match.group(1).strip()
    return ""

shared['user_profile_output'] = extract_with_regex(input_text, '0')
shared['user_prompt_output'] = extract_with_regex(input_text, '1')
shared['user_hobby_output'] = extract_with_regex(input_text, '2')
shared['user_identity_output'] = extract_with_regex(input_text, '3')
shared['broswer_time_output'] = extract_with_regex(input_text, '4') 
shared['buy_item_output'] = extract_with_regex(input_text, '5')
shared['willing1_output'] = extract_with_regex(input_text, '6')
"""
execution_results = CodeExcute(code_parameter_extractor2,'shared')


'''
Post Info 
Function: extract features of post
Prep: branch_to_aggregation_output
Post: poster_identity_output, post_title_output, post_classification_output, post_content_output, like_num_output
cmt_num_output,fwd_num_output
'''
code_post_info = """
import re

input_text = branch_to_aggregation_output

SECTION_MAP = {
    '帖主身份': 'poster_identity_output',
    '帖子标题': 'post_title_output',
    '帖子性质': 'post_classification_output',
    '帖子内容': 'post_content_output',
    '点赞数': ' like_num_output',
    '评论数': 'cmt_num_output',
    '转发数':'fwd_num_output'
}


def extract_section(text, section_marker):
    pattern = re.compile(f'{re.escape(section_marker)}(.*?)(?=%%%|$)', re.DOTALL)
    match = pattern.search(text)
    if match:
        return match.group(1).strip()
    return ""

def parse_section_to_list(section_text):
    if not section_text:
        return []
    items = re.findall(r'{(.*?)}', section_text, re.DOTALL)
    return [item.strip() for item in items]

for chinese_name, english_key in SECTION_MAP.items():
    full_marker = f'%%%{chinese_name}'
    section_content = extract_section(input_text, full_marker)
    item_list = parse_section_to_list(section_content)
    shared[english_key] = item_list
"""

execution_results = CodeExcute(code_post_info,'shared')



