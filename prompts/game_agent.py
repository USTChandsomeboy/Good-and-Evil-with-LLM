from .basic_templetes import output_format_title_templete, cot_output_format_templete

speech_output_format = """
{{
    "content":""
    "executor":"如果你是代表人，则需要在发言时指定执行人候选人，直接说出执行人候选人名称即可，如player2"
}}
"""
vote_output_format = """
{{
    "vote": 赞同或反对,
}}
"""
discard_output_format = """
{{
    "discarded_card":"你想要弃置的卡牌名称"
}}
"""

expelled_output_format = """
{{
    "expelled_player":"你想要驱逐的玩家名称"
}}
"""

guess_output_format = """
{{
    "guess":"你想要猜测的神的身份名称"
}}
"""

summary_output_format = """
{{
    "summary":"你想要总结的内容"
}}
"""

speech_output_format_with_title = speech_output_format + output_format_title_templete
cot_speech_output_format_with_title = speech_output_format + cot_output_format_templete.replace("RESULT_OUTPUT_FORMAT", speech_output_format_with_title)

vote_output_format_with_title = vote_output_format + output_format_title_templete
cot_vote_output_format_with_title = vote_output_format + cot_output_format_templete.replace("RESULT_OUTPUT_FORMAT", vote_output_format_with_title)

discard_output_format_with_title = discard_output_format + output_format_title_templete
cot_discard_output_format_with_title = discard_output_format + cot_output_format_templete.replace("RESULT_OUTPUT_FORMAT", discard_output_format_with_title)

expelled_output_format_with_title = expelled_output_format + output_format_title_templete
cot_expelled_output_format_with_title = expelled_output_format + cot_output_format_templete.replace("RESULT_OUTPUT_FORMAT", expelled_output_format_with_title)

guess_output_format_with_title = guess_output_format + output_format_title_templete
cot_guess_output_format_with_title = guess_output_format + cot_output_format_templete.replace("RESULT_OUTPUT_FORMAT", guess_output_format_with_title)

summary_output_format_with_title = summary_output_format + output_format_title_templete
cot_summary_output_format_with_title = summary_output_format + cot_output_format_templete.replace("RESULT_OUTPUT_FORMAT", summary_output_format_with_title)


game_system_prompt_base = """
"请你模拟一位玩家参加一款类似狼人杀和阿瓦隆的游戏'天使与恶魔', 游戏的规则如下:

```
游戏共有7名玩家，分为两个阵营:天使阵营和恶魔阵营。
**阵营设置**
天使阵营(4人):
神(1人):神需要隐藏自己的身份不被恶魔阵营发现，同时隐晦的帮助天使阵营积累善良卡牌获得胜利。当积累邪恶卡牌时，神会知晓恶魔的身份信息。
大天使(1人):大天使知晓神的身份，需要帮助天使阵营积累善良卡牌获得胜利。
普通天使(2人):需要帮助天使阵营积累善良卡牌获得胜利。
除了大天使知晓神的身份信息外，天使阵营彼此不知晓身份。

恶魔阵营(3人):
路西法(1人):路西法需要帮助恶魔阵营积累邪恶卡牌获得胜利或者找到天使阵营中隐藏的神获得胜利。但是路西法的身份信息不会在积累卡牌时透露给神。
普通恶魔(2人):普通恶魔需要帮助恶魔阵营积累邪恶卡牌获得胜利或者找到天使阵营中隐藏的神获得胜利。普通恶魔的身份信息在积累邪恶卡牌时会透露给神。
恶魔阵营彼此知晓互相身份。

**回合流程**
每一轮游戏分为两个阶段:投票阶段和卡牌阶段。
投票阶段:
游戏内的每一回合会自动产生一位'代表人', 玩家首先需要对当前回合'代表人'指定的'执行人'进行认可投票，执行人负责在接下来的卡牌裁决阶段选择卡牌。
卡牌阶段:
系统会从三张善良牌和六张邪恶牌中随机抽取三张。
'代表人'从随机抽选的三张牌中弃置 1 张，'执行人'再查看剩余 2 张卡牌，从剩余 2 张中再弃置 1 张（注意，'执行人'无法知晓'代表人'弃置的卡牌），最终剩下的⼀张卡牌加入累计卡池。
当恶魔牌每累积1张: 向神揭示1个普通恶魔身份（排除路西法），累积3张: 当前回合'代表人'可驱逐任意玩家

**胜利条件**
1进入终局的条件: 
邪恶方: 累积4张邪恶牌, 此时恶魔阵营直接获胜
善良方: 累积4张善良牌, 进行终局判定
2终局判定: 
当善良方达成条件时: 
路西法可进行1次神身份猜测, 猜测正确则恶魔阵营获胜，反之天使阵营获胜
```

"""

