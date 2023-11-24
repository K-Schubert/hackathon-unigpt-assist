from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView


class ChatBotView(TemplateView):
	template_name = 'chatbot/index.html'
	slug_url_kwarg = 'id_thread'

	id_thread = None

	def setup(self, request, *args, **kwargs):
		super().setup(request, *args, **kwargs)
		self.id_thread = kwargs.get('id_thread', None)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["id_thread"] = kwargs.get('id_thread', None)
		return context

	def get(self, request, *args, **kwargs):
		return render(request, self.template_name)


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
