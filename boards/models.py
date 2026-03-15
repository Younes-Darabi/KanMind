from django.db import models
from users.models import User


class Board(models.Model):

    title = models.CharField(max_length=30)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_boards')
    members = models.ManyToManyField(User, related_name='boards')

    def __str__(self):
        return self.title