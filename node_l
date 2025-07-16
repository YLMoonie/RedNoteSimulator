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
User Information Create 1
Function: Simulate user information(hobby\ identity\searching record\item wanted to buy)
Prep: 1
Post: user_information_create1_output

'''

class UserInformationCreate1(Node):
    def prep(self, shared):
        return 1
    def exec(self, prep_res):
        instruction="请你按照以下要求生成一份用户资料：\n 1. 身份是一位小红书用户，习惯在小红书浏览笔记、搜索信息，并偶尔购买商品。\n 2. 用户的具体信息需要包含：爱好、职业身份、每周大概浏览小红书的时长。\n 3. 生成的用户资料中需要包含用户的近期历史记录，这部分记录需要体现出用户的部分浏览/搜索/购买行为与其爱好身份相符，另一部分则不太相关或随机。\n 4. 用户资料中需要明确提及一件用户有较强购买意愿的商品（例如：最近经常搜索、反复查看详情、已加入购物车、正在比价等）。 \n 5. 你的输出必须严格按照以下格式，每个部分的内容都需要填写： %0%{完整的用户资料}%0% \n %1%{用于给LLM模拟该用户的提示词(此提示词应包含用户的爱好、身份、浏览时长、历史记录和明确想购买的商品等关键信息，以便LLM能代入角色)}%1% \n%2%{爱好}%2% \n %3%{身份}%3%  \n%4%{浏览时长}%4% \n %5%{浏览及购买商品的历史记录}%5% \n %6%{明确想购买的商品}%6%"
        prompt="请你开始生成"
        response=call_llm(prompt=prompt,instruction=instruction)
        return response
    def post(self, shared, prep_res, exec_res):
        shared['user_information_create1_output'] = exec_res

'''
User Information Create 2
Function: Simulate user information(hobby\ identity\searching record\item searched)
Prep: 0
Post: user_information_create2_output
'''
class UserInformationCreate2(Node):
    def prep(self, shared):
        return 0
    def exec(self, prep_res):
        instruction='请你按照以下要求生成一份用户资料：\n 1. 身份是一位小红书用户，习惯在小红书浏览笔记、搜索信息，并偶尔购买商品。\n 2. 用户的具体信息需要包含：爱好、职业身份、每周大概浏览小红书的时长。 \n 3. 生成的用户资料中需要包含用户的近期历史记录，这部分记录需要体现出用户的部分浏览/搜索/购买行为与其爱好身份相符，另一部分则不太相关或随机。 \n 4. 用户资料中需要明确提及一件用户**浏览过但购买意愿不强**的商品（例如：偶然看到、随手点开、看过但没有进一步动作、兴趣不大等）。\n 5. 你的输出必须严格按照以下格式，每个部分的内容都需要填写： \n %0%{完整的用户资料}%0% \n %1%{用于给LLM模拟该用户的提示词(此提示词应包含用户的爱好、身份、浏览时长、历史记录和明确想购买的商品等关键信息，以便LLM能代入角色}%1%\n %2%{爱好}%2% \n %3%{身份}%3% \n %4%{浏览时长}%4% \n %5%{浏览商品或帖子的历史记录}%5%\n %6%{浏览过但购买意愿不强的商品}%6%'
        prompt="请你开始生成"
        response=call_llm(prompt=prompt,instruction=instruction)
        return response
    def post(self, shared, prep_res, exec_res):
        shared['user_information_create2_output'] = exec_res

'''
[USER] Search Word Create 
Function: create the searching word of a specific item
Prep:user_prompt_output, buy_item_output
Post: USER_search_word_create_output

