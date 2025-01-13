from django.urls import path
from .views import PromptView

urlpatterns = [
    path('prompt/', PromptView.as_view(), name='prompt'),
    path('prompt/<str:pk>/', PromptView.as_view(), name='prompt-delete'),
]
