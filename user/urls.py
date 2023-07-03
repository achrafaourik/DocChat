"""
URL mappings for the user API
"""
from django.urls import path, include
from user import views


app_name = "user"

urlpatterns = [
    path("create/", views.CreateUserView.as_view(), name="create"),
    path("token/", views.CreateTokenView.as_view(), name="token"),
    path('me/', views.ManagerUserView.as_view(), name="me"),
    path('google/', include('oauth2_provider.urls', namespace='oauth2_provider')),

]
