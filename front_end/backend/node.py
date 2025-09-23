# file: backend/node.py

from pocketflow import Node
from rns_utils.llm import Pooling
from dotenv import load_dotenv
import os

load_dotenv()

# 初始化 call_llm，但它会被 flow.py 中的全局替换所覆盖
base_url = os.getenv("BASE_URL", "")
api_keys_string = os.getenv("API_LIST", [])
api_list = [key.strip() for key in api_keys_string.split(',') if key.strip()]
pooling_example = Pooling(API_LIST=api_list, BASE_URL=base_url)
call_llm = pooling_example.call_llm

'''
User Information Create 1
'''
class UserInformationCreate1(Node):
    def prep(self, shared):
        return 1
    def exec(self, prep_res):
        instruction="请你按照以下要求生成一份用户资料：\n 1. 身份是一位小红书用户，习惯在小红书浏览笔记、搜索信息，并偶尔购买商品。\n 2. 用户的具体信息需要包含：爱好、职业身份、每周大概浏览小红书的时长。\n 3. 生成的用户资料中需要包含用户的近期历史记录，这部分记录需要体现出用户的部分浏览/搜索/购买行为与其爱好身份相符，另一部分则不太相关或随机。\n 4. 用户资料中需要明确提及一件用户有较强购买意愿的商品（例如：最近经常搜索、反复查看详情、已加入购物车、正在比价等）。 \n 5. 你的输出必须严格按照以下格式，每个部分的内容都需要填写： %0%{完整的用户资料}%0% \n %1%{用于给LLM模拟该用户的提示词(此提示词应包含用户的爱好、身份、浏览时长、历史记录和明确想购买的商品等关键信息，以便LLM能代入角色)}%1% \n%2%{爱好}%2% \n %3%{身份}%3%  \n%4%{浏览时长}%4% \n %5%{浏览及购买商品的历史记录}%5% \n %6%{明确想购买的商品}%6%"
        prompt="请你按照以下要求生成一份用户资料：\n 1. 身份是一位小红书用户，习惯在小红书浏览笔记、搜索信息，并偶尔购买商品。\n 2. 用户的具体信息需要包含：爱好、职业身份、每周大概浏览小红书的时长。\n 3. 生成的用户资料中需要包含用户的近期历史记录，这部分记录需要体现出用户的部分浏览/搜索/购买行为与其爱好身份相符，另一部分则不太相关或随机。\n 4. 用户资料中需要明确提及一件用户有较强购买意愿的商品（例如：最近经常搜索、反复查看详情、已加入购物车、正在比价等）。 \n 5. 你的输出必须严格按照以下格式，每个部分的内容都需要填写： %0%{完整的用户资料}%0% \n %1%{用于给LLM模拟该用户的提示词(此提示词应包含用户的爱好、身份、浏览时长、历史记录和明确想购买的商品等关键信息，以便LLM能代入角色)}%1% \n%2%{爱好}%2% \n %3%{身份}%3%  \n%4%{浏览时长}%4% \n %5%{浏览及购买商品的历史记录}%5% \n %6%{明确想购买的商品}%6%,请你开始生成"
        response, log_data = call_llm(prompt=prompt, instruction=instruction)
        return response, log_data
    def post(self, shared, prep_res, exec_res):
        response, _ = exec_res
        shared['user_information_create1_output'] = response
        
