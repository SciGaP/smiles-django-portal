from django.urls import path
from .views import ComputationalDPView, ExperimentalDPView, LiteratureDPView

urlpatterns = [
    path('computational-dp', ComputationalDPView.as_view(), name="create-computational-dp"),
    path('computational-dp/<str:dp_id>', ComputationalDPView.as_view(), name="get-computational-dp"),
    path('computational-dp/<str:dp_id>', ComputationalDPView.as_view(), name="put-computational-dp"),
    path('computational-dp/<str:dp_id>', ComputationalDPView.as_view(), name="delete-computational-dp"),
    path(ComputationalDPView.UPLOAD_URL, ComputationalDPView.as_view(), name="upload-computational-dps"),

    path('experimental-dp', ExperimentalDPView.as_view(), name="create-experimental-dp"),
    path('experimental-dp/<str:dp_id>', ExperimentalDPView.as_view(), name="get-experimental-dp"),
    path('experimental-dp/<str:dp_id>', ExperimentalDPView.as_view(), name="put-experimental-dp"),
    path('experimental-dp/<str:dp_id>', ExperimentalDPView.as_view(), name="delete-experimental-dp"),
    path(ExperimentalDPView.UPLOAD_URL, ExperimentalDPView.as_view(), name="upload-experimental-dps"),

    path('literature-dp', LiteratureDPView.as_view(), name="create-literature-dp"),
    path('literature-dp/<str:dp_id>', LiteratureDPView.as_view(), name="get-literature-dp"),
    path('literature-dp/<str:dp_id>', LiteratureDPView.as_view(), name="put-literature-dp"),
    path('literature-dp/<str:dp_id>', LiteratureDPView.as_view(), name="delete-literature-dp"),
    path(LiteratureDPView.UPLOAD_URL, LiteratureDPView.as_view(), name="upload-literature-dps")
]
