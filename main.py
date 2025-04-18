from base.llms import create_llm
from modules.game_agent import speech_with_llm, vote_with_llm, discard_with_llm, expelled_with_llm, guess_with_llm, summary_with_llm
import json
import os
import random
os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'


# 创建大语言模型实例
llm = create_llm(backbone="gpt4o")

# 定义角色和玩家名称
roles = ["神", "大天使", "普通天使", "普通天使", "路西法", "普通恶魔", "普通恶魔"]
random.shuffle(roles)
print("角色分配:")
player_names = ["player1", "player2", "player3", "player4", "player5", "player6", "player7"]
for player, role in zip(player_names, roles):
    print(f"{player}: {role}")
human_players = ["player3","player6"]  # 定义人类玩家

# 初始化所有轮次的游戏状态
all_game_states = []

# 初始化游戏状态
game_state = {
    "round": 1,
    "players": [{"name": name, "status": "alive"} for name in player_names],
    "speech_content": {},
    "accumulated_cards": [],
    "voting_results": [],
}

# 单独存储被揭示的恶魔身份
devil_revealed = []

# 恶魔之间互相知道身份
devil_known_identities = {}
for i, role in enumerate(roles):
    if role in ["路西法", "普通恶魔"]:
        devil_known_identities[player_names[i]] = [player_names[j] for j, r in enumerate(roles) if r in ["路西法", "普通恶魔"] and j != i]

# 辅助函数：获取存活玩家
def get_alive_players():
    return [player["name"] for player in game_state["players"] if player["status"] == "alive"]

# 辅助函数：获取代表人候选人
def get_representative_candidate():
    alive_players = get_alive_players()
    index = (game_state["round"] - 1) % len(alive_players)
    return alive_players[index]

# 辅助函数：获取执行人候选人
def get_executor_candidate(representative):
    alive_players = get_alive_players()
    alive_players.remove(representative)
    if representative in human_players:
        while True:
            executor = input(f"{representative}, 请选择一名执行人候选人（{', '.join(alive_players)}）: ")
            if executor in alive_players:
                return executor
            else:
                print("无效的选择，请重新输入。")
    else:
        if roles[player_names.index(representative)] == "神":
            speech_content = speech_with_llm(llm, representative, roles[player_names.index(representative)], game_state["round"], game_state, all_game_states, devil_revealed, representative)
        else:
            speech_content = speech_with_llm(llm, representative, roles[player_names.index(representative)], game_state["round"], game_state, all_game_states, '', representative)
        print(f"{representative} 的发言: {speech_content}")
        executor = speech_content.get("executor")
        if executor not in alive_players:
            # 如果智能体选择无效，随机选择一个
            import random
            print("random")
            executor = random.choice(alive_players)
        return executor

# 辅助函数：进行发言阶段
def speech_phase(representative, executor):
    alive_players = get_alive_players()
    representative_index = alive_players.index(representative)
    # 先让代表人发言
    if representative in human_players:
        speech = input(f"{representative}, 请发表你的看法: ")
        executor = input(f"{representative}, 请选择一名执行人候选人（{', '.join(alive_players)}）: ")
        if executor in alive_players:
            pass
        else:
            print("无效的选择，请重新输入。")
        game_state["speech_content"][representative] = {"content": speech, "executor": executor}
    else:
        if roles[player_names.index(representative)] == "神":
            speech_content = speech_with_llm(llm, representative, roles[player_names.index(representative)], game_state["round"], game_state, all_game_states, devil_revealed, representative)
        elif roles[player_names.index(representative)] in ["路西法", "普通恶魔"]:
            speech_content = speech_with_llm(llm, representative, roles[player_names.index(representative)], game_state["round"], game_state, all_game_states, devil_known_identities[representative], representative)
        else:
            speech_content = speech_with_llm(llm, representative, roles[player_names.index(representative)], game_state["round"], game_state, all_game_states, '', representative)
        executor = speech_content.get("executor")
        if executor not in alive_players:
            # 如果智能体选择无效，随机选择一个
            import random
            print("random")
            executor = random.choice(alive_players)
        game_state["speech_content"][representative] = speech_content.get("content")
    print(f"{representative} 的发言: {game_state['speech_content'][representative]}")

    # 按顺序让其他玩家发言
    for i in range(1, len(alive_players)):
        player = alive_players[(representative_index + i) % len(alive_players)]
        if player in human_players:
            speech = input(f"{player}, 请发表你的看法: ")
            game_state["speech_content"][player] = {"content": speech, "executor": "" if player != representative else executor}
        else:
            if roles[player_names.index(player)] == "神":
                content = speech_with_llm(llm, player, roles[player_names.index(player)], game_state["round"], game_state, all_game_states, devil_revealed, representative).get("content")
            elif roles[player_names.index(player)] in ["路西法", "普通恶魔"]:
                content = speech_with_llm(llm, player, roles[player_names.index(player)], game_state["round"], game_state, all_game_states, devil_known_identities[player], representative).get("content")
            else:
                content = speech_with_llm(llm, player, roles[player_names.index(player)], game_state["round"], game_state, all_game_states, '', representative).get("content")
            game_state["speech_content"][player] = content
        print(f"{player} 的发言: {game_state['speech_content'][player]}")
    return executor