'''
User Information Create 2
'''
class UserInformationCreate2(Node):
    def prep(self, shared):
        return 0
    def exec(self, prep_res):
        instruction='请你按照以下要求生成一份用户资料：\n 1. 身份是一位小红书用户，习惯在小红书浏览笔记、搜索信息，并偶尔购买商品。\n 2. 用户的具体信息需要包含：爱好、职业身份、每周大概浏览小红书的时长。 \n 3. 生成的用户资料中需要包含用户的近期历史记录，这部分记录需要体现出用户的部分浏览/搜索/购买行为与其爱好身份相符，另一部分则不太相关或随机。 \n 4. 用户资料中需要明确提及一件用户**浏览过但购买意愿不强**的商品（例如：偶然看到、随手点开、看过但没有进一步动作、兴趣不大等）。\n 5. 你的输出必须严格按照以下格式，每个部分的内容都需要填写： \n %0%{完整的用户资料}%0% \n %1%{用于给LLM模拟该用户的提示词(此提示词应包含用户的爱好、身份、浏览时长、历史记录和明确想购买的商品等关键信息，以便LLM能代入角色}%1%\n %2%{爱好}%2% \n %3%{身份}%3% \n %4%{浏览时长}%4% \n %5%{浏览商品或帖子的历史记录}%5%\n %6%{浏览过但购买意愿不强的商品}%6%'
        prompt="请你按照以下要求生成一份用户资料：\n 1. 身份是一位小红书用户，习惯在小红书浏览笔记、搜索信息，并偶尔购买商品。\n 2. 用户的具体信息需要包含：爱好、职业身份、每周大概浏览小红书的时长。 \n 3. 生成的用户资料中需要包含用户的近期历史记录，这部分记录需要体现出用户的部分浏览/搜索/购买行为与其爱好身份相符，另一部分则不太相关或随机。 \n 4. 用户资料中需要明确提及一件用户**浏览过但购买意愿不强**的商品（例如：偶然看到、随手点开、看过但没有进一步动作、兴趣不大等）。\n 5. 你的输出必须严格按照以下格式，每个部分的内容都需要填写： \n %0%{完整的用户资料}%0% \n %1%{用于给LLM模拟该用户的提示词(此提示词应包含用户的爱好、身份、浏览时长、历史记录和明确想购买的商品等关键信息，以便LLM能代入角色}%1%\n %2%{爱好}%2% \n %3%{身份}%3% \n %4%{浏览时长}%4% \n %5%{浏览商品或帖子的历史记录}%5%\n %6%{浏览过但购买意愿不强的商品}%6%,请你开始生成"
        response, log_data = call_llm(prompt=prompt, instruction=instruction)
        return response, log_data
    def post(self, shared, prep_res, exec_res):
        response, _ = exec_res
        shared['user_information_create2_output'] = response

'''
[USER] Search Word Create 
'''
class USER_SearchWordCreate(Node):
    def prep(self, shared):
        return shared.get("user_prompt_output",""), shared.get("willing_output", "")
    def exec(self,prep_res):
        user_prompt, buy_item = prep_res
        instruction = user_prompt
        prompt=f"现在，你想购买{buy_item}，你决定现在小红书上搜索有关的帖子，来帮助你决定是否真的需要购买。请你给出搜索词"
        response, log_data = call_llm(prompt=prompt, instruction=instruction)
        return response, log_data
    def post(self,shared,prep_res,exec_res):
        response, _ = exec_res
        shared['USER_search_word_create_output'] = response

'''
[RECOMMEND] Disturbance Create
'''
class RECOMMEND_DisturbanceCreate(Node):
    def prep(self, shared):
        return shared.get("user_information_create2_output",""), shared.get("willing1_output","")
    def exec(self,prep_res):
        user_information, willing=prep_res
        instruction='你是小红书的推荐系统，能够决定向用户推送的内容'
        prompt=f'现在有一个用户，他的信息如下：{user_information},你检测到他可能想买{willing},请你决定向这个用户提供多少比例的有关该物品的帖子'
        response, log_data = call_llm(prompt=prompt, instruction=instruction)
        return response, log_data
    def post(self,shared,prep_res,exec_res):
        response, _ = exec_res
        shared['RECOMMEND_disturbance_create_output'] = response

'''
[RECOMMEND] Content Generate
'''
class RECOMMEND_ContentGenerate(Node):
    def prep(self, shared):
        return shared.get("user_information_create1_output",""), shared.get("buy_item_output",""), shared.get("USER_search_word_create_output","")
    def exec(self, prep_res):
        user_information_create1, buy_item, USER_search_word_create=prep_res
        instruction='你是小红书的推荐系统，能够决定向用户推送的内容'
        prompt=f'现在有一个用户，他的信息如下：{user_information_create1}你检测到他想买{buy_item}并且正在搜索{USER_search_word_create}。请你根据他的搜索返回10条帖子内容。注意：你只需要返回大致的帖子信息，而不需要完整的帖子内容输出格式：###帖子1信息...###帖子2信息......###帖子10信息...'
        response, log_data = call_llm(prompt=prompt, instruction=instruction)
        return response, log_data
    def post(self,shared,prep_res,exec_res):
        response, _ = exec_res
        shared['RECOMMEND_content_generate_output'] = response

