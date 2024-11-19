import os
import autogen
from autogen import AssistantAgent, UserProxyAgent


from iipa_backend.config.config import (
    OPENAI_API_TYPE,
    OPENAI_API_VERSION,
    OPENAI_DEPLOYMENT_NAME,
)
from iipa_backend.utils.utils import a_capture_prints


async def a_generate_code(quest):
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
        code_execution_config={"executor": autogen.coding.LocalCommandLineCodeExecutor(work_dir="coding")}
    )
    chat_result = await a_capture_prints(
        lambda: user_proxy.a_initiate_chat(
            assistant,
            message=quest,
        )
    )
    return chat_result
