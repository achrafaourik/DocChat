from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
import json
from utils import functions
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
import os
from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
import numpy as np
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from django.views import View
from core.models import Item
from django.forms.models import model_to_dict
from utils.huggingface_pipeline import HuggingFaceModel
from utils.instructor_embeddings import InstructorEmbeddings
from utils.emotion_pipeline import EmotionClassifier
from utils.nsfw_classifier import NSFWClassifier



def load_models():
    # Create an instance of HuggingFaceModel
    huggingface_model = HuggingFaceModel()
    instructor_model = InstructorEmbeddings()
    emotion_model = EmotionClassifier()
    nsfw_model = NSFWClassifier()

    # Run the 'load' method
    huggingface_model.load()
    instructor_model.load()
    emotion_model.load()
    nsfw_model.load()


class LoadModelsView(APIView):
    def get(self, request):
        load_models()
        return Response({'message': 'Models successfully loaded'})



class ChatbotView(APIView):
    # authentication_classes = [authentication.TokenAuthentication, OAuth2Authentication]
    # permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        print('-' * 80)
        # Load models
        load_models()

        # # retrieve the user email from the incoming request
        user = request.user
        email = user.email

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
    authentication_classes = [authentication.TokenAuthentication, OAuth2Authentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        # # retrieve the user email from the incoming request
        user = request.user
        email = user.email

        functions.delete_past_history(email)

        return Response({'message': 'History deleted successfully'})
