# 和大模型来玩一场善与恶的博弈吧
## 游戏规则介绍
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

* 投票阶段: 游戏内的每一回合会自动产生一位'代表人', 玩家首先需要对当前回合'代表人'指定的'执行人'进行认可投票，执行人负责在接下来的卡牌裁决阶段选择卡牌。

* 卡牌阶段: 系统会从三张善良牌和六张邪恶牌中随机抽取三张。'代表人'从随机抽选的三张牌中弃置 1 张，'执行人'再查看剩余 2 张卡牌，从剩余 2 张中再弃置 1 张（注意，'执行人'无法知晓'代表人'弃置的卡牌），最终剩下的⼀张卡牌加入累计卡池。当恶魔牌每累积1张: 向神揭示1个普通恶魔身份（排除路西法），累积3张: 当前回合'代表人'可驱逐任意玩家

**胜利条件**

1.进入终局的条件: 

邪恶方: 累积4张邪恶牌, 此时恶魔阵营直接获胜

善良方: 累积4张善良牌, 进行终局判定

2.终局判定: 

当善良方达成条件时: 

路西法可进行1次神身份猜测, 猜测正确则恶魔阵营获胜，反之天使阵营获胜

## 项目运行
* 在`base/llms.py`中配置OPENAI_KEY
* `main.py`中设置你是几号玩家，即可运行。
* 可以使用`test.py`测试网络
