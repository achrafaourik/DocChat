from rest_framework.views import APIView
from rest_framework.response import Response
from utils import functions
import os
from utils.huggingface_pipeline import HuggingFaceModel
from utils.langchain_embeddings import InstructorEmbeddings
from langchain.vectorstores import Chroma
from langchain.llms import OpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.embeddings.openai import OpenAIEmbeddings




class OpenAIView(APIView):

    def post(self, request):
        client = functions.get_chroma_client()
        embeddings = OpenAIEmbeddings()
        vectorstore = Chroma(client=client,
                             collection_name="docs_embeddings_openai",
                             embedding_function=embeddings)

        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        qa = ConversationalRetrievalChain.from_llm(OpenAI(temperature=0),
                                                   vectorstore.as_retriever(),
                                                   memory=memory,
                                                   return_source_documents=True)


        # get the body data from the request
        data = request.data
        query = data['message']

        result = qa({"question": query})['answer']

        return Response({'answer': result})


def load_models():
    # Create an instance of HuggingFaceModel
    huggingface_model = HuggingFaceModel()
    instructor_model = InstructorEmbeddings()

    # Run the 'load' method
    huggingface_model.load()
    instructor_model.load()


class LoadModelsView(APIView):
    def get(self, request):
        load_models()
        return Response({'message': 'Models successfully loaded'})



class ChatbotView(APIView):

    def post(self, request):
        load_models()
        client = functions.get_chroma_client()
        embeddings = InstructorEmbeddings()
        vectorstore = Chroma(client=client,
                             collection_name="docs_embeddings_local",
                             embedding_function=embeddings)

        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        qa = ConversationalRetrievalChain.from_llm(HuggingFaceModel.get_llm(),
                                                   vectorstore.as_retriever(),
                                                   memory=memory,
                                                   return_source_documents=True)


        # get the body data from the request
        data = request.data
        query = data['message']

        result = qa({"question": query})['answer']

        return Response({'answer': result})
