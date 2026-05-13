from django.db import models
from django.contrib.auth.models import User

class ResumeHistory(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    filename = models.CharField(max_length=200)

    score = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.filename