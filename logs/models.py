from django.db import models

# Create your models here.
#
class LogEntry(models.Model):
    title = models.TextField(max_length=200)
    body = models.TextField()
    tags = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.title)


