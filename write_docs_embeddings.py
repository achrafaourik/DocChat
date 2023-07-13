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

client = functions.get_chroma_client()

instructor_ef = InstructorEmbeddings().get_embedding_function()
collection = client.get_or_create_collection(name="docs_embeddings",
                                             embedding_function=instructor_ef)
collection.delete()


collection.add(
        documents=documents,
        ids=[functions.generate_unique_id() for _ in range(len(documents))])