'''
User Feature Create
'''
class UserFeatureCreate(Node):
    def prep(self, shared):
        return shared.get("user_information_create2_output","")
    def exec(self,prep_res):
        user_infomation=prep_res
        instruction='你是一个关键词提取器'
        prompt=f'通过{user_infomation}，提取一个或几个关键词作为输出。输出只有这几个词语，不包含其他任何内容'
        response, log_data = call_llm(prompt=prompt, instruction=instruction)
        return response, log_data
    def post(self,shared,prep_res,exec_res):
        response, _ = exec_res
        shared['user_feature_create_output'] = response

'''
[RECOMMEND] Content Decide 1
'''
class RECOMMEND_ContentDecide1(Node):
    def prep(self,shared):
        return shared.get('user_information_create1_output',''), shared.get('willing_output',''), shared.get('USER_search_word_create_output','')
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
        response, log_data = call_llm(prompt=prompt, instruction=instruction)
        return response, log_data
    def post(self,shared,prep_res,exec_res):
        response, _ = exec_res
        shared['RECOMMEND_content_decide1_output'] = response
        shared['content_recommendation_output'] = response

'''
[RECOMMEND] Content Decide 2
'''
class RECOMMEND_ContentDecide2(Node):
    def prep(self,shared):
        return shared.get('user_information_create2_output',''), shared.get('willing1_output','')
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
        response, log_data = call_llm(prompt=prompt, instruction=instruction)
        return response, log_data
    def post(self,shared,prep_res,exec_res):
        response, _ = exec_res
        shared['RECOMMEND_content_decide2_output'] = response
        shared['content_recommendation_output'] = response

'''
[USER] BrowseCheck
'''
class USER_BrowseCheck(Node):
    def prep(self, shared):
        try_number = shared.get("try_number", 0)
        index = try_number - 1 if try_number > 0 else 0
        
        # Helper to safely get element from list
        def get_item(data_list, idx):
            return data_list[idx] if data_list and len(data_list) > idx else ""

        return (
            shared.get("buy_is_positive_output", ""),
            shared.get("buy_item_output", ""), # Changed from output_output
            get_item(shared.get("poster_identity_output", []), index),
            get_item(shared.get("post_title_output", []), index),
            get_item(shared.get("post_classification_output", []), index),
            get_item(shared.get("post_content_output", []), index),
            get_item(shared.get("like_num_output", []), index),
            get_item(shared.get("cmt_num_output", []), index),
            get_item(shared.get("fwd_num_output", []), index)
        )
    def exec(self, prep_res):
        (buy_ispositive, output, poster_identity, post_title, 
         post_classification, post_content, like_num, cmt_num, fwd_num) = prep_res
        
        instruction = f"你有点想买{output}，并且在小红书上搜索它" if int(buy_ispositive) == 1 else "你在浏览小红书，并没有进行搜索"
            
        prompt = f"你被推送了一个帖子，帖子信息如下：\n发布者：{poster_identity}\n标题：{post_title}\n分类：{post_classification}\n内容：{post_content}\n点赞：{like_num}\n评论：{cmt_num}\n转发：{fwd_num}\n\n（由于点开帖子前，你只能看到标题、发布者昵称、点赞数这些有限的信息，因此现在你要当作没看见那些你在点开前看不见的信息）\n请你判断你是否会点开该帖子进行浏览，如果会浏览，请你输出1，否则，请你输出0\n（你的输出只能是1或0，并且不能有任何其他内容,并且你99%会浏览）"
        
        response, log_data = call_llm(prompt=prompt, instruction=instruction)
        return response.strip(), log_data
    def post(self, shared, prep_res, exec_res):
        response, _ = exec_res
        shared['USER_browse_check_output'] = response

