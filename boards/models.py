from django.db import models
from users.models import User

class Board(models.Model):
    """
    Represents a project board. 
    A board acts as a container for tasks and defines access levels for users.
    """
    title = models.CharField(max_length=30)
    
    # The user who created the board. If the owner is deleted, the board is removed.
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_boards')
    
    # A board can have multiple members, and a user can belong to multiple boards.
    members = models.ManyToManyField(User, related_name='boards')

    def __str__(self):
        """Returns the board title as its string representation."""
        return self.title