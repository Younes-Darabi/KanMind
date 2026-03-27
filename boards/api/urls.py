from django.urls import include, path
from boards.api.views import BoardsView, BoardDetailView

# Define the URL patterns for Board-related API endpoints
urlpatterns = [
    # Global board endpoints: GET to list all boards the user is a member of, 
    # and POST to create a new project board.
    path('', BoardsView.as_view(), name='boards-view'),
    
    # Detail endpoint for a specific board using its Primary Key (ID).
    # Supports GET (retrieve), PATCH (update), and DELETE.
    path('<int:pk>/', BoardDetailView.as_view(), name='single-board-view'),
    
    # Standard Django Rest Framework authentication views (login/logout) 
    # for the browsable API interface.
    path('api-auth/', include('rest_framework.urls'))
]