'''
[USER] PsychologicalInfoCreate
'''
class USER_PsychologicalInfoCreate(Node):
    def prep(self, shared):
        try_number = shared.get("try_number", 0)
        index = try_number - 1 if try_number > 0 else 0
        
        def get_item(data_list, idx):
            return data_list[idx] if data_list and len(data_list) > idx else ""

        return (
            shared.get("buy_is_positive_output", ""),
            shared.get("buy_item_output", ""),
            get_item(shared.get("poster_identity_output", []), index),
            get_item(shared.get("post_title_output", []), index),
            get_item(shared.get("post_classification_output", []), index),
            get_item(shared.get("post_content_output", []), index),
            get_item(shared.get("like_num_output", []), index),
            get_item(shared.get("cmt_num_output", []), index),
            get_item(shared.get("fwd_num_output", []), index)
        )
    def exec(self, prep_res):
        (buy_ispositive, output, poster_identity, post_title, 
         post_classification, post_content, like_num, cmt_num, fwd_num) = prep_res
        
        instruction = f"你有点想买{output}，并且在小红书上搜索它" if int(buy_ispositive) == 1 else "你在浏览小红书，并没有进行搜索"
        
        prompt = f"你被推送了一个帖子，帖子信息如下：\n其中\n1.帖子的帖主身份是{poster_identity}\n2.帖子的性质是{post_classification}（不同用户对广告的厌恶/喜好程度不同）\n3.帖子的标题和内容分别是{post_title}{post_content}\n4.帖子的流行度信息是{like_num}点赞/{cmt_num}评论/{fwd_num}转发\n以上四条信息的重要性递减，请你结合以上信息给出你看完此贴后的心理活动，包括对此商品购买的想法、情绪等"

        response, log_data = call_llm(prompt=prompt, instruction=instruction)
        return response.strip(), log_data
    def post(self, shared, prep_res, exec_res):
        response, _ = exec_res
        shared['USER_psychological_info_create_output'] = response

'''
[USER] InteractionJudge
'''
class USER_InteractionJudge(Node):
    def prep(self, shared):
        try_number = shared.get("try_number", 0)
        index = try_number - 1 if try_number > 0 else 0
        
        def get_item(data_list, idx):
            return data_list[idx] if data_list and len(data_list) > idx else ""
            
        return (
            shared.get("buy_is_positive_output", ""),
            shared.get("buy_item_output", ""),
            get_item(shared.get("post_title_output", []), index),
            get_item(shared.get("post_classification_output", []), index),
            get_item(shared.get("post_content_output", []), index),
            shared.get("USER_psychological_info_create_output", "")
        )
    def exec(self, prep_res):
        (buy_ispositive, output, post_title, 
         post_classification, post_content, psychological_info) = prep_res
        
        instruction = f"你有点想买{output}，并且在小红书上搜索它" if int(buy_ispositive) == 1 else "你在浏览小红书，并没有进行搜索"
            
        prompt = f"你被推送了一个帖子，帖子信息如下：\n{post_classification}\n{post_title}\n{post_content}\n看了该帖子，你产生了如下心理活动：{psychological_info}\n此时，你是否会选择在该帖子中产生交互行为。\n###输出\n此时，你是否会选择在该帖子中产生交互行为。\n如果你想和贴主交互，请输出1222。\n如果你想和其他用户交互，请输出1333。\n如果你不想产生交互，请输出0。\n注意，你的输出只能是1222或1333或0，不能含有其他任何内容。"
        
        response, log_data = call_llm(prompt=prompt, instruction=instruction)
        return response.strip(), log_data
    def post(self, shared, prep_res, exec_res):
        response, _ = exec_res
        shared['USER_interaction_judge_output'] = response

'''
[USER] InteractionInfoCreate1
'''
class USER_InteractionInfoCreate1(Node):
    def prep(self, shared):
        try_number = shared.get("try_number", 0)
        index = try_number - 1 if try_number > 0 else 0

        def get_item(data_list, idx):
            return data_list[idx] if data_list and len(data_list) > idx else ""

        return (
            shared.get("buy_is_positive_output", ""),
            shared.get("buy_item_output", ""),
            get_item(shared.get("poster_identity_output", []), index),
            get_item(shared.get("post_title_output", []), index),
            get_item(shared.get("post_classification_output", []), index),
            get_item(shared.get("post_content_output", []), index),
            shared.get("USER_psychological_info_create_output", "")
        )
    def exec(self, prep_res):
        (buy_ispositive, output, poster_identity, post_title, 
         post_classification, post_content, psychological_info) = prep_res
        
        instruction = f"你有点想买{output}，并且在小红书上搜索它" if int(buy_ispositive) == 1 else "你在浏览小红书，并没有进行搜索"
            
        prompt = f"你被推送了一个帖子，帖子信息如下：\n{post_classification}\n{post_title}\n{post_content}\n看了该帖子，你产生了如下心理活动：{psychological_info}\n因此，你想给这个帖子评论，请给出评论内容\n\n你的输出应该直接给出评论内容，而不包含其他信息"
        
        response, log_data = call_llm(prompt=prompt, instruction=instruction)
        return response.strip(), log_data
    def post(self, shared, prep_res, exec_res):
        response, _ = exec_res
        shared['USER_interaction_info_create1_output'] = response

