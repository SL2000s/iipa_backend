import os
from typing import Dict

from langchain.prompts.prompt import PromptTemplate
from langchain_openai import AzureChatOpenAI

from iipa_backend.config.config import (
    PROMPT_TEMPLATE_FORMAT,
    OPENAI_MODEL_NAME,
    OPENAI_TEMPERATURE,
    OPENAI_API_TYPE,
    OPENAI_API_VERSION,
    OPENAI_DEPLOYMENT_NAME,
    OPENAI_TOP_P,
    OPENAI_SEED,
)


async def openai_quest(prompt_template: PromptTemplate, template_variables: Dict = {}):
    client = AzureChatOpenAI(
        model_name=OPENAI_MODEL_NAME,
        temperature=OPENAI_TEMPERATURE,
        openai_api_type=OPENAI_API_TYPE,
        openai_api_version=OPENAI_API_VERSION,
        deployment_name=OPENAI_DEPLOYMENT_NAME,
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        azure_endpoint=os.getenv("AZURE_ENDPOINT"),
        top_p=OPENAI_TOP_P,
        seed=OPENAI_SEED,
    )
    chain = prompt_template | client
    chain_results = await chain.ainvoke(template_variables)
    result_text = chain_results.content
    return result_text


async def llm_quest(prompt: str):
    prompt_template = PromptTemplate.from_template(
        prompt,
        template_format=PROMPT_TEMPLATE_FORMAT,
    )
    llm_ans = await openai_quest(prompt_template)
    return llm_ans


if __name__ == '__main__':              # TODO: remove
    from dotenv import load_dotenv
    load_dotenv()
    import asyncio
    ans = asyncio.run(llm_quest('What is 1+1?'))
    print(ans)