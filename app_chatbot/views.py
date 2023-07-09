from rest_framework.views import APIView
from rest_framework.response import Response
from utils import functions
import os
from utils.huggingface_pipeline import HuggingFaceModel
from utils.instructor_embeddings import InstructorEmbeddings
from langchain.vectorstores import Chroma
from langchain.llms import OpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory



class OpenAIView(APIView):

    def post(self, request):
        client = functions.get_chroma_client()
        vectorstore = Chroma(client=client, collection_name="docs_embeddings")
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
        print('-' * 80)
        # Load models
        load_models()

        # # retrieve the user email from the incoming request
        email = "user@mail.com"

        # get the body data from the request
        data = request.data
        text = data['message']

        related_history = functions.get_related_history(email, text)

        # get the last n conversations
        past_conversations = functions.return_last_n_interactions(email,
                                                                  int(os.environ.get('N_RELATED_INTERACTIONS')))
        print(f'past conversations of the client : \n{past_conversations}')

        # instantiate the model class and perform the prediction
        model = HuggingFaceModel()
        answer = model.predict(related_history, past_conversations, text)['answer']
        print(f"bot's answer: \n{answer}")

        # write the current interaction to ChromaDB
        current_interaction = "\n".join([f'USER: {text}', f'ASSISTANT: {answer}'])
        functions.write_current_interaction(email, current_interaction)

        return Response({'answer': answer})


class DeleteHistoryView(APIView):

    def post(self, request):
        # # retrieve the user email from the incoming request
        email = "user@mail.com"

        functions.delete_past_history(email)

        return Response({'message': 'History deleted successfully'})
