from django.urls import path
from . import views

urlpatterns = [path("verifier/", views.VerifierViews.as_view())]