'''

class USER_SearchWordCreate(Node):
    def prep(self, shared):
        return shared.get("user_prompt_output",""),shared.get("buy_item_output", "")
    def exec(self,prep_res):
        user_prompt, buy_item = prep_res
        instruction = user_prompt
        prompt=f"现在，你想购买{buy_item}，你决定现在小红书上搜索有关的帖子，来帮助你决定是否真的需要购买。请你给出搜索词"
        response=response = call_llm(prompt = prompt, instruction = instruction)

        return response
    def post(self,shared,prep_res,exec_res):
        shared['USER_search_word_create_output'] = exec_res

'''
[RECOMMEND] Disturbance Create
Function: create articles about items might be bought
Prep:user_information_create2_output, willing1_output
Post:RECOMMEND_disturbance_create_output
'''
class RECOMMEND_DisturbanceCreate(Node):
    def prep(self, shared):
        return shared.get("user_information_create2_output",""),shared.get("willing1_output","")
    def exec(self,prep_res):
        user_information, willing=prep_res
        instruction='你是小红书的推荐系统，能够决定向用户推送的内容'
        prompt=f'现在有一个用户，他的信息如下：{user_information},你检测到他可能想买{willing},请你决定向这个用户提供多少比例的有关该物品的帖子'
        response = call_llm(prompt = prompt, instruction = instruction)

        return response
    def post(self,shared,prep_res,exec_res):
        shared['RECOMMEND_disturbance_create_output']=exec_res

'''
User Feature Create
Function: create key word 
Prep: user_information_create2_output
Post: user_feature_create_output
'''
class UserFeatureCreate(Node):
    def prep(self, shared):
        return shared.get("user_information_create2_output","")
    def exec(self,prep_res):
        user_infomation=prep_res
        instruction='你是一个关键词提取器'
        prompt=f'通过{user_infomation}，提取一个或几个关键词作为输出。输出只有这几个词语，不包含其他任何内容'
        response = call_llm(prompt = prompt, instruction = instruction)

        return response

    def post(self,shared,prep_res,exec_res):
        shared['user_feature_create_output'] = exec_res

'''
[RECOMMEND] Content Decide 1
Function: decide the content recommended to users
Prep:user_information_create1_output,willing_output,USER_search_word_create_output
Post:RECOMMEND_content_decide1_output
'''
class RECOMMEND_ContentDecide1(Node):
    def prep(self,shared):
        return shared.get('user_information_create1_output',''),shared.get('willing_output',''),shared.get('USER_search_word_create_output','')
    def exec(self, prep_res):
        user_information, willing, USER_search_word_create=prep_res
        instruction='你是小红书的推荐系统，能够决定向用户推送的内容.'
        prompt=f'''现在有一个用户，他的信息如下：{user_information}。他想买{willing}。现在，用户搜索了{USER_search_word_create}，你需要输出10条帖子。帖子信息并不完全，你需要根据帖子已知信息来补充：
        1.帖主的身份（只能是 KOL、KOC、普通用户、入驻商家 中的一个）\n 2.帖子性质，必须严格遵循：\n KOL→广告|软广\n KOC→广告|软广|真实体验\n用户→真实体验 \n入驻商家→广告|软广
        \n
        根据输出格式如下内容：
        %%%帖主身份
        ###第1个帖子的帖主身份
        ...
        ###第10帖子的帖主身份

        %%%帖子标题
        ###第1个帖子的帖子标题

        ...
        ###第10帖子的帖子标题

        %%%帖子性质
        ###第1个帖子的帖子性质
        ...
        ###第10帖子的帖子性质

        %%%帖子内容
        ###第1个帖子的帖子内容
        ...
        ###第10帖子的帖子内容

        %%%点赞数
        ###第1个帖子的点赞数
        ...
        ###第10帖子的点赞数

        %%%评论数
        ###第1个帖子的评论数
        ...
        ###第10帖子的评论数

        %%%转发量
        ###第1个帖子的转发量
        ...
        ###第10帖子的转发量
        '''
        response = call_llm(prompt = prompt, instruction = instruction)

        return response
    def post(self,shared,prep_res,exec_res):
        shared['RECOMMEND_content_decide1_output'] = exec_res
'''
[RECOMMEND] Content Decide 2
Function: decide the content recommended to users
Prep:user_information_create2_output,willing1_output
Post:RECOMMEND_content_decide1_output
'''
class RECOMMEND_ContentDecide2(Node):
    def prep(self,shared):
        return shared.get('user_information_create2_output',''),shared.get('willing_output','')
    def exec(self, prep_res):
        user_information, willing=prep_res
        instruction='你是小红书的推荐系统，能够决定向用户推送的内容.'
        prompt=f'''现在有一个用户，他的信息如下：{user_information}。你检测到他想买{willing}。你需要输出10条帖子。帖子信息并不完全，你需要根据帖子已知信息来补充：
        1.帖主的身份（只能是 KOL、KOC、普通用户、入驻商家 中的一个）\n 2.帖子性质，必须严格遵循：\n KOL→广告|软广\n KOC→广告|软广|真实体验\n用户→真实体验 \n入驻商家→广告|软广
        \n
        根据输出格式如下内容：
        %%%帖主身份
        ###第1个帖子的帖主身份
        ...
        ###第10帖子的帖主身份

        %%%帖子标题
        ###第1个帖子的帖子标题

        ...
        ###第10帖子的帖子标题

        %%%帖子性质
        ###第1个帖子的帖子性质
        ...
        ###第10帖子的帖子性质

        %%%帖子内容
        ###第1个帖子的帖子内容
        ...
        ###第10帖子的帖子内容

        %%%点赞数
        ###第1个帖子的点赞数
        ...
        ###第10帖子的点赞数

        %%%评论数
        ###第1个帖子的评论数
        ...
        ###第10帖子的评论数

        %%%转发量
        ###第1个帖子的转发量
        ...
        ###第10帖子的转发量
        '''

        response = call_llm(prompt = prompt, instruction = instruction)

        return response
    def post(self,shared,prep_res,exec_res):
        shared['RECOMMEND_content_decide1_output'] = exec_res

'''
User Decision Report Create
Function:create a analysis report about user's purchasing decision
Prep:post_info_output,PsychologicalBuyInfo_output,poster_identity_output,post_title_output
     post_classification_output,post_content_output,like_num_output,cmt_num_output,fwd_num_output,is_browse_output
     is_interact_output,is_buy_output,browse_psychology_infomation_output,interact_psychology_information_output
