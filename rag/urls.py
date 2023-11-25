from django.urls import path

from .views import (RagProcessMessageView)

urlpatterns = [
	path('', RagProcessMessageView.as_view(), name='launch_task'),
]
