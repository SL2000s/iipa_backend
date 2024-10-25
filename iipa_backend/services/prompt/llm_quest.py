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



def mentioned_statements(test: str):
    pass


# statement_pattern_strs = {
#     'Theorem': r'\b(Theorem|theorem|Thm|thm|Thm\.|thm\.)\s*(\d+)\b',
#     'Definition': r'\b(Definition|definition|Def|def|Def\.|def\.)\s*(\d+)\b',
#     'Axiom': r'\b(Axiom|axiom)\s*(\d+)\b',
#     'Corollary': r'\b(Corollary|corollary|Cor|cor|Cor\.|cor\.)\s*(\d+)\b',
#     'Lemma': r'\b(Lemma|lemma)\s*(\d+)\b',
# }
# import re
# statement_patterns = {s: re.compile(p) for s, p in statement_pattern_strs.items()}
# statement_label_template = '{statement_type} {statement_type_nr}'
# DEFAULT_TEXT_NODE_TMPL = '{metadata_str}\n\n{content}'      # Same as from llamaindex.core.schema
# DEFAULT_METADATA_TMPL = '{key}: {value}'                    # Same as from llamaindex.core.schema
# METADATA_SEPARATOR = '\n'
# from llama_index.core.schema import MetadataMode
# INDEX_QUERY_PROMPT_TEMPLATE_STR = (
#     "Context information is below.\n"
#     "---------------------\n"
#     "{context_str}\n"
#     "---------------------\n"
#     "Given the context information and not prior knowledge, "
#     "answer the query.\n"
#     "Query: {query_str}\n"
#     "Answer: "
# )  # from llamaindex
# async def _index_aquest_with_statement_rag(query: str, kb_label: str):
#     print('HERE!!!', query)
#     input()
#     index = INDICES.get(kb_label)
#     if not index:
#         return f"ERROR: could not find KB '{kb_label}'"                   # TODO: handle more properly

#     vector_retriever = index.as_retriever()
#     retrieved_nodes = vector_retriever.retrieve(query)
#     node_ids = set([n.id_ for n in retrieved_nodes])
#     for statement_type, statement_pattern in statement_patterns.items():
#         matches = statement_pattern.findall(query)
#         for _, statement_type_nr in matches:
#             print('Match', matches)
#             input()
#             statement_label = statement_label_template.format(
#                 statement_type=statement_type,
#                 statement_type_nr=statement_type_nr,
#             )
#             nodes = vector_retriever.retrieve(statement_label)
#             print(123, nodes)
#             input()
#             for node in nodes:
#                 if node.id_ not in node_ids:
#                     node_ids.add(node.id_)
#                     retrieved_nodes.append(node)
#     print('Done')
#     input()
#     context_str = "\n\n".join([n.get_content(metadata_mode=MetadataMode.LLM) for n in nodes])
#     prompt = INDEX_QUERY_PROMPT_TEMPLATE_STR.format(
#         context_str=context_str,
#         query_str=query
#     )
#     response = await llm_quest(prompt)
#     return response




statement_pattern_strs = {
    'Theorem': r'\b(Theorem|theorem|Thm|thm|Thm\.|thm\.)\s*(\d+)\b',
    'Definition': r'\b(Definition|definition|Def|def|Def\.|def\.)\s*(\d+)\b',
    'Axiom': r'\b(Axiom|axiom)\s*(\d+)\b',
    'Corollary': r'\b(Corollary|corollary|Cor|cor|Cor\.|cor\.)\s*(\d+)\b',
    'Lemma': r'\b(Lemma|lemma)\s*(\d+)\b',
}
import re
statement_patterns = {s: re.compile(p) for s, p in statement_pattern_strs.items()}
statement_label_template = '{statement_type} {statement_type_nr}'
DEFAULT_TEXT_NODE_TMPL = '{metadata_str}\n\n{content}'      # Same as from llamaindex.core.schema
DEFAULT_METADATA_TMPL = '{key}: {value}'                    # Same as from llamaindex.core.schema
METADATA_SEPARATOR = '\n'
from llama_index.core.schema import MetadataMode
LM_THEORY_INDEX_JSON_PATH = os.getenv('LM_THEORY_INDEX_JSON_PATH')  # TODO: move to config
import json
with open(LM_THEORY_INDEX_JSON_PATH, 'r') as f:
    LM_THEORY_INDEX_DICT = json.load(f)
LABEL2DOC = {d['metadata']['Statement label']: d for d in LM_THEORY_INDEX_DICT}
INDEX_QUERY_PROMPT_TEMPLATE_STR = (
    "Context information is below.\n"
    "---------------------\n"
    "{context_str}\n"
    "---------------------\n"
    "Given the context information and not prior knowledge, "
    "answer the query.\n"
    "Query: {query_str}\n"
    "Answer: "
)  # from llamaindex
async def _index_aquest_with_statement_rag(query: str, kb_label: str):
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
        doc = LABEL2DOC[statement_label]
        metadata_str = METADATA_SEPARATOR.join([
            DEFAULT_METADATA_TMPL.format(
                key=key,
                value=value,
            ) for key, value in doc['metadata'].items()
        ])
        context_str = DEFAULT_TEXT_NODE_TMPL.format(
            metadata_str=metadata_str,
            content=doc['text'],
        )
        context_strs.append(context_str)
    context_str = "\n\n".join(context_strs)
    print(context_str)
    prompt = INDEX_QUERY_PROMPT_TEMPLATE_STR.format(
        context_str=context_str,
        query_str=query
    )
    response = await llm_quest(prompt)
    return response


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
    # ans = asyncio.run(llm_quest('What is 1+1?'))
    ans = asyncio.run(kb_quest('What does Theorem 1 say?', 'lm_theory'))
    print(ans)
