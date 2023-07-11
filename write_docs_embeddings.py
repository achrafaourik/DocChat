from utils import loaders
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from utils.instructor_embeddings import InstructorEmbeddings
from utils import functions


doc_loaders = loaders.get_all_loaders()
documents = []
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

for loader in doc_loaders:
    documents.extend(text_splitter.split_documents(loader.load()))

embeddings = InstructorEmbeddings().get_embedding_function()
client = functions.get_chroma_client()
vectorstore = Chroma.from_documents(documents, embeddings)
