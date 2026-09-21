from django.contrib import admin
from .models import Status, Tag, Task, TaskTag

admin.site.register(Status)
admin.site.register(Tag)
admin.site.register(Task)
admin.site.register(TaskTag)