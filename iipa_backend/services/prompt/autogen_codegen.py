import os
import autogen
from autogen import AssistantAgent, UserProxyAgent


from iipa_backend.config.config import (
    OPENAI_API_TYPE,
    OPENAI_API_VERSION,
    OPENAI_DEPLOYMENT_NAME,
    AUTOGEN_TMP_DIR,
    INDEX_QUERY_CONTEXT_START,
    INDEX_QUERY_CONTEXT_END,
)
from iipa_backend.utils.utils import a_capture_prints, delete_directory


async def a_generate_code(quest, hide_content=True):
    llm_config = {                                  # TODO: move out from method (then do same in llm_quest.py)
        "model": OPENAI_DEPLOYMENT_NAME,
        "api_key": os.environ["OPENAI_API_KEY"],
        "base_url": os.environ["AZURE_ENDPOINT"],
        "api_type": OPENAI_API_TYPE,
        "api_version": OPENAI_API_VERSION,
    }
    assistant = AssistantAgent("assistant", llm_config=llm_config)
    user_proxy = UserProxyAgent(
        name="user_proxy",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=10,
        is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
        code_execution_config={"executor": autogen.coding.LocalCommandLineCodeExecutor(work_dir=AUTOGEN_TMP_DIR)}
    )
    chat_result = await a_capture_prints(
        lambda: user_proxy.a_initiate_chat(
            assistant,
            message=quest,
        )
    )
    delete_directory(AUTOGEN_TMP_DIR)
    if hide_content:
        i_start = chat_result.find(INDEX_QUERY_CONTEXT_START) + len(INDEX_QUERY_CONTEXT_START)
        i_end = chat_result.find(INDEX_QUERY_CONTEXT_END)
        chat_result = chat_result[:i_start] + "\n[HIDDEN CONTEXT...]\n" + chat_result[i_end:]
    return chat_result
