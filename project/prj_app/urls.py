from django.urls import path
from . import views

urlpatterns = [
    path("tasks/", views.get_tasks),
    path("tasks/add/", views.TaskAddView.as_view()),

    path("tags/", views.get_tags),
    path("tags/add/", views.TagAddView.as_view()),
    path("tags/<int:tag_id>/tasks/", views.get_tag_tasks),
]