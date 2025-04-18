output_format_title_templete = """
**Output Format:**
"""

cot_output_format_templete = """
{{
    "tracks": [
        The thought result for input of step 1 (max 50 words),
        The thought result for input of step 2 (max 50 words),
        ...
    ],
    "result": RESULT_OUTPUT_FORMAT
}}

- If the CoT is unavailable (i.e.,., no chain of thoughts are provided in the prompt), set the "tracks" field to an empty list.
- Ensure the first level of the JSON object contains the "tracks" and "result" fields.
- Ensure the "tracks" field is a list of thought results, each of which is a string of at most 50 words.
- Ensure the "result" field contains the final desired output.
"""

output_format_requirements_templete = """

**Output format requirements:**
- Must!!! Must!!! Must!!! Ensure the output is correct and valid JSON format following the provided output format.
- Must!!! Must!!! Must!!! Do not include any tags (``` and ```json tag)
- Must!!! Must!!! Must!!! Do not start fron ``` and end with ```
- Must!!! Must!!! Must!!! only the JSON output. Do not output any additional information (e.g, explanation, comments, notes etc.)
- Must!!! Must!!! Must!!! Ensure Output only and just is a JSON object!!!
- Must!!! Must!!! Must!!! Do not start from some explanation or any other information before the JSON output!!!
- Must!!! Must!!! Must!!! Ensure proper escaping so the final result can be successfully loaded using json.loads.
- If your output includes JSON-related content within an item of the original format, ensure it is correctly escaped and formatted.
- Before output, ensure the final result is correct and valid JSON format following the provided output format.
- Must!!! Must!!! Must!!! The first word of your output must be {{ or [ and the last word of your output must be }} or ].
- The language of the output should be same as the learning goal that user provided.
"""

batch_evaluation_requirements_prompt = """

**Batch Evaluation Requirements:**
- Before evaluation, carefully review the input batch to ensure the number of entries and their IDs are correct and consistent.
- Your output should be structured as a list of evaluations, with each entry clearly linked to its respective set of skill requirements by using the “id” field. 
- Must ensure a one-to-one correspondence between input and output entries by matching each output entry to its respective input ID.
- Must Ensure the number of output entries matches the number of input entries.
- You must output the evaluation results in the same order as the input batch. All ids in List of batch ids should be present in the output.
"""