from django.urls import path
from . import views

urlpatterns = [
    path('hf/', views.ChatbotView.as_view(), name="huggingface"),
    path('load/', views.LoadModelsView.as_view(), name='load'),
    path('openai/', views.OpenAIView.as_view(), name="openai"),
]
