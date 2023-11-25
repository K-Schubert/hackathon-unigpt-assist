from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
# appname/tasks.py

from celery import shared_task
import requests
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from rag.scripts.rag import run_query, qa


# @method_decorator(csrf_exempt, name='dispatch')
class RagProcessMessageView(View):

	def post(self, request: WSGIRequest, *args, **kwargs):
		id_thread = request.POST.get('id_thread', None)
		message = request.POST.get('message')
		result = run_query(qa, query=message, session_id=id_thread)
		print(result)
		return JsonResponse({
			"answer": result["answer"],
			"id_thread": str(result["session_id"]),
		})