game_system_prompt_base_backup = """
"请你模拟一位玩家参加一款类似狼人杀和阿瓦隆的游戏'天使与恶魔', 游戏的规则如下:
游戏共有七名玩家，分为两个阵营:天使阵营和恶魔阵营。
**阵营设置**
天使阵营(4人):
神(1人):神需要隐藏自己的身份不被恶魔阵营发现，同时隐晦的帮助天使阵营积累善良卡牌获得胜利。当积累邪恶卡牌时，神会知晓恶魔的身份信息。
大天使(1人):大天使知晓神的身份，需要帮助天使阵营积累善良卡牌获得胜利。
普通天使(2人):需要帮助天使阵营积累善良卡牌获得胜利。
除了大天使知晓神的身份信息外，天使阵营彼此不知晓身份。

恶魔阵营(3人):
路西法(1人):路西法需要帮助恶魔阵营积累邪恶卡牌获得胜利或者找到天使阵营中隐藏的神获得胜利。但是路西法的身份信息不会在积累卡牌时透露给神。
普通恶魔(2人):普通恶魔需要帮助恶魔阵营积累邪恶卡牌获得胜利或者找到天使阵营中隐藏的神获得胜利。普通恶魔的身份信息在积累邪恶卡牌时会透露给神。
恶魔阵营彼此知晓互相身份。

**卡牌设置**
总共9张卡牌，其中善良卡牌3张，邪恶卡牌6张。

**回合流程**

阶段1:代表推选
代表人产生:采⽤轮序制，每回合按玩家编号递增产⽣代表候选⼈，⼀轮结束后重新循环。
执行人产生:代表候选⼈需从其他玩家中选择1名执⾏⼈候选⼈。
发言阶段:然后每名玩家可以发表⾃⼰对这组代表人候选人和执行人候选人的看法，按顺序发⾔。
投票阶段:发言结束后，全体玩家进行投票，当赞成票大于等于存活玩家半数:则该组合代表人与执行人选定成功。否则选定失败，到下一个代表人产生。
如果连续2次投票失败，则第3次⽆需投票，代表候选⼈选定执⾏候选⼈直接确定，进行卡牌裁决阶段。

阶段2:卡牌裁决
管理者(GM)随机抽取3张卡牌公开给代表⼈。
代表⼈先查看3张卡牌，先弃置1张。
执⾏⼈再查看剩余2张卡牌，从剩余2张中再弃置1张(注意，执⾏⼈⽆法知晓代表⼈弃置的卡牌)。
最终剩下的⼀张卡牌加⼊当前累积卡牌(每次抽取仍然是9张卡牌，3张善良牌，6张邪恶牌)。
注意:除了代表人和执行人其他玩家不知晓3张卡牌信息以及弃置卡牌信息，只知道最后累积了什么卡牌。当然代表人和执行人可以在后续发言进行说明，可以说明事实或撒谎。


**信息揭露机制**
邪恶卡牌累积效果
每累积1张邪恶卡牌:向神揭示1个普通恶魔身份(路西法除外)。
当累积3张邪恶卡牌:当前回合的代表人可驱逐任意一名玩家(⽴即公示身份)。

**胜利条件**
终局条件
天使阵营:累积4张善良卡牌。
恶魔阵营:累积4张邪恶卡牌。

终局判定
当天使阵营达成条件时:路西法可进⾏1次神的身份猜测。管理者(GM)验证猜测，若正确，恶魔阵营获胜；若错误，天使阵营获胜。
当恶魔阵营达成条件时:恶魔阵营获胜。
"""

game_system_prompt = game_system_prompt_base


speech_task_prompt = """
你游戏内的名称是{player_name}
你的游戏角色是{role}，你需要根据游戏规则进行游戏。
当前代表人是{representative}。如果你是代表人，请你说出指定的执行人候选人。
当前是游戏的第{round}轮，当前的游戏状态如下:
{game_state}
之前的游戏记录如下:
{all_game_state}
已知的恶魔身份有:{known_devils}。
请你根据游戏状态，给出你在本轮游戏中的发言内容。你可以在适当的时机撒谎来引导其他玩家，但你也要留意其他玩家撒谎的可能性。请注意，你的发言内容需要符合你的角色身份和游戏规则，并且要尽量让其他玩家相信你是天使阵营的角色。
CODE_GENERATION_OUTPUT_FORMAT
"""

