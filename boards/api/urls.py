from django.urls import include, path
from boards.api.views import BoardsView, SingleBoardView

# URL configuration for the Boards API.
# These endpoints handle all project board-related operations.

urlpatterns = [
    # GET: List all boards | POST: Create a new board
    path('', BoardsView.as_view(), name='boards_view'),

    # GET: Retrieve board details | PATCH: Update board | DELETE: Remove board
    # <int:pk> is the Primary Key (ID) of the board.
    path('<int:pk>/', SingleBoardView.as_view(), name='single_board_view'),

    # Built-in DRF login/logout views for the browsable API.
    path('api-auth/', include('rest_framework.urls'))
]