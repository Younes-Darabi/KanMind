from django.urls import path
from .views import BoardView, SingleBoardView

urlpatterns = [
    path('', BoardView.as_view(), name='board'),
    path('<int:pk>', SingleBoardView.as_view(), name='single_board'),
]