# 辅助函数：进行投票阶段
def voting_phase(representative, executor):
    votes = []
    for player in get_alive_players():
        if player in human_players:
            while True:
                vote = input(f"{player}, 你是否赞同 {executor} 作为执行人（赞同/反对）: ")
                if vote in ["赞同", "反对"]:
                    votes.append(vote)
                    break
                else:
                    print("无效的投票，请输入 '赞同' 或 '反对'。")
        else:
            if roles[player_names.index(player)] == "神":
                vote_result = vote_with_llm(llm, player, roles[player_names.index(player)], game_state["round"], game_state, all_game_states, representative, executor, devil_revealed)
            elif roles[player_names.index(player)] in ["路西法", "普通恶魔"]:
                vote_result = vote_with_llm(llm, player, roles[player_names.index(player)], game_state["round"], game_state, all_game_states, representative, executor, devil_known_identities[player])
            else:
                vote_result = vote_with_llm(llm, player, roles[player_names.index(player)], game_state["round"], game_state, all_game_states, representative, executor, '')
            vote = vote_result.get("vote")
            votes.append(vote)
            print(f"{player} 的投票: {vote}")
    game_state["voting_results"] = votes
    return votes.count("赞同") >= len(votes) / 2

# 辅助函数：进行卡牌裁决阶段
def card_judgment_phase(representative, executor):
    import random
    all_cards = ["善良"] * 3 + ["邪恶"] * 6
    drawn_cards = random.sample(all_cards, 3)
    print(f"GM 抽取的三张牌: {drawn_cards}")

    # 代表人弃牌
    if representative in human_players:
        while True:
            discarded_card = input(f"{representative}, 请选择一张牌弃置（{', '.join(drawn_cards)}）: ")
            if discarded_card in drawn_cards:
                break
            else:
                print("无效的选择，请重新输入。")
    else:
        if roles[player_names.index(representative)] == "神":
            discarded = discard_with_llm(llm, representative, roles[player_names.index(representative)], game_state["round"], game_state, all_game_states, drawn_cards, devil_revealed)
        elif roles[player_names.index(representative)] in ["路西法", "普通恶魔"]:
            discarded = discard_with_llm(llm, representative, roles[player_names.index(representative)], game_state["round"], game_state, all_game_states, drawn_cards, devil_known_identities[representative])
        else:
            discarded = discard_with_llm(llm, representative, roles[player_names.index(representative)], game_state["round"], game_state, all_game_states, drawn_cards,'')
        discarded_card = discarded.get("discarded_card")
    drawn_cards.remove(discarded_card)
    # print(f"{representative} 弃置了: {}")

    # 执行人弃牌
    if executor in human_players:
        while True:
            discarded_card = input(f"{executor}, 请选择一张牌弃置（{', '.join(drawn_cards)}）: ")
            if discarded_card in drawn_cards:
                break
            else:
                print("无效的选择，请重新输入。")
    else:
        if roles[player_names.index(executor)] == "神":
            discarded = discard_with_llm(llm, executor, roles[player_names.index(executor)], game_state["round"], game_state, all_game_states, drawn_cards, devil_revealed)
        elif roles[player_names.index(executor)] in ["路西法", "普通恶魔"]:
            discarded = discard_with_llm(llm, executor, roles[player_names.index(executor)], game_state["round"], game_state, all_game_states, drawn_cards, devil_known_identities[executor])
        else:
            discarded = discard_with_llm(llm, executor, roles[player_names.index(executor)], game_state["round"], game_state, all_game_states, drawn_cards,'')
        discarded_card = discarded.get("discarded_card")
    try:
        drawn_cards.remove(discarded_card)
    except ValueError:
        # 如果执行人选择的卡牌已经被代表人弃置，则随机选择一张
        discarded_card = random.choice(drawn_cards)
        drawn_cards.remove(discarded_card)
    # print(f"{executor} 弃置了: {discarded_card}")

    # 加入累积卡牌
    final_card = drawn_cards[0]
    game_state["accumulated_cards"].append(final_card)
    print(f"本轮累积的卡牌: {final_card}")

    # 处理邪恶卡牌累积效果
    if final_card == "邪恶":
        evil_count = game_state["accumulated_cards"].count("邪恶")
            # 揭示一个普通恶魔身份给神
        try:
            devil_index = [i for i, role in enumerate(roles) if role == "普通恶魔" and player_names[i] not in devil_revealed][0]
            devil_revealed.append(player_names[devil_index])
            print(f"神得知了 {player_names[devil_index]} 是普通恶魔。")
        except Exception as e:
            print("没有普通恶魔身份可以揭示。")
        if evil_count == 3:
            # 代表人驱逐一名玩家
            alive_players = get_alive_players()
            if representative in human_players:
                while True:
                    if roles[player_names.index(representative)] == "神":
                        print(f"已知的恶魔身份有：{devil_revealed}")
                    expelled_player = input(f"{representative}, 你可以驱逐一名玩家（{', '.join(alive_players)}）: ")
                    if expelled_player in alive_players:
                        break
                    else:
                        print("无效的选择，请重新输入。")
            else:
                if roles[player_names.index(representative)] == "神":
                    expelled_player = expelled_with_llm(llm, representative, roles[player_names.index(representative)], game_state["round"], game_state, all_game_states, representative, executor, devil_revealed).get("expelled_player")
                elif roles[player_names.index(representative)] in ["路西法", "普通恶魔"]:
                    expelled_player = expelled_with_llm(llm, representative, roles[player_names.index(representative)], game_state["round"], game_state, all_game_states, representative, executor, devil_known_identities[representative]).get("expelled_player")
                else:
                    expelled_player = expelled_with_llm(llm, representative, roles[player_names.index(representative)], game_state["round"], game_state, all_game_states, representative, executor, '').get("expelled_player")
                if expelled_player not in alive_players:
                    # 如果智能体选择无效，随机选择一个
                    import random
                    expelled_player = random.choice(alive_players)
            for player in game_state["players"]:
                if player["name"] == expelled_player:
                    player["status"] = "dead"
            print(f"{representative} 驱逐了 {expelled_player}，其身份是 {roles[player_names.index(expelled_player)]}。")

