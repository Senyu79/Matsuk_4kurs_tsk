from django.urls import path
from . import views

urlpatterns = [
    path("tasks/", views.get_tasks),
    path("tasks/add/", views.post_task),
    path("tags/", views.get_tags),
    path("tags/add/", views.post_tag),
    path("tags/<int:tag_id>/tasks/", views.get_tag_tasks),
    path("statuses/", views.get_statuses),
    path("statuses/add/", views.post_status),
]