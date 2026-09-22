import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .models import Tag, Task, TaskTag


def task_to_dict(task):
    return {
        "id": task.id,
        "title": task.title,
        "status": task.status,
        "time": task.time.strftime("%Y-%m-%d %H:%M:%S"),
        "tags": [{"id": t.id, "name": t.name} for t in task.tags.all()],
    }

def get_tasks(request):
    tasks = Task.objects.all()

    status = request.GET.get("status")

    if status == "pending":
        tasks = tasks.filter(status="pending")
    elif status == "runs":
        tasks = tasks.filter(status="runs")
    elif status == "done":
        tasks = tasks.filter(status="done")

    if request.GET.get("tags"):
        tasks = tasks.filter(tags__id=request.GET.get("tags"))

    result = [task_to_dict(t) for t in tasks]
    return JsonResponse(result, safe=False)

def get_tags(request):
    tags = Tag.objects.all()
    result = [{"id": t.id, "name": t.name} for t in tags]
    return JsonResponse(result, safe=False)


def get_tag_tasks(request, tag_id):
    tag = Tag.objects.get(id=tag_id)
    tasks = Task.objects.filter(tasktag__tag=tag)
    result = [task_to_dict(t) for t in tasks]
    return JsonResponse(result, safe=False)


@method_decorator(csrf_exempt, name="post")
class TaskAddView(View):
    def post(self, request):
        data = json.loads(request.body)

        title = data.get("title")
        status = data.get("status", "новая")

        task = Task.objects.create(title=title, status=status)

        tag_ids = data.get("tag_ids", [])
        for tag_id in tag_ids:
            tag = Tag.objects.get(id=tag_id)
            TaskTag.objects.create(task=task, tag=tag)

        return JsonResponse(task_to_dict(task), status=201)


@method_decorator(csrf_exempt, name="post")
class TagAddView(View):
    def post(self, request):
        data = json.loads(request.body)
        name = data.get("name")

        tag = Tag.objects.create(name=name)

        return JsonResponse({"id": tag.id, "name": tag.name}, status=201)