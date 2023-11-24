from django.urls import path

from chatbot.views import (ChatBotFormView, ChatBotCreateView)

urlpatterns = [
	path('', ChatBotFormView.as_view(), name='index_no_thread'),
	path('<int:id_thread>', ChatBotFormView.as_view(), name='index_thread'),
	path('create/<int:id_thread>', ChatBotCreateView.as_view(), name='create'),
]
