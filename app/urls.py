
from django.urls import path
from .views import chatbot,ChatMessage,chat_history_view,chat_history_api


urlpatterns = [
    path("chat/", chatbot, name="chatbot"),
    path("chat_history/", chat_history_view, name="chathistory"),
    path("chat_history_api/", chat_history_api, name="chat_history_api"),
    
]