# 主游戏循环
executor = None
while True:
    print(f"\n第 {game_state['round']} 轮游戏开始")

    # 推选代表人
    representative = get_representative_candidate()
    print(f"本轮代表人候选人: {representative}")


    # 发言阶段
    executor =  speech_phase(representative, executor)

    # 投票阶段
    vote_success = False
    consecutive_failures = 0
    while not vote_success:
        vote_success = voting_phase(representative, executor)
        if not vote_success:
            consecutive_failures += 1
            if consecutive_failures == 2:
                print("连续两次投票失败，第三次无需投票，直接确定代表人和执行人。")
                vote_success = True
            else:
                print("投票失败，重新推选代表人。")
                game_state["round"] += 1
                representative = get_representative_candidate()
                print(f"新的代表人候选人: {representative}")
                speech_phase(representative, executor)
    
    # 卡牌裁决阶段
    card_judgment_phase(representative, executor)

    # 检查胜利条件
    good_count = game_state["accumulated_cards"].count("善良")
    evil_count = game_state["accumulated_cards"].count("邪恶")
    if good_count == 4:
        print("天使阵营累积了4张善良卡牌，进入终局判定。")
        if "路西法" in roles:
            lucifer_index = roles.index("路西法")
            lucifer_name = player_names[lucifer_index]
            if lucifer_name in human_players:
                guess = input(f"{lucifer_name}，请猜测神的身份: ")
            else:
                alive_angels = [name for name, role in zip(player_names, roles) if role in ["神", "大天使", "普通天使"] and name in get_alive_players()]
                guess = guess_with_llm(llm, lucifer_name, roles[lucifer_index], game_state["round"], game_state, all_game_states).get("guess")
                print("路西法的猜测:", guess)
            if guess == player_names[roles.index("神")]:
                print("路西法猜对了神的身份，恶魔阵营获胜！")
            else:
                print("路西法猜错了神的身份，天使阵营获胜！")
        all_game_states.append(game_state.copy())
        break
    elif evil_count == 4:
        print("恶魔阵营累积了4张邪恶卡牌，恶魔阵营获胜！")
        all_game_states.append(game_state.copy())
        break

    # 记录当前轮次的游戏状态
    all_game_states.append(game_state.copy())

    # 进入下一轮
    game_state["round"] += 1

for role in roles:
    try:
        play_index = roles.index(role)
        player_name = player_names[play_index]
        guess = summary_with_llm(llm, player_name, roles[play_index], all_game_states).get("summary")
        print(f"玩家{player_name}的猜测:", guess)
    except Exception as e:
        print(f"玩家{player_name}的猜测发生错误:", str(e))

with open('records/all_game_state.json', 'w') as f:
    json.dump(all_game_states, f, ensure_ascii=False, indent=4)

with open('records/game_state.json', 'w') as f:
    json.dump(game_state, f, ensure_ascii=False, indent=4)