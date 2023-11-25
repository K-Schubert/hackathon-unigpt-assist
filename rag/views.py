from django.shortcuts import render

# Create your views here.
# appname/tasks.py

from celery import shared_task
import requests


@shared_task
def fetch_and_process_data(api_url):
	response = requests.get(api_url)
	data = response.json()

	# Process the data
	processed_data = process_data(data)

	return processed_data


def process_data(data):
	# Dummy function for processing data
	return {"processed": True, "original_data": data}


# appname/views.py

from django.http import JsonResponse
from .tasks import fetch_and_process_data


def trigger_data_processing(request):
	api_url = "https://api.example.com/data"
	fetch_and_process_data.delay(api_url)
	return JsonResponse({"status": "Processing started"})


# Trigger the task and get task ID
task = fetch_and_process_data.delay(api_url)
task_id = task.id

# Later, you can retrieve the result using the task ID
from celery.result import AsyncResult

task_result = AsyncResult(task_id).get()

from celery import chain

task_chain = chain(fetch_and_process_data.s(api_url), another_task.s())
task_chain()