Post:user_decision_report_create_output
'''
class UserDecisionReportCreate(Node):
    def prep(self,shared):
        return shared.get("post_info_output",""),shared.get("poster_identity_output",""),shared.get("post_title_output",""),shared.get("post_classification_output",""),shared.get("post_content_output",""),shared.get("like_num_output",""),shared.get("cmt_num_output",""),shared.get("fwd_num_output",""),shared.get("is_browse_output",""),shared.get("is_interact_output",""),shared.get("is_buy_output",""),shared.get("browse_psychology_infomation_output",""),shared.get("interact_psychology_information","")

    def exec(self, prep_res):
        post_info,poster_identity,post_title,post_classification,post_content,like_num,cmt_num,fwd_num,is_browse,is_interact,is_buy,browse_psychology_infomation,interact_psychology_information =prep_res
        instruction=f'''用户在浏览小红书时浏览了这些帖子{post_info},根据帖子做了些是否购买该产品的决策，具体内容如下。基于以下内容生成一份用户决策报告。
        {post_info},{poster_identity},{post_title},{post_classification},{post_content},{like_num},{cmt_num},{fwd_num},
        是否浏览：{is_browse}\n 是否交互：{is_interact}\n 是否购买：{is_buy}\n浏览时的心理信息：{browse_psychology_infomation}\n
        帖子中交互产生的心理信息：{interact_psychology_information}
        '''
        prompt=""
        response = call_llm(prompt=formatted_prompt, instruction=instruction)
        return response

    def post(self, shared, prep_res, exec_res):
        shared['user_decision_report_create_output'] = exec_res
    