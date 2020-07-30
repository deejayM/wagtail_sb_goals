
from django.urls import path
from django.urls import path, re_path, include

from .views import (
    BoardListView,
    BoardDetailView,
    BoardCreateView,
    BoardUpdateView,
    BoardDeleteView,
    UserBoardListView
)
from . import views

app_name = 'sb_quiver'

urlpatterns = [
    path('', BoardListView.as_view(), name='sb_quiver-home'),
    path('user/<str:username>/', UserBoardListView.as_view(), name='user-boards'),
    path('board/<int:pk>/', BoardDetailView.as_view(), name='board-detail'),
    path('board/new/', BoardCreateView.as_view(), name='board-create'),
    path('board/<int:pk>/update/', BoardUpdateView.as_view(), name='board-update'),
    path('board/<int:pk>/delete/', BoardDeleteView.as_view(), name='board-delete'),
    path('about/', views.about, name='sb_quiver-about'),
]