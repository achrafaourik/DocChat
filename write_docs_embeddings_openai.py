from utils import loaders
from langchain.text_splitter import CharacterTextSplitter
from utils import functions
from dotenv import load_dotenv; load_dotenv('.env')
from chromadb.utils import embedding_functions
import os


doc_loaders = loaders.get_all_loaders()
documents = []
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

for loader in doc_loaders:
    documents.extend(text_splitter.split_documents(loader.load()))

client = functions.get_chroma_client()

openai_ef = embedding_functions.OpenAIEmbeddingFunction(
                api_key=os.environ.get('OPENAI_API_KEY'),
                model_name="text-embedding-ada-002"
            )
client.delete_collection('docs_embeddings_openai')
collection = client.get_or_create_collection(name="docs_embeddings_openai",
                                             embedding_function=openai_ef)

docs = [x.page_content for x in documents]
collection.add(
        documents=docs,
        ids=[functions.generate_unique_id() for _ in range(len(docs))])
