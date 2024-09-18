
from django.urls import path
from chatbot.views import chatbot_response,chatbot_page

urlpatterns = [
    path('', chatbot_page, name='chatbot_page'),
    path('response/', chatbot_response, name='chatbot_response'),
]
