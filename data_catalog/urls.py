from django.urls import path
from .views import ComputationalDPView

urlpatterns = [
    path('create/computational-dp', ComputationalDPView.as_view(), name="create-computational-dp"),
]
