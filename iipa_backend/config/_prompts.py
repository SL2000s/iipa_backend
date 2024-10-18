############################
######## NEW PROMPT ########
############################
TACTIC_STR_TEMPLATE = """Name: {label}
Description of tactic: {description}
The prompt that will be used for this tactic: {prompt}"""


############################
######## NEW PROMPT ########
############################
EXAMPLE_TEMPLATE = """Example:
Task: {task}
Answer: {answer}"""


############################
######## NEW PROMPT ########
############################
NL2TACTIC_PROMPT_TEMPLATE = """You are an assistant choosing which tactic to use to solve a task defined in natural language.
You can choose between the following tactics:
==== Start of tactics list ====
{tactics_str}
==== End of tactics list ====

Given the tactics above, choose which one to use for solving the task below.
Output nothing else than the tactic.

{examples_str}

TASK: {prompt}"""


############################
######## NEW PROMPT ########
############################
PROMPT_WITH_HISTORY_TEMPLATE = """CONVERSATION HISTORY:
{history}

NEW PROMPT:
{prompt}"""
