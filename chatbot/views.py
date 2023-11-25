import uuid

import requests
from django.middleware.csrf import get_token
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.http import JsonResponse
from celery.result import AsyncResult
from django.views.generic import (TemplateView, FormView)

from chatbot.forms import ChatBotForm
from rag.scripts.rag import chat_history_map


class ChatBotFormView(FormView):
	template_name = 'chatbot/index.html'
	slug_url_kwarg = 'id_thread'

	form_class = ChatBotForm

	id_thread = None

	def setup(self, request, *args, **kwargs):
		super().setup(request, *args, **kwargs)
		self.id_thread = str(kwargs.get('id_thread', None))
		try:
			if uuid.UUID(self.id_thread) not in chat_history_map:
				self.id_thread = None
		except:
			self.id_thread = None

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["id_thread"] = kwargs.get('id_thread', None)
		context["messages"] = self.request.session.get('messages', [])
		context["history"] = self.request.session.get('history', list(str(key) for key in chat_history_map.keys()))
		return context

	def post(self, request, *args, **kwargs):
		form = self.get_form()
		messages = self.request.session.get('messages', [])
		if not form.is_valid() or (len(messages) > 0 and messages[-1]['answer'] is None):
			return self.form_invalid(form)
		else:
			return self.form_valid(form)

	def form_valid(self, form):
		message = form.cleaned_data.get('message')
		messages = self.request.session.get('messages', [])
		messages.append({"question": message, "answer": None})
		self.request.session['messages'] = messages

		response = requests.post(
			url=f"http://localhost:{self.request.META['SERVER_PORT']}/rag/",
			data={
				"id_thread": self.id_thread,
				"message": message,
			})

		result = response.json()

		messages[-1]['answer'] = result['answer']

		self.id_thread = str(result.get('id_thread', None))

		self.request.session["history"] = self.request.session.get('history', list(str(key) for key in chat_history_map.keys()))
		return super().form_valid(form)

	def get_success_url(self):
		if self.id_thread is None:
			return reverse('chatbot:index_no_thread')
		else:
			return reverse('chatbot:index_thread', kwargs={'id_thread': self.id_thread})


def task_status(request, task_id):
	task_result = AsyncResult(task_id)
	if task_result.ready():
		return JsonResponse({'status': 'complete', 'result': task_result.get()})
	else:
		return JsonResponse({'status': 'pending'})
