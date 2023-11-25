from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import (TemplateView, FormView)

from chatbot.forms import ChatBotForm


class ChatBotFormView(FormView):
	template_name = 'chatbot/index.html'
	slug_url_kwarg = 'id_thread'

	form_class = ChatBotForm

	id_thread = None

	def setup(self, request, *args, **kwargs):
		super().setup(request, *args, **kwargs)
		self.id_thread = kwargs.get('id_thread', None)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["id_thread"] = kwargs.get('id_thread', None)
		context["messages"] = self.request.session.get('messages', [])
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
		return super().form_valid(form)

	def get_success_url(self):
		if self.id_thread is None:
			return reverse('chatbot:index_no_thread')
		else:
			return reverse('chatbot:index_thread', kwargs={'id_thread': self.id_thread})


class ChatBotCreateView(View):
	template_name = 'chatbot/create.html'

	def post(self, request, *args, **kwargs):
		id_thread = request.POST.get('id_thread', None)
		message = request.POST.get('message', None)
		if not message:
			return render(request, self.template_name)

		if id_thread is not None:
			# create new thread
			...
		else:
			# use old thread
			...

		return render(request, self.template_name)
