from iipa_backend.config import TACTICS

# Azure OpenAI API parameters
PROMPT_TEMPLATE_FORMAT = 'jinja2'
OPENAI_MODEL_NAME = 'gpt-4o'
OPENAI_TEMPERATURE = 1e-16
OPENAI_API_TYPE = 'azure'
OPENAI_API_VERSION = '2024-02-01'
OPENAI_DEPLOYMENT_NAME = 'lunar-chatgpt-4o'
OPENAI_TOP_P = 1e-16
OPENAI_SEED = 1234


TACTIC_STR_TEMPLATE = f"""Name: {{label}}
Description of tactic: {{description}}
The prompt that will be used for this tactic: {{prompt}}"""
TACTICS_LIST = [
    TACTIC_STR_TEMPLATE.format(
        label=tactic_key,
        description=tactic_data['description'],
        prompt=tactic_data['prompt'],
    ) for tactic_key, tactic_data in TACTICS.items()
]
TACTICS_STR = '\n\n'.join(TACTICS_LIST)


EXAMPLE_TEMPLATE = f"""Example:
Task: {{task}}
Answer: {{answer}}"""
EXAMPLES_LIST = []
for tactic_key, tactic_data in TACTICS.items():
    for example in tactic_data.get('examples', []):
        EXAMPLES_LIST.append(
            EXAMPLE_TEMPLATE.format(
                task=example['task'],
                answer=tactic_key,
            )
        )
EXAMPLES_STR = '\n\n'.join(EXAMPLES_LIST)


NL2TACTIC_PROMPT_TEMPLATE = f"""You are an assistant choosing which tactic to use to solve a task defined in natural language.
You can choose between the following tactics:
==== Start of tactics list ====
{TACTICS_STR}
==== End of tactics list ====

Given the tactics above, choose which one to use for solving the task below.
Output nothing else than the tactic.

{EXAMPLES_STR}

TASK: {{prompt}}"""


# USER_PROMPT_WITH_HISTORY_TEMPLATE = """You are a proof assistent answering to prompts. Given the (possible empty) conversation history, answer to the new prompt.
USER_PROMPT_WITH_HISTORY_TEMPLATE = """CONVERSATION HISTORY:
{conversation_history}

NEW PROMPT:
{prompt}"""