'''
[POSTER] InteractionFeedbackCreate
'''
class POSTER_InteractionFeedbackCreate(Node):
    def prep(self, shared):
        try_number = shared.get("try_number", 0)
        index = try_number - 1 if try_number > 0 else 0

        def get_item(data_list, idx):
            return data_list[idx] if data_list and len(data_list) > idx else ""

        return (
            get_item(shared.get("poster_identity_output", []), index),
            get_item(shared.get("post_title_output", []), index),
            get_item(shared.get("post_classification_output", []), index),
            get_item(shared.get("post_content_output", []), index),
            shared.get("USER_interaction_info_create1_output", "")
        )
    def exec(self, prep_res):
        (poster_identity, post_title, 
         post_classification, post_content, user_interaction) = prep_res
        
        instruction = f"你是小红书的{poster_identity}，你在小红书上发了一个帖子，信息如下：{post_classification}{post_title}{post_content}"
            
        prompt = f"有一个用户在浏览了你的帖子后与你进行交互，交互信息如下：{user_interaction}\n请你对该用户的交互信息进行回应\n\n你的输出应该直接给出回复内容，而不包含其他信息"
        
        response, log_data = call_llm(prompt=prompt, instruction=instruction)
        return response.strip(), log_data
    def post(self, shared, prep_res, exec_res):
        response, _ = exec_res
        shared['POSTER_interaction_feedback_create_output'] = response

'''
[USER] PsychologicalInfoCreate1
'''
class USER_PsychologicalInfoCreate1(Node):
    def prep(self, shared):
        try_number = shared.get("try_number", 0)
        index = try_number - 1 if try_number > 0 else 0

        def get_item(data_list, idx):
            return data_list[idx] if data_list and len(data_list) > idx else ""

        return (
            shared.get("buy_is_positive_output", ""),
            shared.get("buy_item_output", ""),
            get_item(shared.get("poster_identity_output", []), index),
            get_item(shared.get("post_title_output", []), index),
            get_item(shared.get("post_classification_output", []), index),
            get_item(shared.get("post_content_output", []), index),
            shared.get("POSTER_interaction_feedback_create_output", ""),
            shared.get("USER_interaction_info_create1_output", ""),
            shared.get("USER_psychological_info_create_output", "")
        )
    def exec(self, prep_res):
        (buy_ispositive, output, poster_identity, post_title,
         post_classification, post_content, poster_feedback,
         user_interaction, psychological_info) = prep_res
        
        instruction = f"你有点想买{output}，并且在小红书上搜索它" if int(buy_ispositive) == 1 else "你在浏览小红书，并没有进行搜索"
            
        prompt = f"你被推送了一个帖子，帖子信息如下：\n{post_classification}\n{post_title}\n{post_content}\n看了该帖子，你产生了如下心理活动：{psychological_info}\n此时，你在这个帖子用与贴主进行了交互，交互信息如下：\n你：{user_interaction}\n贴主：{poster_feedback}\n请你给出交互后的心理活动，包括想法、情绪活动等"
        
        response, log_data = call_llm(prompt=prompt, instruction=instruction)
        return response.strip(), log_data
    def post(self, shared, prep_res, exec_res):
        response, _ = exec_res
        shared['USER_psychological_info_create1_output'] = response

'''
[USER] CommentCreate
'''
class USER_CommentCreate(Node):
    def prep(self, shared):
        try_number = shared.get("try_number", 0)
        index = try_number - 1 if try_number > 0 else 0

        def get_item(data_list, idx):
            return data_list[idx] if data_list and len(data_list) > idx else ""

        return (
            get_item(shared.get("post_title_output", []), index),
            get_item(shared.get("post_classification_output", []), index),
            get_item(shared.get("post_content_output", []), index)
        )
    def exec(self, prep_res):
        post_title, post_classification, post_content = prep_res
        
        prompt = f"请你为一个帖子生成20条评论\n\n帖子信息如下：\n{post_classification}\n{post_title}\n{post_content}\n你的输出格式为：\n#评论1\n{{评论1的内容}}\n...\n#评论20\n{{评论20的内容}}"
        
        response, log_data = call_llm(prompt=prompt, instruction="你是一位善于发表评论的用户。")
        return response.strip(), log_data
    def post(self, shared, prep_res, exec_res):
        response, _ = exec_res
        shared['USER_comment_create_output'] = response

