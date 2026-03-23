from django.db import models
from users.models import User


class Board(models.Model):
    """
    Represents a project management board.
    
    Attributes:
        title (str): The name of the board (max 30 characters).
        owner (User): The user who created the board (Foreign Key).
        members (User): A list of users who have access to this board (Many-to-Many).
    """

    title = models.CharField(max_length=30)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_boards')
    members = models.ManyToManyField(User, related_name='boards')

    def __str__(self):
        """Returns the string representation of the board."""
        return self.title