from django.urls import path
from .views import ComputationalDPView

urlpatterns = [
    path('computational-dp', ComputationalDPView.as_view(), name="create-computational-dp"),
    path('computational-dp/<str:dp_id>', ComputationalDPView.as_view(), name="get-computational-dp"),
    path('computational-dp/<str:dp_id>', ComputationalDPView.as_view(), name="put-computational-dp"),
    path('computational-dp/<str:dp_id>', ComputationalDPView.as_view(), name="delete-computational-dp"),
]
