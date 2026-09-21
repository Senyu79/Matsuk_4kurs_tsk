import json

from django.http import JsonResponse

from .models import Status, Tag, Task, TaskTag


def task_to_dict(task):
    return {
        "id": task.id,
        "title": task.title,
        "status_id": task.status_id,
        "status_name": task.status.name,
        "time": task.time.strftime("%Y-%m-%d %H:%M:%S"),
        "tags": [{"id": t.id, "name": t.name} for t in task.tags.all()],
    }


def get_tasks(request):
    tasks = Task.objects.all()

    status_filter = request.GET.get("status")
    if status_filter == "pending":
        tasks = tasks.exclude(status__name="выполнена")

    tag_id = request.GET.get("tags")
    if tag_id:
        tasks = tasks.filter(tags__id=tag_id)

    result = [task_to_dict(t) for t in tasks]
    return JsonResponse(result, safe=False)


def post_task(request):
    data = json.loads(request.body)
    title = data.get("title")
    status_id = data.get("status_id")

    status = Status.objects.get(id=status_id)
    task = Task.objects.create(title=title, status=status)

    tag_ids = data.get("tag_ids", [])
    for tid in tag_ids:
        tag = Tag.objects.get(id=tid)
        TaskTag.objects.create(task=task, tag=tag)

    return JsonResponse(task_to_dict(task), status=201)


def get_tags(request):
    tags = Tag.objects.all()
    result = [{"id": t.id, "name": t.name} for t in tags]
    return JsonResponse(result, safe=False)


def post_tag(request):
    data = json.loads(request.body)
    name = data.get("name")
    tag = Tag.objects.create(name=name)
    return JsonResponse({"id": tag.id, "name": tag.name}, status=201)


def get_tag_tasks(request, tag_id):
    tag = Tag.objects.get(id=tag_id)
    tasks = Task.objects.filter(tasktag__tag=tag)
    result = [task_to_dict(t) for t in tasks]
    return JsonResponse(result, safe=False)


def get_statuses(request):
    statuses = Status.objects.all()
    result = [{"id": s.id, "name": s.name} for s in statuses]
    return JsonResponse(result, safe=False)


def post_status(request):
    data = json.loads(request.body)
    name = data.get("name")
    status = Status.objects.create(name=name)
    return JsonResponse({"id": status.id, "name": status.name}, status=201)