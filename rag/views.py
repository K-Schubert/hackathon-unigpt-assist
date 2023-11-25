from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
# appname/tasks.py

from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from rag.scripts.rag import run_query, qa, labels, llm_routing


@method_decorator(csrf_exempt, name='dispatch')
class RagProcessMessageView(View):

	def post(self, request: WSGIRequest, *args, **kwargs):
		global labels
		id_thread = request.POST.get('id_thread', None)
		message = request.POST.get('message')
		print(message)
		labels.append(llm_routing(message))
		result = run_query(qa, query=message, labels=labels, session_id=id_thread)
		print(result)

		answer = result["answer"] + "\n\n" + "Source documents:\n- " + "\n- ".join(result["source_documents"] if result["source_documents"] else [])

		return JsonResponse({
			"answer": result["answer"],
			"id_thread": str(result["session_id"]),
		})
