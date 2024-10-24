from dotenv import load_dotenv
import os
from llama_index.core import (
    Document,
    load_index_from_storage,
    Settings,
    StorageContext,
    VectorStoreIndex,
)
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from llama_index.llms.azure_openai import AzureOpenAI


load_dotenv()


PERSIST_DIR = os.path.join(os.path.dirname(__file__), 'test_persist_index')


llm = AzureOpenAI(
    model=os.getenv('MODEL_NAME'),
    deployment_name=os.getenv('DEPLOYMENT_NAME'),
    api_key=os.getenv('OPENAI_API_KEY'),
    azure_endpoint=os.getenv('AZURE_ENDPOINT'),
    api_version=os.getenv('OPENAI_API_VERSION'),
)
embed_model = AzureOpenAIEmbedding(
    model=os.getenv('EMBEDDING_MODEL'),
    deployment_name=os.getenv('EMBEDDING_DEPLOYMENT'),
    api_key=os.getenv('OPENAI_API_KEY'),
    azure_endpoint=os.getenv('AZURE_ENDPOINT'),
    api_version=os.getenv('OPENAI_API_VERSION'),
)
Settings.llm = llm
Settings.embed_model = embed_model

print(embed_model)
print(llm)

d1 = Document(text='The pin code for the entrance is 9191', metadata={})
documents = [d1]

index = VectorStoreIndex.from_documents(documents)#, embed_model=embed_model, llm=llm)
index.as_query_engine()

index.storage_context.persist(persist_dir=PERSIST_DIR)

storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
index = load_index_from_storage(storage_context)

# # Insert new documents
# for doc in documents:
#     vector_index.insert(doc)

query_engine = index.as_query_engine()
response = query_engine.query(
    "What is the PIN code for comming in?"
)
print(response)
