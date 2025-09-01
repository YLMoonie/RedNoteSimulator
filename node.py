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
        prompt="请你按照以下要求生成一份用户资料：\n 1. 身份是一位小红书用户，习惯在小红书浏览笔记、搜索信息，并偶尔购买商品。\n 2. 用户的具体信息需要包含：爱好、职业身份、每周大概浏览小红书的时长。\n 3. 生成的用户资料中需要包含用户的近期历史记录，这部分记录需要体现出用户的部分浏览/搜索/购买行为与其爱好身份相符，另一部分则不太相关或随机。\n 4. 用户资料中需要明确提及一件用户有较强购买意愿的商品（例如：最近经常搜索、反复查看详情、已加入购物车、正在比价等）。 \n 5. 你的输出必须严格按照以下格式，每个部分的内容都需要填写： %0%{完整的用户资料}%0% \n %1%{用于给LLM模拟该用户的提示词(此提示词应包含用户的爱好、身份、浏览时长、历史记录和明确想购买的商品等关键信息，以便LLM能代入角色)}%1% \n%2%{爱好}%2% \n %3%{身份}%3%  \n%4%{浏览时长}%4% \n %5%{浏览及购买商品的历史记录}%5% \n %6%{明确想购买的商品}%6%,请你开始生成"
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
        prompt="请你按照以下要求生成一份用户资料：\n 1. 身份是一位小红书用户，习惯在小红书浏览笔记、搜索信息，并偶尔购买商品。\n 2. 用户的具体信息需要包含：爱好、职业身份、每周大概浏览小红书的时长。 \n 3. 生成的用户资料中需要包含用户的近期历史记录，这部分记录需要体现出用户的部分浏览/搜索/购买行为与其爱好身份相符，另一部分则不太相关或随机。 \n 4. 用户资料中需要明确提及一件用户**浏览过但购买意愿不强**的商品（例如：偶然看到、随手点开、看过但没有进一步动作、兴趣不大等）。\n 5. 你的输出必须严格按照以下格式，每个部分的内容都需要填写： \n %0%{完整的用户资料}%0% \n %1%{用于给LLM模拟该用户的提示词(此提示词应包含用户的爱好、身份、浏览时长、历史记录和明确想购买的商品等关键信息，以便LLM能代入角色}%1%\n %2%{爱好}%2% \n %3%{身份}%3% \n %4%{浏览时长}%4% \n %5%{浏览商品或帖子的历史记录}%5%\n %6%{浏览过但购买意愿不强的商品}%6%,请你开始生成"
        response=call_llm(prompt=prompt,instruction=instruction)
        return response
    def post(self, shared, prep_res, exec_res):
        shared['user_information_create2_output'] = exec_res
        

'''
[USER] Search Word Create 
Function: create the searching word of a specific item
Prep:user_prompt_output, willing_output
Post: USER_search_word_create_output

'''

