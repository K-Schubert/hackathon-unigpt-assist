from django.urls import path

from chatbot.views import (ChatBotFormView)

urlpatterns = [
	path('', ChatBotFormView.as_view(), name='index_no_thread'),
	path('<str:id_thread>', ChatBotFormView.as_view(), name='index_thread'),
]
