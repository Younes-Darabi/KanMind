from django.urls import include, path
from boards.api.views import BoardsView, BoardDetailView


urlpatterns = [
    path('', BoardsView.as_view(), name='boards-view'),
    path('<int:pk>/', BoardDetailView.as_view(), name='single-board-view'),
    path('api-auth/', include('rest_framework.urls'))
]