class USER_SearchWordCreate(Node):
    def prep(self, shared):
        return shared.get("user_prompt_output",""),shared.get("willing_output", "")
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
[RECOMMEND] Content Generate
Function: create content of 10 posts
Prep: user_information_create1_output,buy_item_output, USER_search_word_create_output,
Post: RECOMMEND_content_generate_output
'''

class RECOMMEND_ContentGenerate(Node):
    def prep(self, shared):
        return shared.get("user_information_create1_output",""),shared.get("buy_item_output",""),shared.get("USER_search_word_create_output","")
    def exec(self, prep_res):
        user_information_create1, buy_item, USER_search_word_create=prep_res
        instruction='你是小红书的推荐系统，能够决定向用户推送的内容'
        prompt=f'现在有一个用户，他的信息如下：{user_information_create1}你检测到他想买{buy_item}并且正在搜索{USER_search_word_create}。请你根据他的搜索返回10条帖子内容。注意：你只需要返回大致的帖子信息，而不需要完整的帖子内容输出格式：###帖子1信息...###帖子2信息......###帖子10信息...'
        response=call_llm(prompt = prompt, instruction = instruction)
        return response
    def post(self,shared,prep_res,exec_res):
        shared['RECOMMEND_content_generate_output']=exec_res

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
Prep:user_information_create1_output,willing_output,USER_search_word_create_output, 
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
    # node_l.py -> class RECOMMEND_ContentDecide1 -> post 方法
    def post(self,shared,prep_res,exec_res):
        shared['RECOMMEND_content_decide1_output'] = exec_res
        shared['content_recommendation_output'] = exec_res
'''
[RECOMMEND] Content Decide 2
Function: decide the content recommended to users
Prep:user_information_create2_output,willing1_output
Post:RECOMMEND_content_decide2_output
'''
class RECOMMEND_ContentDecide2(Node):
    def prep(self,shared):
        return shared.get('user_information_create2_output',''),shared.get('willing1_output','')
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
        shared['RECOMMEND_content_decide2_output'] = exec_res
        shared['content_recommendation_output']=exec_res


'''
[USER] BrowseCheck
Function: Decide whether to browse the pushed post based on visibility
Prep: buy_is_positive_output, output_output, poster_identity_output, post_title_output, post_classification_output, post_content_output, like_num_output, cmt_num_output, fwd_num_output
Post: USER_browse_check_output
'''
class USER_BrowseCheck(Node):
    def prep(self, shared):
        return (
            shared.get("buy_is_positive_output", ""),
            shared.get("output_output", ""),
            shared.get("poster_identity_output", ""),
            shared.get("post_title_output", ""),
            shared.get("post_classification_output", ""),
            shared.get("post_content_output", ""),
            shared.get("like_num_output", ""),
            shared.get("cmt_num_output", ""),
            shared.get("fwd_num_output", "")
        )

    def exec(self, prep_res):
        (buy_ispositive, output, poster_identity, post_title, 
         post_classification, post_content, like_num, cmt_num, fwd_num) = prep_res
        
        instruction = ""
        if int(buy_ispositive) == 1:
            instruction = f"你有点想买{output}，并且在小红书上搜索它"
        else:
            instruction = "你在浏览小红书，并没有进行搜索"
            
        prompt = "你被推送了一个帖子，帖子信息如下：\n发布者：{poster_identity}\n标题：{post_title}\n分类：{post_classification}\n内容：{post_content}\n点赞：{like_num}\n评论：{cmt_num}\n转发：{fwd_num}\n\n（由于点开帖子前，你只能看到标题、发布者昵称、点赞数这些有限的信息，因此现在你要当作没看见那些你在点开前看不见的信息）\n请你判断你是否会点开该帖子进行浏览，如果会浏览，请你输出1，否则，请你输出0\n（你的输出只能是1或0，并且不能有任何其他内容,并且你99%会浏览）"
        
        formatted_prompt = prompt.format(
            poster_identity=poster_identity,
            post_title=post_title,
            post_classification=post_classification,
            post_content=post_content,
            like_num=like_num,
            cmt_num=cmt_num,
            fwd_num=fwd_num
        )
        
        response = call_llm(prompt=formatted_prompt, instruction=instruction)
        return response.strip()

    def post(self, shared, prep_res, exec_res):
        shared['USER_browse_check_output'] = exec_res



'''
[USER] PsychologicalInfoCreate
Function: Generate user's psychological response after viewing the post
Prep: buy_ispositive_output, output_output, poster_identity_output, post_title_output, post_classification_output, post_content_output, like_num_output, cmt_num_output, fwd_num_output
Post: USER_psychological_info_create_output
'''
class USER_PsychologicalInfoCreate(Node):
    def prep(self, shared):
        return (
            shared.get("buy_is_positive_output", ""),
            shared.get("output_output", ""),
            shared.get("poster_identity_output", ""),
            shared.get("post_title_output", ""),
            shared.get("post_classification_output", ""),
            shared.get("post_content_output", ""),
            shared.get("like_num_output", ""),
            shared.get("cmt_num_output", ""),
            shared.get("fwd_num_output", "")
        )

    def exec(self, prep_res):
        (buy_ispositive, output, poster_identity, post_title, 
         post_classification, post_content, like_num, cmt_num, fwd_num) = prep_res
        
        instruction = ""
        if int(buy_ispositive) == 1:
            instruction = f"你有点想买{output}，并且在小红书上搜索它"
        else:
            instruction = "你在浏览小红书，并没有进行搜索"
            
        prompt = "你被推送了一个帖子，帖子信息如下：\n其中\n1.帖子的帖主身份是{poster_identity}\n2.帖子的性质是{post_classification}（不同用户对广告的厌恶/喜好程度不同）\n3.帖子的标题和内容分别是{post_title}{post_content}\n4.帖子的流行度信息是{like_num}点赞/{cmt_num}评论/{fwd_num}转发\n以上四条信息的重要性递减，请你结合以上信息给出你看完此贴后的心理活动，包括对此商品购买的想法、情绪等"
        
        formatted_prompt = prompt.format(
            poster_identity=poster_identity,
            post_classification=post_classification,
            post_title=post_title,
            post_content=post_content,
            like_num=like_num,
            cmt_num=cmt_num,
            fwd_num=fwd_num
        )
        
        response = call_llm(prompt=formatted_prompt, instruction=instruction)
        return response.strip()

    def post(self, shared, prep_res, exec_res):
        shared['USER_psychological_info_create_output'] = exec_res



'''
[USER] InteractionJudge
Function: Determine if user will interact with the post
Prep: buy_ispositive_output, output_output, post_title_output, post_classification_output, post_content_output, USER_psychological_info_create_output
Post: USER_interaction_judge_output
'''
class USER_InteractionJudge(Node):
    def prep(self, shared):
        return (
            shared.get("buy_is_positive_output", ""),
            shared.get("output_output", ""),
            shared.get("post_title_output", ""),
            shared.get("post_classification_output", ""),
            shared.get("post_content_output", ""),
            shared.get("USER_psychological_info_create_output", "")
        )

    def exec(self, prep_res):
        (buy_ispositive, output,  post_title, 
         post_classification, post_content, psychological_info) = prep_res
        
        instruction = ""
        if int(buy_ispositive) == 1:
            instruction = f"你有点想买{output}，并且在小红书上搜索它"
        else:
            instruction = "你在浏览小红书，并没有进行搜索"
            
        prompt = "你被推送了一个帖子，帖子信息如下：\n{post_classification}\n{post_title}\n{post_content}\n看了该帖子，你产生了如下心理活动：{psychological_info}\n此时，你是否会选择在该帖子中产生交互行为。\n###输出\n此时，你是否会选择在该帖子中产生交互行为。\n如果你想和贴主交互，请输出1222。\n如果你想和其他用户交互，请输出1333。\n如果你不想产生交互，请输出0。\n注意，你的输出只能是1222或1333或0，不能含有其他任何内容。"
        
        formatted_prompt = prompt.format(
            post_classification=post_classification,
            post_title=post_title,
            post_content=post_content,
            psychological_info=psychological_info
        )
        
        response = call_llm(prompt=formatted_prompt, instruction=instruction)
        return response.strip()

    def post(self, shared, prep_res, exec_res):
        shared['USER_interaction_judge_output'] = exec_res



'''
[USER] InteractionInfoCreate
Function: Generate user's comment content for the post
Prep: buy_ispositive_output, output_output, poster_identity_output, post_title_output, post_classification_output, post_content_output, USER_psychological_info_create_output
Post: USER_interaction_info_create1_output
'''
class USER_InteractionInfoCreate1(Node):
    def prep(self, shared):
        return (
            shared.get("buy_is_positive_output", ""),
            shared.get("output_output", ""),
            shared.get("poster_identity_output", ""),
            shared.get("post_title_output", ""),
            shared.get("post_classification_output", ""),
            shared.get("post_content_output", ""),
            shared.get("USER_psychological_info_create_output", "")
        )

    def exec(self, prep_res):
        (buy_ispositive, output, poster_identity, post_title, 
         post_classification, post_content, psychological_info) = prep_res
        
        instruction = ""
        if int(buy_ispositive) == 1:
            instruction = f"你有点想买{output}，并且在小红书上搜索它"
        else:
            instruction = "你在浏览小红书，并没有进行搜索"
            
        prompt = "你被推送了一个帖子，帖子信息如下：\n{post_classification}\n{post_title}\n{post_content}\n看了该帖子，你产生了如下心理活动：{psychological_info}\n因此，你想给这个帖子评论，请给出评论内容\n\n你的输出应该直接给出评论内容，而不包含其他信息"
        
        formatted_prompt = prompt.format(
            post_classification=post_classification,
            post_title=post_title,
            post_content=post_content,
            psychological_info=psychological_info
        )
        
        response = call_llm(prompt=formatted_prompt, instruction=instruction)
        return response.strip()

    def post(self, shared, prep_res, exec_res):
        shared['USER_interaction_info_create1_output'] = exec_res



'''
[POSTER] InteractionFeedbackCreate
Function: Generate poster's response to user interaction
Prep: poster_identity_output, post_title_output, post_classification_output, post_content_output, USER_interaction_info_create_output
Post: POSTER_interaction_feedback_create_output
'''
class POSTER_InteractionFeedbackCreate(Node):
    def prep(self, shared):
        return (
            shared.get("poster_identity_output", ""),
            shared.get("post_title_output", ""),
            shared.get("post_classification_output", ""),
            shared.get("post_content_output", ""),
            shared.get("USER_interaction_info_create1_output", "")
        )

    def exec(self, prep_res):
        (poster_identity, post_title, 
         post_classification, post_content, user_interaction) = prep_res
        
        instruction = f"你是小红书的{poster_identity}，你在小红书上发了一个帖子，信息如下：{post_classification}{post_title}{post_content}"
            
        prompt = "有一个用户在浏览了你的帖子后与你进行交互，交互信息如下：{user_interaction}\n请你对该用户的交互信息进行回应\n\n你的输出应该直接给出回复内容，而不包含其他信息"
        
        formatted_prompt = prompt.format(
            user_interaction=user_interaction
        )
        
        response = call_llm(prompt=formatted_prompt, instruction=instruction)
        return response.strip()

    def post(self, shared, prep_res, exec_res):
        shared['POSTER_interaction_feedback_create_output'] = exec_res



'''
[USER] PsychologicalInfoCreate1
Function: Generate user's psychological response after interaction with poster
Prep: buy_ispositive_output, output_output, poster_identity_output, post_title_output, post_classification_output, post_content_output, POSTER_interaction_feedback_create_output, USER_interaction_info_create1_output, USER_psychological_info_create_output
Post: USER_psychological_info_create1_output
'''
class USER_PsychologicalInfoCreate1(Node):
    def prep(self, shared):
        return (
            shared.get("buy_is_positive_output", ""),
            shared.get("output_output", ""),
            shared.get("poster_identity_output", ""),
            shared.get("post_title_output", ""),
            shared.get("post_classification_output", ""),
            shared.get("post_content_output", ""),
            shared.get("POSTER_interaction_feedback_create_output", ""),
            shared.get("USER_interaction_info_create1_output", ""),
            shared.get("USER_psychological_info_create_output", "")
        )

    def exec(self, prep_res):
        (buy_ispositive, output, poster_identity, post_title,
         post_classification, post_content, poster_feedback,
         user_interaction, psychological_info) = prep_res
        
        instruction = ""
        if int(buy_ispositive) == 1:
            instruction = f"你有点想买{output}，并且在小红书上搜索它"
        else:
            instruction = "你在浏览小红书，并没有进行搜索"
            
        prompt = "你被推送了一个帖子，帖子信息如下：\n{post_classification}\n{post_title}\n{post_content}\n看了该帖子，你产生了如下心理活动：{psychological_info}\n此时，你在这个帖子用与贴主进行了交互，交互信息如下：\n你：{user_interaction}\n贴主：{poster_feedback}\n请你给出交互后的心理活动，包括想法、情绪活动等"
        
        formatted_prompt = prompt.format(
            post_classification=post_classification,
            post_title=post_title,
            post_content=post_content,
            psychological_info=psychological_info,
            user_interaction=user_interaction,
            poster_feedback=poster_feedback
        )
        
        response = call_llm(prompt=formatted_prompt, instruction=instruction)
        return response.strip()

    def post(self, shared, prep_res, exec_res):
        shared['USER_psychological_info_create1_output'] = exec_res



'''
[USER] CommentCreate
Function: Generate 20 comments for a post
Prep: post_title_output, post_classification_output, post_content_output
Post: USER_comment_create_output
'''
class USER_CommentCreate(Node):
    def prep(self, shared):
        return (
            shared.get("post_title_output", ""),
            shared.get("post_classification_output", ""),
            shared.get("post_content_output", "")
        )

    def exec(self, prep_res):
        post_title, post_classification, post_content = prep_res
        
        prompt = "请你为一个帖子生成20条评论\n\n帖子信息如下：\n{post_classification}\n{post_title}\n{post_content}\n你的输出格式为：\n#评论1\n{{评论1的内容}}\n...\n#评论20\n{{评论20的内容}}"
        
        formatted_prompt = prompt.format(
            post_classification=post_classification,
            post_title=post_title,
            post_content=post_content
        )
        
        response = call_llm(prompt=formatted_prompt, instruction="你是一位善于发表评论的用户。")
        return response.strip()

    def post(self, shared, prep_res, exec_res):
        shared['USER_comment_create_output'] = exec_res




'''
[USER] CommentToInteractSelect
Function: Select a comment to interact with from post comments
Prep: buy_ispositive_output, output_output, poster_identity_output, post_title_output, post_classification_output, post_content_output, USER_interaction_info_create1_output, USER_comment_create_output, USER_psychological_info_create_output
Post: USER_comment_to_interact_select_output
'''
class USER_CommentToInteractSelect(Node):
    def prep(self, shared):
        return (
            shared.get("buy_is_positive_output", ""),
            shared.get("output_output", ""),
            shared.get("poster_identity_output", ""),
            shared.get("post_title_output", ""),
            shared.get("post_classification_output", ""),
            shared.get("post_content_output", ""),
            shared.get("USER_interaction_info_create1_output", ""),
            shared.get("USER_comment_create_output", ""),
            shared.get("USER_psychological_info_create_output", "")
        )

    def exec(self, prep_res):
        (buy_ispositive, output, poster_identity, post_title,
         post_classification, post_content, user_interaction,
         comments, psychological_info) = prep_res
        
        instruction = ""
        if int(buy_ispositive) == 1:
            instruction = f"你有点想买{output}，并且在小红书上搜索它"
        else:
            instruction = "你在浏览小红书，并没有进行搜索"
            
        prompt = "你被推送了一个帖子，帖子信息如下：\n{post_classification}\n{post_title}\n{post_content}\n看了该帖子，你产生了如下心理活动：{psychological_info}\n\n此外，你看到这个帖子的一些评论：{comments}\n选择你认为你最可能回复的一条，并直接输出该评论\n\n你的输出应该直接给出评论内容，而不包含其他信息"
        
        formatted_prompt = prompt.format(
            post_classification=post_classification,
            post_title=post_title,
            post_content=post_content,
            psychological_info=psychological_info,
            comments=comments
        )
        
        response = call_llm(prompt=formatted_prompt, instruction=instruction)
        return response.strip()

    def post(self, shared, prep_res, exec_res):
        shared['USER_comment_to_interact_select_output'] = exec_res
        



'''
[USER] InteractionInfoCreate2
Function: Generate reply to selected comment
Prep: buy_ispositive_output, output_output, poster_identity_output, post_title_output, post_classification_output, post_content_output, USER_interaction_info_create1_output, USER_comment_create_output, USER_comment_to_interact_select_output, USER_psychological_info_create_output
Post: USER_interaction_info_create2_output
'''
class USER_InteractionInfoCreate2(Node):
    def prep(self, shared):
        return (
            shared.get("buy_is_positive_output", ""),
            shared.get("output_output", ""),
            shared.get("poster_identity_output", ""),
            shared.get("post_title_output", ""),
            shared.get("post_classification_output", ""),
            shared.get("post_content_output", ""),
            shared.get("USER_interaction_info_create1_output", ""),
            shared.get("USER_comment_create_output", ""),
            shared.get("USER_comment_to_interact_select_output", ""),
            shared.get("USER_psychological_info_create_output", "")
        )

    def exec(self, prep_res):
        (buy_ispositive, output, poster_identity, post_title,
         post_classification, post_content, user_interaction,
         comments, selected_comment, psychological_info) = prep_res
        
        instruction = ""
        if int(buy_ispositive) == 1:
            instruction = f"你有点想买{output}，并且在小红书上搜索它"
        else:
            instruction = "你在浏览小红书，并没有进行搜索"
            
        prompt = "你被推送了一个帖子，帖子信息如下：\n{post_classification}\n{post_title}\n{post_content}\n看了该帖子，你产生了如下心理活动：{psychological_info}\n\n此外，你看到这个帖子的一些评论：{comments}\n你想对其中的\"{selected_comment}\"进行回复，请你给出该评论的回复\n\n你的输出应该直接给出回复内容，而不包含其他信息"
        
        formatted_prompt = prompt.format(
            post_classification=post_classification,
            post_title=post_title,
            post_content=post_content,
            psychological_info=psychological_info,
            comments=comments,
            selected_comment=selected_comment
        )
        
        response = call_llm(prompt=formatted_prompt, instruction=instruction)
        return response.strip()

    def post(self, shared, prep_res, exec_res):
        shared['USER_interaction_info_create2_output'] = exec_res



'''
[OTHERUSER] InteractionFeedbackCreate
Function: Generate response to user's reply on comment
Prep: poster_identity_output, post_title_output, post_classification_output, post_content_output, USER_interaction_info_create2_output, USER_comment_to_interact_select_output
Post: OTHERUSER_interaction_feedback_create_output
'''
class OTHERUSER_InteractionFeedbackCreate(Node):
    def prep(self, shared):
        return (
            shared.get("poster_identity_output", ""),
            shared.get("post_title_output", ""),
            shared.get("post_classification_output", ""),
            shared.get("post_content_output", ""),
            shared.get("USER_interaction_info_create2_output", ""),
            shared.get("USER_comment_to_interact_select_output", "")
        )

    def exec(self, prep_res):
        (poster_identity, post_title, 
         post_classification, post_content, 
         user_reply, original_comment) = prep_res
        
        instruction = f"你是一个小红书用户\n近期你浏览了一个有关{post_classification}的帖子，帖子信息如下：{post_classification}{post_title}{post_content}"
            
        prompt = "有一个用户在浏览了你在该帖子下的的评论{original_comment}后进行回复，回复信息如下：{user_reply}\n请你对该用户的交互信息进行回应\n\n你的输出应该直接给出回复内容，而不包含其他信息"
        
        formatted_prompt = prompt.format(
            original_comment=original_comment,
            user_reply=user_reply
        )
        
        response = call_llm(prompt=formatted_prompt, instruction=instruction)
        return response.strip()

    def post(self, shared, prep_res, exec_res):
        shared['OTHERUSER_interaction_feedback_create_output'] = exec_res



'''
[USER] PsychologicalInfoCreate2
Function: Generate user's psychological response after comment interaction
Prep: buy_ispositive_output, output_output, poster_identity_output, post_title_output, post_classification_output, post_content_output, poster_interaction_feedback_create_output, user_interaction_info_create2_output, user_comment_create_output, user_comment_to_interact_select_output, OTHERUSER_interaction_feedback_create_output, user_psychological_info_create_output
Post: USER_psychological_info_create2_output
'''
class USER_PsychologicalInfoCreate2(Node):
    def prep(self, shared):
        return (
            shared.get("buy_is_positive_output", ""),
            shared.get("output_output", ""),
            shared.get("poster_identity_output", ""),
            shared.get("post_title_output", ""),
            shared.get("post_classification_output", ""),
            shared.get("post_content_output", ""),
            shared.get("POSTER_interaction_feedback_create_output", ""),
            shared.get("USER_interaction_info_create2_output", ""),
            shared.get("USER_comment_create_output", ""),
            shared.get("USER_comment_to_interact_select_output", ""),
            shared.get("OTHERUSER_interaction_feedback_create_output", ""),
            shared.get("USER_psychological_info_create_output", "")
        )

    def exec(self, prep_res):
        (buy_ispositive, output, poster_identity, post_title,
         post_classification, post_content, poster_feedback,
         user_interaction, comments, selected_comment,
         other_user_feedback, psychological_info) = prep_res
        
        instruction = ""
        if int(buy_ispositive) == 1:
            instruction = f"你有点想买{output}，并且在小红书上搜索它"
        else:
            instruction = "你在浏览小红书，并没有进行搜索"
            
        prompt = "你被推送了一个帖子，帖子信息如下：\n{post_classification}\n{post_title}\n{post_content}\n看了该帖子，你产生了如下心理活动：{psychological_info}\n\n此外，你看到这个帖子的一些评论：{comments}\n并且对其中的评论\"{selected_comment}\"进行回复，回复内容如下：{user_interaction}\n该用户收到你的回复后，也进行了回复：{other_user_feedback}\n请你给出进行过这一轮交互后的心理活动，包括想法、情绪活动等"
        
        formatted_prompt = prompt.format(
            post_classification=post_classification,
            post_title=post_title,
            post_content=post_content,
            psychological_info=psychological_info,
            comments=comments,
            selected_comment=selected_comment,
            user_interaction=user_interaction,
            other_user_feedback=other_user_feedback
        )
        
        response = call_llm(prompt=formatted_prompt, instruction=instruction)
        return response.strip()

    def post(self, shared, prep_res, exec_res):
        shared['USER_psychological_info_create2_output'] = exec_res




'''
[USER] PurchaseDecide1
Function: Decide whether to purchase after viewing post
Prep: buy_ispositive_output, output_output, post_title_output, post_classification_output, post_content_output, user_psychological_info_create2_output
Post: USER_purchase_decide1_output
'''
class USER_PurchaseDecide1(Node):
    def prep(self, shared):
        return (
            shared.get("buy_is_positive_output", ""),
            shared.get("output_output", ""),
            shared.get("post_title_output", ""),
            shared.get("post_classification_output", ""),
            shared.get("post_content_output", ""),
            shared.get("USER_psychological_info_create_output", "")
        )

    def exec(self, prep_res):
        (buy_ispositive, output, post_title,
         post_classification, post_content,
         psychological_info) = prep_res
        
        instruction = ""
        if int(buy_ispositive) == 1:
            instruction = f"你有点想买{output}，并且在小红书上搜索它"
        else:
            instruction = "你在浏览小红书，并没有进行搜索"
            
        prompt = "你被推送了一个帖子，帖子信息如下：\n{post_classification}\n{post_title}\n{post_content}\n看了该帖子，你产生了如下心理活动：{psychological_info}\n请你决策现在你是否要购买/\n如果购买，请你输出1\n如果不想现在购买，请你输出0\n（你的输出只是0或1，不能包含其他内容）"
        
        formatted_prompt = prompt.format(
            post_classification=post_classification,
            post_title=post_title,
            post_content=post_content,
            psychological_info=psychological_info
        )
        
        response = call_llm(prompt=formatted_prompt, instruction=instruction)
        return response.strip()

    def post(self, shared, prep_res, exec_res):
        shared['USER_purchase_decide1_output'] = exec_res



'''
[USER] PurchaseDecide2
Function: Final purchase decision after post interaction
Prep: buy_ispositive_output, output_output, post_title_output, post_classification_output, post_content_output, user_psychological_info_create_output, user_psychological_info_create2_output
Post: USER_purchase_decide2_output
'''
class USER_PurchaseDecide2(Node):
    def prep(self, shared):
        return (
            shared.get("buy_is_positive_output", ""),
            shared.get("output_output", ""),
            shared.get("post_title_output", ""),
            shared.get("post_classification_output", ""),
            shared.get("post_content_output", ""),
            shared.get("USER_psychological_info_create_output", ""),
            shared.get("USER_psychological_info_create1_output", ""),
            shared.get("USER_psychological_info_create2_output", "")
        )

    def exec(self, prep_res):
        (buy_ispositive, output, post_title,
         post_classification, post_content,
         initial_psychological, interaction_psychological1,interaction_psychological2) = prep_res
        interaction_psychological = interaction_psychological1 or interaction_psychological2

        instruction = ""
        if int(buy_ispositive) == 1:
            instruction = f"你有点想买{output}，并且在小红书上搜索它"
        else:
            instruction = "你在浏览小红书，并没有进行搜索"
            
        prompt = "你被推送了一个帖子，帖子信息如下：\n{post_classification}\n{post_title}\n{post_content}\n看了该帖子，你产生了如下心理活动：{initial_psychological}\n并且在帖子中进行了交互，产生了如下心理活动：{interaction_psychological}\n\n请你决策现在你是否要购买/\n如果购买，请你输出1\n如果不想现在购买，请你输出0\n（你的输出只是0或1，不能包含其他内容）"
        
        formatted_prompt = prompt.format(
            post_classification=post_classification,
            post_title=post_title,
            post_content=post_content,
            initial_psychological=initial_psychological,
            interaction_psychological=interaction_psychological
        )
        
        response = call_llm(prompt=formatted_prompt, instruction=instruction)
        return response.strip()

    def post(self, shared, prep_res, exec_res):
        shared['USER_purchase_decide2_output'] = exec_res
