from utils import loaders
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from utils.instructor_embeddings import InstructorEmbeddings
from utils import functions


doc_loaders = loaders.get_all_loaders()
docs = []
for loader in doc_loaders:
    docs.extend(loader.load())
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
documents = text_splitter.split_documents(docs)

embeddings = InstructorEmbeddings().get_embedding_function()
client = functions.get_chroma_client()
vectorstore = Chroma(client=client, collection_name="docs_embeddings").from_documents(documents, embeddings)
