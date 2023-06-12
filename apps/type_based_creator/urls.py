"""
URL configuration for type_based_creator project.
"""
import django

from . import views

urlpatterns = [django.urls.path("table/", views.TableView.as_view())]