vote_task_prompt = """
你游戏内的名称是{player_name}，你是游戏中的一名玩家。
你的游戏角色是{role}，你需要根据游戏规则进行游戏。
当前是游戏的第{round}轮，当前的游戏状态如下:
{game_state}
之前的游戏记录如下:
{all_game_state}
已知的恶魔身份有:{known_devils}。
当前代表人是{representative}，执行人候选是{executor}。
请你根据游戏状态，给出你在本轮游戏中的投票内容，你是否赞同执行人的选举。请注意，你的投票内容需要符合你的角色身份和游戏规则，并且要尽量让其他玩家相信你是天使阵营的角色。
你需要回答赞同或者反对
通常来说，赞同和你同阵营的执行人对你更加有利，但这可能暴露你的所在阵营，请你对当前的形式综合分析并做出选择。
"""

discard_task_prompt = """
你游戏内的名称是{player_name}，你是游戏中的一名玩家。
你的游戏角色是{role}，你需要根据游戏规则进行游戏。
当前是游戏的第{round}轮，当前的游戏状态如下:
{game_state}
之前的游戏记录如下:
{all_game_state}
抽取的卡牌是:{discarded_cards}。
已知的恶魔身份有:{known_devils}。
请你根据游戏状态，并考虑弃置卡牌所带来的效果，给出你在本轮游戏中的弃置卡牌内容。请注意，你的弃置卡牌内容需要符合你的角色身份和游戏规则，并且要尽量让其他玩家相信你是天使阵营的角色。
并且你选择弃置的卡牌是必须存在于抽取的卡牌中。
CODE_GENERATION_OUTPUT_FORMAT
"""

expelled_task_prompt = """
你游戏内的名称是{player_name}，你是游戏中的一名玩家。
你的游戏角色是{role}，你需要根据游戏规则进行游戏。
当前是游戏的第{round}轮，当前的游戏状态如下:
{game_state}
之前的游戏记录如下:
{all_game_state}
已知的恶魔身份有:{known_devils}。
当前的代表人是{representative}，执行人是{executor}。
请你根据游戏状态，给出你在本轮游戏中的驱逐玩家内容。请注意，你的驱逐玩家内容需要符合你的角色身份和游戏规则，并且要尽量让其他玩家相信你是天使阵营的角色。
"""

guess_task_prompt = """
你游戏内的名称是{player_name}，你是游戏中的一名玩家。
你的游戏角色是{role}，你需要根据游戏规则进行游戏。
当前是游戏的第{round}轮，所有游戏记录如下:
{game_state}
之前的游戏记录如下:
{all_game_state}
当前游戏结束，你需要猜测神的身份，你的选择会直接决定游戏的胜负，请你根据当前的局势仔细分析，谨慎做出选择。
"""

summary_task_prompt = """你游戏内的名称是{player_name}，你是游戏中的一名玩家。
你的游戏角色是{role}。所有的游戏记录如下:
{all_game_state}
请你总结你对其他玩家的身份猜测和游戏的理解。解释出你每一轮的发言、投票和行动的原因。
"""


guess_task_prompt = guess_task_prompt.replace("CODE_GENERATION_OUTPUT_FORMAT", cot_guess_output_format_with_title)
speech_task_prompt = speech_task_prompt.replace("CODE_GENERATION_OUTPUT_FORMAT", cot_speech_output_format_with_title)
vote_task_prompt = vote_task_prompt.replace("CODE_GENERATION_OUTPUT_FORMAT", cot_vote_output_format_with_title)
discard_task_prompt = discard_task_prompt.replace("CODE_GENERATION_OUTPUT_FORMAT", cot_discard_output_format_with_title)
expelled_task_prompt = expelled_task_prompt.replace("CODE_GENERATION_OUTPUT_FORMAT", cot_expelled_output_format_with_title)
summary_task_prompt = summary_task_prompt.replace("CODE_GENERATION_OUTPUT_FORMAT", cot_summary_output_format_with_title)

from .basic_templetes import output_format_requirements_templete

task_prompt_vars = [var_name for var_name in globals() if "task_prompt" in var_name]
for var_name in task_prompt_vars:
    globals()[var_name] += output_format_requirements_templete