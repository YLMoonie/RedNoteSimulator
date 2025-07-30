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




'''
[USER] BrowseCheck
Function: Decide whether to browse the pushed post based on visibility
Prep: buy_ispositive_output, output_output, poster_identity_output, post_title_output, post_classification_output, post_content_output, like_num_output, cmt_num_output, fwd_num_output
Post: USER_browse_check_output
'''
class USER_BrowseCheck(Node):
    def prep(self, shared):
        return (
            shared.get("buy_ispositive_output", ""),
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
            
        prompt = "你被推送了一个帖子，帖子信息如下：\n发布者：{poster_identity}\n标题：{post_title}\n分类：{post_classification}\n内容：{post_content}\n点赞：{like_num}\n评论：{cmt_num}\n转发：{fwd_num}\n\n（由于点开帖子前，你只能看到标题、发布者昵称、点赞数这些有限的信息，因此现在你要当作没看见那些你在点开前看不见的信息）\n请你判断你是否会点开该帖子进行浏览，如果会浏览，请你输出1，否则，请你输出0\n（你的输出只能是1或0，并且不能有任何其他内容）"
        
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
            shared.get("buy_ispositive_output", ""),
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
            shared.get("buy_ispositive_output", ""),
            shared.get("output_output", ""),
            shared.get("post_title_output", ""),
            shared.get("post_classification_output", ""),
            shared.get("post_content_output", ""),
            shared.get("USER_psychological_info_create_output", "")
        )

    def exec(self, prep_res):
        (buy_ispositive, output, poster_identity, post_title, 
         post_classification, post_content, like_num, cmt_num, 
         fwd_num, psychological_info) = prep_res
        
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
Post: USER_interaction_info_create_output
'''
class USER_InteractionInfoCreate(Node):
    def prep(self, shared):
        return (
            shared.get("buy_ispositive_output", ""),
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
        shared['USER_interaction_info_create_output'] = exec_res



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
            shared.get("USER_interaction_info_create_output", "")
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
Prep: buy_ispositive_output, output_output, poster_identity_output, post_title_output, post_classification_output, post_content_output, POSTER_interaction_feedback_create_output, USER_interaction_info_create_output, USER_psychological_info_create_output
Post: USER_psychological_info_create1_output
'''
class USER_PsychologicalInfoCreate1(Node):
    def prep(self, shared):
        return (
            shared.get("buy_ispositive_output", ""),
            shared.get("output_output", ""),
            shared.get("poster_identity_output", ""),
            shared.get("post_title_output", ""),
            shared.get("post_classification_output", ""),
            shared.get("post_content_output", ""),
            shared.get("POSTER_interaction_feedback_create_output", ""),
            shared.get("USER_interaction_info_create_output", ""),
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
        
        response = call_llm(prompt=formatted_prompt)
        return response.strip()

    def post(self, shared, prep_res, exec_res):
        shared['USER_comment_create_output'] = exec_res




'''
[USER] CommentToInteractSelect
Function: Select a comment to interact with from post comments
Prep: buy_ispositive_output, output_output, poster_identity_output, post_title_output, post_classification_output, post_content_output, USER_interaction_info_create_output, USER_comment_create_output, USER_psychological_info_create_output
Post: USER_comment_to_interact_select_output
'''
class USER_CommentToInteractSelect(Node):
    def prep(self, shared):
        return (
            shared.get("buy_ispositive_output", ""),
            shared.get("output_output", ""),
            shared.get("poster_identity_output", ""),
            shared.get("post_title_output", ""),
            shared.get("post_classification_output", ""),
            shared.get("post_content_output", ""),
            shared.get("USER_interaction_info_create_output", ""),
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
[USER] InteractionInfoCreate
Function: Generate reply to selected comment
Prep: buy_ispositive_output, output_output, poster_identity_output, post_title_output, post_classification_output, post_content_output, USER_interaction_info_create_output, USER_comment_create_output, USER_comment_to_interact_select_output, USER_psychological_info_create_output
Post: USER_interaction_info_create_output
'''
class USER_InteractionInfoCreate(Node):
    def prep(self, shared):
        return (
            shared.get("buy_ispositive_output", ""),
            shared.get("output_output", ""),
            shared.get("poster_identity_output", ""),
            shared.get("post_title_output", ""),
            shared.get("post_classification_output", ""),
            shared.get("post_content_output", ""),
            shared.get("USER_interaction_info_create_output", ""),
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
        shared['USER_interaction_info_create_output'] = exec_res



'''
[OTHERUSER] InteractionFeedbackCreate
Function: Generate response to user's reply on comment
Prep: poster_identity_output, post_title_output, post_classification_output, post_content_output, USER_interaction_info_create_output, USER_comment_to_interact_select_output
Post: OTHERUSER_interaction_feedback_create_output
'''
class OTHERUSER_InteractionFeedbackCreate(Node):
    def prep(self, shared):
        return (
            shared.get("poster_identity_output", ""),
            shared.get("post_title_output", ""),
            shared.get("post_classification_output", ""),
            shared.get("post_content_output", ""),
            shared.get("USER_interaction_info_create_output", ""),
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
Prep: buy_ispositive_output, output_output, poster_identity_output, post_title_output, post_classification_output, post_content_output, poster_interaction_feedback_create_output, user_interaction_info_create_output, user_comment_create_output, user_comment_to_interact_select_output, OTHERUSER_interaction_feedback_create_output, user_psychological_info_create_output
Post: USER_psychological_info_create2_output
'''
class USER_PsychologicalInfoCreate2(Node):
    def prep(self, shared):
        return (
            shared.get("buy_ispositive_output", ""),
            shared.get("output_output", ""),
            shared.get("poster_identity_output", ""),
            shared.get("post_title_output", ""),
            shared.get("post_classification_output", ""),
            shared.get("post_content_output", ""),
            shared.get("POSTER_interaction_feedback_create_output", ""),
            shared.get("USER_interaction_info_create_output", ""),
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
Prep: buy_ispositive_output, output_output, post_title_output, post_classification_output, post_content_output, user_psychological_info_create_output
Post: USER_purchase_decide1_output
'''
class USER_PurchaseDecide1(Node):
    def prep(self, shared):
        return (
            shared.get("buy_ispositive_output", ""),
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
            shared.get("buy_ispositive_output", ""),
            shared.get("output_output", ""),
            shared.get("post_title_output", ""),
            shared.get("post_classification_output", ""),
            shared.get("post_content_output", ""),
            shared.get("USER_psychological_info_create_output", ""),
            shared.get("USER_psychological_info_create2_output", "")
        )

    def exec(self, prep_res):
        (buy_ispositive, output, post_title,
         post_classification, post_content,
         initial_psychological, interaction_psychological) = prep_res
        
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