import logging
import os
from typing import Dict

from langchain.prompts.prompt import PromptTemplate
from langchain_openai import AzureChatOpenAI

from iipa_backend.config.config import (
    OPENAI_MODEL_NAME,
    OPENAI_TEMPERATURE,
    OPENAI_API_TYPE,
    OPENAI_API_VERSION,
    OPENAI_DEPLOYMENT_NAME,
    OPENAI_TOP_P,
    OPENAI_SEED,
    CODE_PATTERN,
    INDICES,
    STATEMENT_LABEL_PATTERNS,
    STATEMENT_LABEL_TEMPLATE,
    INDICES_LABEL2DOC,
    METADATA_SEPARATOR,
    DEFAULT_METADATA_TMPL,
    DEFAULT_TEXT_NODE_TMPL,
    INDEX_QUERY_PROMPT_TEMPLATE,
    LATEX_DEFS,
)
from iipa_backend.models.prompt import PromptAnswer


logger = logging.getLogger(__name__)


def create_azure_openai_client():
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
    return client


async def a_openai_quest_prompt_template(prompt_template: PromptTemplate, template_variables: Dict = {}):
    client = create_azure_openai_client()
    chain = prompt_template | client
    chain_results = await chain.ainvoke(template_variables)
    result_text = chain_results.content
    return result_text


async def a_openai_quest(prompt: str):
    client = create_azure_openai_client()
    messages = [
        ('system', 'You are an helpful assistant.'),
        ('user', prompt)
    ]
    results = await client.ainvoke(messages)
    result_text = results.content
    return result_text


async def llm_quest(prompt: str, extract_code: bool = False):
    logger.debug(f'Requesting the LLM with this prompt:\n{prompt}')
    llm_ans = await a_openai_quest(prompt)
    logger.debug(f'LLM responded with this answer:\n{llm_ans}')
    llm_ans_post_processed = post_process_llm_ans(llm_ans, extract_code)
    logger.debug(f'Returning this post-processed LLM answer:\n{llm_ans_post_processed}')
    return llm_ans_post_processed


async def _index_aquest_with_statement_rag(
        query: str, kb_label: str,
        statement_patterns = STATEMENT_LABEL_PATTERNS,
        statement_label_template = STATEMENT_LABEL_TEMPLATE,
        indices_label2doc = INDICES_LABEL2DOC,
        metadata_separator = METADATA_SEPARATOR,
        metadata_template = DEFAULT_METADATA_TMPL,
        text_node_template = DEFAULT_TEXT_NODE_TMPL,
        index_query_prompt_template = INDEX_QUERY_PROMPT_TEMPLATE,
        include_latex_macros = True,
    ):
    index = INDICES.get(kb_label)
    if not index:
        return f"ERROR: could not find KB '{kb_label}'"                   # TODO: handle more properly
    vector_retriever = index.as_retriever()
    retrieved_nodes = vector_retriever.retrieve(query)
    statement_labels = [n.metadata['Statement label'] for n in retrieved_nodes]  # TODO: support non-statements (but give warning?)
    for statement_type, statement_pattern in statement_patterns.items():
        matches = statement_pattern.findall(query)
        for _, statement_type_nr in matches:
            statement_label = statement_label_template.format(
                statement_type=statement_type,
                statement_type_nr=statement_type_nr,
            )
            if statement_label not in statement_labels:
                statement_labels.append(statement_label)
    context_strs = []
    for statement_label in statement_labels:
        doc = indices_label2doc[kb_label][statement_label]
        metadata_str = metadata_separator.join([
            metadata_template.format(
                key=key,
                value=value,
            ) for key, value in doc['metadata'].items()
        ])
        context_str = text_node_template.format(
            metadata_str=metadata_str,
            content=doc['text'],
        )
        context_strs.append(context_str)
    context_str = "\n\n".join(context_strs)
    prompt = index_query_prompt_template.format(
        context_str=context_str,
        query_str=query
    )
    response = await llm_quest(prompt)
    prompt_answer = PromptAnswer(answer=response)
    if include_latex_macros:
        statement_label2latex_defs = LATEX_DEFS.get(kb_label, {})
        for statement_label in statement_labels:
            statement_latex_defs = statement_label2latex_defs.get(statement_label, {})
            statement_latex_macros = statement_latex_defs.get('macros', {})
            prompt_answer.latex_macros.update(statement_latex_macros)
    return prompt_answer


async def _index_aquest(query: str, kb_label: str):
    index = INDICES.get(kb_label)
    if index:
        query_engine = index.as_query_engine()
        response = await query_engine.aquery(query).response
    else:
        response = f"ERROR: could not find KB '{kb_label}'"                   # TODO: handle more properly
    return response


async def kb_quest(prompt: str, kb_label: str, extract_code: bool = False,
                   extra_statement_rag: bool = True):
    logger.debug(f"Requesting KB '{kb_label}' with this prompt:\n{prompt}")
    if extra_statement_rag:
        llm_ans = await _index_aquest_with_statement_rag(prompt, kb_label)
    else:
        llm_ans = await _index_aquest(prompt, kb_label, extra_statement_rag)
    logger.debug(f'KB responded with this answer:\n{llm_ans}')
    llm_ans_post_processed = post_process_llm_ans(llm_ans, extract_code)
    logger.debug(f'Returning this post-processed KB answer:\n{llm_ans_post_processed}')
    return llm_ans_post_processed


def extract_llm_ans_code(llm_ans, code_pattern=CODE_PATTERN):
    logger.debug(f'Extracting code from this LLM answer:\n{llm_ans}')
    matches = code_pattern.findall(llm_ans)
    code = matches[0] if matches else llm_ans
    return code


def post_process_llm_ans(llm_ans: str, extract_code: bool = False):
    if extract_code:
        llm_ans = extract_llm_ans_code(llm_ans)
    return llm_ans