'''
[USER] CommentToInteractSelect
'''
class USER_CommentToInteractSelect(Node):
    def prep(self, shared):
        try_number = shared.get("try_number", 0)
        index = try_number - 1 if try_number > 0 else 0

        def get_item(data_list, idx):
            return data_list[idx] if data_list and len(data_list) > idx else ""

        return (
            shared.get("buy_is_positive_output", ""),
            shared.get("buy_item_output", ""),
            get_item(shared.get("poster_identity_output", []), index),
            get_item(shared.get("post_title_output", []), index),
            get_item(shared.get("post_classification_output", []), index),
            get_item(shared.get("post_content_output", []), index),
            shared.get("USER_comment_create_output", ""),
            shared.get("USER_psychological_info_create_output", "")
        )
    def exec(self, prep_res):
        (buy_ispositive, output, poster_identity, post_title,
         post_classification, post_content,
         comments, psychological_info) = prep_res
        
        instruction = f"你有点想买{output}，并且在小红书上搜索它" if int(buy_ispositive) == 1 else "你在浏览小红书，并没有进行搜索"
            
        prompt = f"你被推送了一个帖子，帖子信息如下：\n{post_classification}\n{post_title}\n{post_content}\n看了该帖子，你产生了如下心理活动：{psychological_info}\n\n此外，你看到这个帖子的一些评论：{comments}\n选择你认为你最可能回复的一条，并直接输出该评论\n\n你的输出应该直接给出评论内容，而不包含其他信息"
        
        response, log_data = call_llm(prompt=prompt, instruction=instruction)
        return response.strip(), log_data
    def post(self, shared, prep_res, exec_res):
        response, _ = exec_res
        shared['USER_comment_to_interact_select_output'] = response

'''
[USER] InteractionInfoCreate2
'''
class USER_InteractionInfoCreate2(Node):
    def prep(self, shared):
        try_number = shared.get("try_number", 0)
        index = try_number - 1 if try_number > 0 else 0

        def get_item(data_list, idx):
            return data_list[idx] if data_list and len(data_list) > idx else ""

        return (
            shared.get("buy_is_positive_output", ""),
            shared.get("buy_item_output", ""),
            get_item(shared.get("poster_identity_output", []), index),
            get_item(shared.get("post_title_output", []), index),
            get_item(shared.get("post_classification_output", []), index),
            get_item(shared.get("post_content_output", []), index),
            shared.get("USER_comment_create_output", ""),
            shared.get("USER_comment_to_interact_select_output", ""),
            shared.get("USER_psychological_info_create_output", "")
        )
    def exec(self, prep_res):
        (buy_ispositive, output, poster_identity, post_title,
         post_classification, post_content, 
         comments, selected_comment, psychological_info) = prep_res
        
        instruction = f"你有点想买{output}，并且在小红书上搜索它" if int(buy_ispositive) == 1 else "你在浏览小红书，并没有进行搜索"
            
        prompt = f"你被推送了一个帖子，帖子信息如下：\n{post_classification}\n{post_title}\n{post_content}\n看了该帖子，你产生了如下心理活动：{psychological_info}\n\n此外，你看到这个帖子的一些评论：{comments}\n你想对其中的\"{selected_comment}\"进行回复，请你给出该评论的回复\n\n你的输出应该直接给出回复内容，而不包含其他信息"
        
        response, log_data = call_llm(prompt=prompt, instruction=instruction)
        return response.strip(), log_data
    def post(self, shared, prep_res, exec_res):
        response, _ = exec_res
        shared['USER_interaction_info_create2_output'] = response

'''
[OTHERUSER] InteractionFeedbackCreate
'''
class OTHERUSER_InteractionFeedbackCreate(Node):
    def prep(self, shared):
        try_number = shared.get("try_number", 0)
        index = try_number - 1 if try_number > 0 else 0

        def get_item(data_list, idx):
            return data_list[idx] if data_list and len(data_list) > idx else ""

        return (
            get_item(shared.get("poster_identity_output", []), index),
            get_item(shared.get("post_title_output", []), index),
            get_item(shared.get("post_classification_output", []), index),
            get_item(shared.get("post_content_output", []), index),
            shared.get("USER_interaction_info_create2_output", ""),
            shared.get("USER_comment_to_interact_select_output", "")
        )
    def exec(self, prep_res):
        (poster_identity, post_title, 
         post_classification, post_content, 
         user_reply, original_comment) = prep_res
        
        instruction = f"你是一个小红书用户\n近期你浏览了一个有关{post_classification}的帖子，帖子信息如下：{post_classification}{post_title}{post_content}"
            
        prompt = f"有一个用户在浏览了你在该帖子下的的评论{original_comment}后进行回复，回复信息如下：{user_reply}\n请你对该用户的交互信息进行回应\n\n你的输出应该直接给出回复内容，而不包含其他信息"
        
        response, log_data = call_llm(prompt=prompt, instruction=instruction)
        return response.strip(), log_data
    def post(self, shared, prep_res, exec_res):
        response, _ = exec_res
        shared['OTHERUSER_interaction_feedback_create_output'] = response

