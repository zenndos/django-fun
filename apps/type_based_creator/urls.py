"""
URL configuration for type_based_creator project.
"""
import django

from . import views

urlpatterns = [
    django.urls.path("table", views.TableView.as_view()),
    django.urls.path("table/<int:id>", views.TableView.as_view()),
    django.urls.path("table/<int:id>/row", views.RowView.as_view()),
    django.urls.path("table/<int:id>/rows", views.RowsView.as_view()),
    django.urls.path("cool-table", views.TableView.as_view()),
    django.urls.path("cool-table/<int:id>", views.TableView.as_view()),
]
