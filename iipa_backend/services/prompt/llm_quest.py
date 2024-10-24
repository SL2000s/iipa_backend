import logging
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
    CODE_PATTERN,
    INDICES,
)


logger = logging.getLogger(__name__)


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


async def llm_quest(prompt: str, extract_code: bool = False):
    logger.debug(f'Requesting the LLM with this prompt:\n{prompt}')
    prompt_template = PromptTemplate.from_template(
        prompt,
        template_format=PROMPT_TEMPLATE_FORMAT,
    )
    llm_ans = await openai_quest(prompt_template)
    logger.debug(f'LLM responded with this answer:\n{llm_ans}')
    llm_ans_post_processed = post_process_llm_ans(llm_ans, extract_code)
    logger.debug(f'Returning this post-processed LLM answer:\n{llm_ans_post_processed}')
    return llm_ans_post_processed


async def _index_quest(query: str, kb_label: str):
    index = INDICES.get(kb_label)
    if index:
        query_engine = index.as_query_engine()
        response = query_engine.query(query).response
    else:
        response = f"ERROR: could not find KB '{kb_label}'"                   # TODO: handle more properly
    return response



async def kb_quest(prompt: str, kb_label: str, extract_code: bool = False):
    logger.debug(f"Requesting KB '{kb_label}' with this prompt:\n{prompt}")
    llm_ans = await _index_quest(prompt, kb_label)
    logger.debug(f'KB responded with this answer:\n{llm_ans}')
    llm_ans_post_processed = post_process_llm_ans(llm_ans, extract_code)
    logger.debug(f'Returning this post-processed KB answer:\n{llm_ans_post_processed}')
    return llm_ans_post_processed


def extract_llm_ans_code(llm_ans, code_pattern=CODE_PATTERN):
    logger.debug(f'JSON post-processing this LLM answer:\n{llm_ans}')
    matches = code_pattern.findall(llm_ans)
    code = matches[0] if matches else llm_ans
    return code


def post_process_llm_ans(llm_ans: str, extract_code: bool = False):
    if extract_code:
        llm_ans = extract_llm_ans_code(llm_ans)
    return llm_ans


if __name__ == '__main__':              # TODO: remove
    from dotenv import load_dotenv
    load_dotenv()
    import asyncio
    ans = asyncio.run(llm_quest('What is 1+1?'))
    print(ans)
