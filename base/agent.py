import abc
import json
import ast
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


class AbstractAgent(abc.ABC):
    
    def __init__(self, name, llm=None, json_output=True, output_tracks=False, **kwargs):
        self.name = name
        self.llm = llm
        self.json_output = json_output
        self.output_tracks = output_tracks

    def act(self, input_dict=None, batch_mode=False, json=None):
        if json is not None:
            json_setting_backup = self.json_output
            self.json_output = json
        output = self.invoke_llm(input_dict, batch_mode=batch_mode)
        # TODO: batch mode for removing tracks
        if not self.output_tracks and isinstance(output, dict) and 'tracks' in output:
            try:
                # print(output, flush=True)
                output = output['result']
            except Exception as e:
                print(f"Failed to remove tracks from output: {e}")
        if json is not None:
            self.json_output = json_setting_backup
        # is_valid = self.check_json_output(output_json, input_dict)
        # if not is_valid:
        #     import pdb; pdb.set_trace()
        #     print(f"Invalid JSON response:\n{output.content}")
        #     return None
        return output

    def invoke_llm(self, input_dict, max_retries=10, batch_mode=False):
        num_retries = 0
        while num_retries < max_retries:
            results = self.invoke_llm_once(input_dict, batch_mode)
            if results is not None:
                return results
            num_retries += 1
        raise Exception("Failed to invoke LLM")

    def fix_json_string(self, json_str):
        if json_str.startswith('```') and json_str.endswith('```'):
            json_str_start = json_str[:10]
            json_str_main = json_str[10:-10]
            json_str_end = json_str[-10:]
            fix_json_str_start = json_str_start.replace('```', '').replace('```json', '').replace('```JSON', '')
            fix_json_str_end = json_str_end.replace('```', '')
            json_str = fix_json_str_start + json_str_main + fix_json_str_end
        return json_str

    def invoke_llm_once(self, input_dict, batch_mode=False):
        agent = self.prompt | self.llm
        output = agent.invoke(input_dict) if not batch_mode else agent.batch(input_dict)
        if not self.json_output:
            return output.content

        # Output the number of tokens used
        tokens_used = output.usage_metadata
        # print(f"Tokens used: {tokens_used}", flush=True)
        try:
            if batch_mode:
                output_json = [json.loads(o.content) for o in output]
            else:
                output_str = self.fix_json_string(output.content)
                # output_json = ast.literal_eval(output_str)
                output_json = json.loads(output_str)
        except json.JSONDecodeError:
            print(f"Failed to decode JSON response:\n{output.content}")
            # raise Exception(f"Failed to decode JSON response: \n{output.content}")
            try:
                output_str = self.fix_json_string(output.content)
                output_str = output_str.replace("\\'", "\'").replace("\\r", "\r").replace("\\t", "\t").replace("\\n", "\n")
                output_json = json.loads(output_str)
                return output_json
            except:
                output_str = self.fix_json_string(output.content)
                output_str = output_str.replace("\\'", "\'").replace("\\r", "\r").replace("\\t", "\t").replace("\\n", "\n")
                print(f"Failed to decode JSON response2:\n{output_str}")
                return None
        return output_json


class Agent(AbstractAgent):

    def __init__(self, name, llm=None, json_output=True, output_tracks=False, tools=None, **kwargs):
        super().__init__(name, llm, json_output=json_output, output_tracks=output_tracks, **kwargs)
        self.system_prompt = None
        self.task_prompt = None

    def check_json_output(self, output, input_dict):
        return True

    def set_prompts(self, system_prompt, task_prompt):
        self.system_prompt = system_prompt
        self.task_prompt = task_prompt
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ('system', self.system_prompt),
                ('human', self.task_prompt),
            ]
        )

    def update_prompts(self, system_prompt=None, task_prompt=None):
        if system_prompt:
            self.system_prompt = system_prompt
        if task_prompt:
            self.task_prompt = task_prompt
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ('system', self.system_prompt),
                ('human', self.task_prompt),
            ]
        )