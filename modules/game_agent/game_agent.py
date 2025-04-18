from base import Agent
from prompts import game_system_prompt, \
                    speech_task_prompt, \
                    vote_task_prompt, \
                    discard_task_prompt, \
                    expelled_task_prompt, \
                    guess_task_prompt, \
                    summary_task_prompt
                    
class GameAgent(Agent):

    def __init__(self, llm):
        super().__init__('GameAgent', llm=llm, json_output=True, output_tracks=False)

    def speech(self, input_dict):

        self.set_prompts(game_system_prompt, speech_task_prompt)
        output = self.act(input_dict)
        return output
    def vote(self, input_dict):

        self.set_prompts(game_system_prompt, vote_task_prompt)
        output = self.act(input_dict)
        return output
    def discard(self, input_dict):

        self.set_prompts(game_system_prompt, discard_task_prompt)
        output = self.act(input_dict)
        return output
    def expelled(self, input_dict):
        self.set_prompts(game_system_prompt, expelled_task_prompt)
        output = self.act(input_dict)
        return output
    def guess(self, input_dict):
        self.set_prompts(game_system_prompt, guess_task_prompt)
        output = self.act(input_dict)
        return output
    def summary(self, input_dict):
        self.set_prompts(game_system_prompt, summary_task_prompt)
        output = self.act(input_dict, json=False)
        return output

def speech_with_llm(llm, player_name, role, round, game_state, all_game_state, known_devils, representative):
    speech_agent= GameAgent(llm)
    try:
        content = speech_agent.speech({
            "player_name": player_name,
            "role": role,
            "round": round,
            "game_state": game_state,
            "all_game_state": all_game_state,
            "known_devils": known_devils,
            "representative": representative,
        })
        return content
    except Exception as e:
        raise Exception(str(e))
def vote_with_llm(llm, player_name, role, round, game_state, all_game_state, representative, executor, known_devils):
    vote_agent= GameAgent(llm)
    try:
        vote = vote_agent.vote({
            "player_name": player_name,
            "role": role,
            "round": round,
            "game_state": game_state,
            "all_game_state": all_game_state,
            "representative": representative,
            "executor": executor,
            "known_devils": known_devils,
        })
        return vote
    except Exception as e:
        raise Exception(str(e))
    
def discard_with_llm(llm, player_name, role, round, game_state, all_game_state, discarded_cards, known_devils):
    discard_agent= GameAgent(llm)
    try:
        discard = discard_agent.discard({
            "player_name": player_name,
            "role": role,
            "round": round,
            "game_state": game_state,
            "all_game_state": all_game_state,
            "discarded_cards": discarded_cards,
            "known_devils": known_devils,
        })
        return discard
    except Exception as e:
        raise Exception(str(e))

def expelled_with_llm(llm, player_name, role, round, game_state, all_game_state, representative, executor, known_devils):
    expelled_agent= GameAgent(llm)
    try:
        expelled = expelled_agent.expelled({
            "player_name": player_name,
            "role": role,
            "round": round,
            "game_state": game_state,
            "all_game_state": all_game_state,
            "representative": representative,
            "executor": executor,
            "known_devils": known_devils,
        })
        return expelled
    except Exception as e:
        raise Exception(str(e))
def guess_with_llm(llm, player_name, role, round, game_state, all_game_state):
    guess_agent= GameAgent(llm)
    try:
        guess = guess_agent.guess({
            "player_name": player_name,
            "role": role,
            "round": round,
            "game_state": game_state,
            "all_game_state": all_game_state,
        })
        return guess
    except Exception as e:
        raise Exception(str(e))
    
def summary_with_llm(llm, player_name, role, all_game_state):
    summary_agent= GameAgent(llm)
    try:
        guess = summary_agent.summary({
            "player_name": player_name,
            "role": role,
            "all_game_state": all_game_state,
        })
        return guess
    except Exception as e:
        print(e)
        raise Exception(str(e))