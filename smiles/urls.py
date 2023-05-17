from django.urls import re_path
from . import views
from .views import ComputationalDPView, ExperimentalDPView, LiteratureDPView

urlpatterns = [
    re_path('home/', views.home, name='home'),

    re_path(r'^comp-dp/?$', ComputationalDPView, name="create-comp-dp"),
    re_path(r"^comp-dp/(?P<dp_id>[^/]+)/$", ComputationalDPView, name="get-comp-dp"),
    re_path(r"comp-dp/(?P<dp_id>[^/]+)$", ComputationalDPView, name="update-comp-dp"),
    re_path(r"^comp-dp/(?P<dp_id>[^/]+)/$", ComputationalDPView, name="delete-comp-dp"),
    re_path(r'comp-dp/upload/?$', ComputationalDPView, name="upload-comp-dps"),
    re_path(r"^comp-dps/?$", ComputationalDPView, name="get-comp-dps"),

    re_path(r'^exp-dp/?$', ExperimentalDPView, name="create-exp-dp"),
    re_path(r"^exp-dp/(?P<dp_id>[^/]+)/$", ExperimentalDPView, name="get-exp-dp"),
    re_path(r"exp-dp/(?P<dp_id>[^/]+)$", ExperimentalDPView, name="update-exp-dp"),
    re_path(r"^exp-dp/(?P<dp_id>[^/]+)/$", ExperimentalDPView, name="delete-exp-dp"),
    re_path(r'exp-dp/upload/?$', ExperimentalDPView, name="upload-exp-dps"),
    re_path(r"^exp-dps/?$", ExperimentalDPView, name="get-exp-dps"),

    re_path(r'^lit-dp/?$', LiteratureDPView, name="create-lit-dp"),
    re_path(r"^lit-dp/(?P<dp_id>[^/]+)/$", LiteratureDPView, name="get-lit-dp"),
    re_path(r"lit-dp/(?P<dp_id>[^/]+)$", LiteratureDPView, name="update-lit-dp"),
    re_path(r"^lit-dp/(?P<dp_id>[^/]+)/$", LiteratureDPView, name="delete-lit-dp"),
    re_path(r'lit-dp/upload/?$', LiteratureDPView, name="upload-lit-dps"),
    re_path(r"^lit-dps/?$", LiteratureDPView, name="get-lit-dps"),
]
