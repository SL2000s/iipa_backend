###############################
######## TACTIC PROMPT ########
###############################
TACTIC_STR_TEMPLATE = """Name: {label}
Description of tactic: {description}
The prompt that will be used for this tactic: \"\"\"{prompt}\"\"\""""



##########################################
######## EXAMPLE NL2TACTIC PROMPT ########
##########################################
EXAMPLE_NL2TACTIC_TEMPLATE = """Example:
Task: \"\"\"{task}\"\"\"
Answer: {answer}"""



##################################
######## NL2TACTIC PROMPT ########
##################################
NL2TACTIC_TEMPLATE = """You are an assistant choosing which tactic to use to solve a task defined in natural language.
You can choose between the following tactics:
==== Start of tactics list ====
{tactics}
==== End of tactics list ====

Given the tactics above, choose which one to use for solving the task below.
Output nothing else than the tactic.

{examples}

TASK: {prompt}"""



#####################################
######## PROMPT WITH HISTORY ########
#####################################
PROMPT_WITH_HISTORY_TEMPLATE = """CONVERSATION HISTORY:
{history}

CURRENT PROMPT:
{prompt}"""



###################################################
######## EXAMPLE PROMPT2TEMPLATE_VARIABLES ########
###################################################
EXAMPLE_PROMPT2TEMPLATE_VARIABLES_TEMPLATE = """Example:
User instruction: {user_prompt}
Answer: {answer}
"""



###########################################
######## PROMPT2TEMPLATE_VARIABLES ########
###########################################
PROMPT2TEMPLATE_VARIABLES_TEMPLATE = """You are a prompt engineer assistant who converts instructions from the user to template variables which will be used when rendering a given prompt template.
Output a dict with the template variable names as keys mapped to their corresponding values (which are strings that you formulates).
Output according to the examples below.
Output nothing else than the dictionary.

PROMPT TEMPLATE: \"\"\"{prompt_template}\"\"\"
TEMPLATE VARIABLES: {template_variables}

{examples}

USER INSTRUCTION: {user_prompt}"""
