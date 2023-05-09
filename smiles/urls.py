from django.urls import re_path
from . import views
from .views import ComputationalDPView, ExperimentalDPView, LiteratureDPView

urlpatterns = [
    re_path(r'^comp-dp/?$', ComputationalDPView.as_view(), name="create-comp-dp"),
    re_path(r"^comp-dp/(?P<dp_id>[^/]+)/$", ComputationalDPView.as_view(), name="get-comp-dp"),
    re_path(r"comp-dp/(?P<dp_id>[^/]+)$", ComputationalDPView.as_view(), name="update-comp-dp"),
    re_path(r"^comp-dp/(?P<dp_id>[^/]+)/$", ComputationalDPView.as_view(), name="delete-comp-dp"),
    re_path(r'comp-dp/upload/?$', ComputationalDPView.as_view(), name="upload-comp-dps"),
    re_path(r"^comp-dps/?$", ComputationalDPView.as_view(), name="get-comp-dps"),

    re_path(r'^exp-dp/?$', ExperimentalDPView.as_view(), name="create-exp-dp"),
    re_path(r"^exp-dp/(?P<dp_id>[^/]+)/$", ExperimentalDPView.as_view(), name="get-exp-dp"),
    re_path(r"exp-dp/(?P<dp_id>[^/]+)$", ExperimentalDPView.as_view(), name="update-exp-dp"),
    re_path(r"^exp-dp/(?P<dp_id>[^/]+)/$", ExperimentalDPView.as_view(), name="delete-exp-dp"),
    re_path(r'exp-dp/upload/?$', ExperimentalDPView.as_view(), name="upload-exp-dps"),
    re_path(r"^exp-dps/?$", ExperimentalDPView.as_view(), name="get-exp-dps"),

    re_path(r'^lit-dp/?$', LiteratureDPView.as_view(), name="create-lit-dp"),
    re_path(r"^lit-dp/(?P<dp_id>[^/]+)/$", LiteratureDPView.as_view(), name="get-lit-dp"),
    re_path(r"lit-dp/(?P<dp_id>[^/]+)$", LiteratureDPView.as_view(), name="update-lit-dp"),
    re_path(r"^lit-dp/(?P<dp_id>[^/]+)/$", LiteratureDPView.as_view(), name="delete-lit-dp"),
    re_path(r'lit-dp/upload/?$', LiteratureDPView.as_view(), name="upload-lit-dps"),
    re_path(r"^lit-dps/?$", LiteratureDPView.as_view(), name="get-lit-dps"),

    re_path('home/', views.home, name='home'),
]
