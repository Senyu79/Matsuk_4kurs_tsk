from django.db import models


class Status(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Task(models.Model):
    title = models.CharField(max_length=200)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, through="TaskTag", blank=True)

    def __str__(self):
        return self.title


class TaskTag(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.task} — {self.tag}"