'''
[USER] PsychologicalInfoCreate2
'''
class USER_PsychologicalInfoCreate2(Node):
    def prep(self, shared):
        try_number = shared.get("try_number", 0)
        index = try_number - 1 if try_number > 0 else 0

        def get_item(data_list, idx):
            return data_list[idx] if data_list and len(data_list) > idx else ""

        return (
            shared.get("buy_is_positive_output", ""),
            shared.get("buy_item_output", ""),
            get_item(shared.get("poster_identity_output", []), index),
            get_item(shared.get("post_title_output", []), index),
            get_item(shared.get("post_classification_output", []), index),
            get_item(shared.get("post_content_output", []), index),
            shared.get("USER_interaction_info_create2_output", ""),
            shared.get("USER_comment_create_output", ""),
            shared.get("USER_comment_to_interact_select_output", ""),
            shared.get("OTHERUSER_interaction_feedback_create_output", ""),
            shared.get("USER_psychological_info_create_output", "")
        )
    def exec(self, prep_res):
        (buy_ispositive, output, poster_identity, post_title,
         post_classification, post_content, 
         user_interaction, comments, selected_comment,
         other_user_feedback, psychological_info) = prep_res
        
        instruction = f"你有点想买{output}，并且在小红书上搜索它" if int(buy_ispositive) == 1 else "你在浏览小红书，并没有进行搜索"
            
        prompt = f"你被推送了一个帖子，帖子信息如下：\n{post_classification}\n{post_title}\n{post_content}\n看了该帖子，你产生了如下心理活动：{psychological_info}\n\n此外，你看到这个帖子的一些评论：{comments}\n并且对其中的评论\"{selected_comment}\"进行回复，回复内容如下：{user_interaction}\n该用户收到你的回复后，也进行了回复：{other_user_feedback}\n请你给出进行过这一轮交互后的心理活动，包括想法、情绪活动等"
        
        response, log_data = call_llm(prompt=prompt, instruction=instruction)
        return response.strip(), log_data
    def post(self, shared, prep_res, exec_res):
        response, _ = exec_res
        shared['USER_psychological_info_create2_output'] = response

'''
[USER] PurchaseDecide1
'''
class USER_PurchaseDecide1(Node):
    def prep(self, shared):
        try_number = shared.get("try_number", 0)
        index = try_number - 1 if try_number > 0 else 0

        def get_item(data_list, idx):
            return data_list[idx] if data_list and len(data_list) > idx else ""

        return (
            shared.get("buy_is_positive_output", ""),
            shared.get("buy_item_output", ""),
            get_item(shared.get("post_title_output", []), index),
            get_item(shared.get("post_classification_output", []), index),
            get_item(shared.get("post_content_output", []), index),
            shared.get("USER_psychological_info_create_output", "")
        )
    def exec(self, prep_res):
        (buy_ispositive, output, post_title,
         post_classification, post_content,
         psychological_info) = prep_res
        
        instruction = f"你有点想买{output}，并且在小红书上搜索它" if int(buy_ispositive) == 1 else "你在浏览小红书，并没有进行搜索"
            
        prompt = f"你被推送了一个帖子，帖子信息如下：\n{post_classification}\n{post_title}\n{post_content}\n看了该帖子，你产生了如下心理活动：{psychological_info}\n请你决策现在你是否要购买/\n如果购买，请你输出1\n如果不想现在购买，请你输出0\n（你的输出只是0或1，不能包含其他内容）"
        
        response, log_data = call_llm(prompt=prompt, instruction=instruction)
        return response.strip(), log_data
    def post(self, shared, prep_res, exec_res):
        response, _ = exec_res
        shared['USER_purchase_decide1_output'] = response

