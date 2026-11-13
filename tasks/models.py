from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=255,verbose_name="Называние задачи")
    description = models.TextField(blank=True, verbose_name="Описание задачи")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создание")
    completed = models.BooleanField(default=False, verbose_name="Статус задачи")

    def __str__(self):
        return self.title