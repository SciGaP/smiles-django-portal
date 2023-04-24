from django.urls import re_path
from . import views
from .views import ComputationalDPView, ExperimentalDPView, LiteratureDPView

urlpatterns = [
    re_path(r'^computational-dp/?$', ComputationalDPView.as_view(), name="create-comp-dp"),
    re_path(r"^computational-dp/(?P<dp_id>[^/]+)/$", ComputationalDPView.as_view(), name="get-comp-dp"),
    re_path(r"computational-dp/(?P<dp_id>[^/]+)$", ComputationalDPView.as_view(), name="update-comp-dp"),
    re_path(r"^computational-dp/(?P<dp_id>[^/]+)/$", ComputationalDPView.as_view(), name="delete-comp-dp"),
    re_path(r'computational-dp/upload/?$', ComputationalDPView.as_view(), name="upload-comp-dps"),
    re_path(r"^computational-dps/?$", ComputationalDPView.as_view(), name="get-comp-dps"),

    re_path(r'^experimental-dp/?$', ExperimentalDPView.as_view(), name="create-exp-dp"),
    re_path(r"^experimental-dp/(?P<dp_id>[^/]+)/$", ExperimentalDPView.as_view(), name="get-exp-dp"),
    re_path(r"experimental-dp/(?P<dp_id>[^/]+)$", ExperimentalDPView.as_view(), name="update-exp-dp"),
    re_path(r"^experimental-dp/(?P<dp_id>[^/]+)/$", ExperimentalDPView.as_view(), name="delete-exp-dp"),
    re_path(r'experimental-dp/upload/?$', ExperimentalDPView.as_view(), name="upload-exp-dps"),
    re_path(r"^experimental-dps/?$", ExperimentalDPView.as_view(), name="get-exp-dps"),

    re_path(r'^literature-dp/?$', LiteratureDPView.as_view(), name="create-lit-dp"),
    re_path(r"^literature-dp/(?P<dp_id>[^/]+)/$", LiteratureDPView.as_view(), name="get-lit-dp"),
    re_path(r"literature-dp/(?P<dp_id>[^/]+)$", LiteratureDPView.as_view(), name="update-lit-dp"),
    re_path(r"^literature-dp/(?P<dp_id>[^/]+)/$", LiteratureDPView.as_view(), name="delete-lit-dp"),
    re_path(r'literature-dp/upload/?$', LiteratureDPView.as_view(), name="upload-lit-dps"),
    re_path(r"^literature-dps/?$", LiteratureDPView.as_view(), name="get-lit-dps"),

    re_path('home/', views.home, name='home'),
]