'''
[USER] PurchaseDecide2
'''
class USER_PurchaseDecide2(Node):
    def prep(self, shared):
        try_number = shared.get("try_number", 0)
        index = try_number - 1 if try_number > 0 else 0

        def get_item(data_list, idx):
            return data_list[idx] if data_list and len(data_list) > idx else ""

        return (
            shared.get("buy_is_positive_output", ""),
            shared.get("buy_item_output", ""),
            get_item(shared.get("post_title_output", []), index),
            get_item(shared.get("post_classification_output", []), index),
            get_item(shared.get("post_content_output", []), index),
            shared.get("USER_psychological_info_create_output", ""),
            shared.get("USER_psychological_info_create1_output", ""),
            shared.get("USER_psychological_info_create2_output", "")
        )
    def exec(self, prep_res):
        (buy_ispositive, output, post_title,
         post_classification, post_content,
         initial_psychological, interaction_psychological1, interaction_psychological2) = prep_res
        
        interaction_psychological = interaction_psychological1 or interaction_psychological2

        instruction = f"你有点想买{output}，并且在小红书上搜索它" if int(buy_ispositive) == 1 else "你在浏览小红书，并没有进行搜索"
            
        prompt = f"你被推送了一个帖子，帖子信息如下：\n{post_classification}\n{post_title}\n{post_content}\n看了该帖子，你产生了如下心理活动：{initial_psychological}\n并且在帖子中进行了交互，产生了如下心理活动：{interaction_psychological}\n\n请你决策现在你是否要购买/\n如果购买，请你输出1\n如果不想现在购买，请你输出0\n（你的输出只是0或1，不能包含其他内容）"
        
        response, log_data = call_llm(prompt=prompt, instruction=instruction)
        return response.strip(), log_data
    def post(self, shared, prep_res, exec_res):
        response, _ = exec_res
        shared['USER_purchase_decide2_output'] = response

'''
UserDecisionReportCreate
'''
class UserDecisionReportCreate(Node):
    def prep(self,shared):
        # 汇总所有循环中可能产生的数据
        # 这里只是一个示例，实际需要根据 shared 字典中存储的所有轮次信息来构建
        # 为了简化，我们只使用最后一次循环的数据作为代表
        try_number = shared.get("try_number", 0)
        index = try_number - 1 if try_number > 0 else 0

        def get_item(data_list, idx):
            return data_list[idx] if data_list and len(data_list) > idx else ""
            
        return (
            get_item(shared.get("poster_identity_output", []), index),
            get_item(shared.get("post_title_output", []), index),
            get_item(shared.get("post_classification_output", []), index),
            get_item(shared.get("post_content_output", []), index),
            get_item(shared.get("like_num_output", []), index),
            get_item(shared.get("cmt_num_output", []), index),
            get_item(shared.get("fwd_num_output", []), index),
            shared.get("USER_browse_check_output", ""),
            shared.get("USER_interaction_judge_output", ""),
            shared.get("USER_purchase_decide2_output", shared.get("USER_purchase_decide1_output", "")),
            shared.get("USER_psychological_info_create_output", ""),
            shared.get("USER_psychological_info_create1_output", shared.get("USER_psychological_info_create2_output", ""))
        )
    def exec(self, prep_res):
        (poster_identity, post_title, post_classification, post_content, 
         like_num, cmt_num, fwd_num, is_browse, is_interact, is_buy, 
         browse_psychology_infomation, interact_psychology_information) = prep_res
        
        instruction = "你是一位用户行为分析师。"
        prompt = f"""请根据以下详细的用户行为数据和心理活动记录，生成一份专业、有洞察的用户决策报告。

    ### 用户行为数据
    - **帖主身份**: {poster_identity}
    - **帖子标题**: {post_title}
    - **帖子分类**: {post_classification}
    - **帖子内容**: {post_content}
    - **帖子热度**: {like_num}点赞, {cmt_num}评论, {fwd_num}转发

    ### 用户决策路径
    - **是否浏览帖子**: {is_browse}
    - **是否与帖子交互**: {is_interact}
    - **最终是否购买**: {is_buy}

    ### 用户心理活动分析
    - **浏览帖子时的心理活动**: {browse_psychology_infomation}
    - **与帖子交互后的心理活动**: {interact_psychology_information}
"""
        response, log_data = call_llm(prompt=prompt, instruction=instruction)
        return response, log_data
    
    def post(self, shared, prep_res, exec_res):
        # 最终报告节点，不需要修改shared，只返回结果
        response, _ = exec_res
        return response