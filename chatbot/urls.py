from django.urls import path

from chatbot.views import (ChatBotView, ChatBotCreateView)

urlpatterns = [
	path('', ChatBotView.as_view(), name='list'),
	path('create/<int:id_thread>', ChatBotCreateView.as_view(), name='create'),
]
