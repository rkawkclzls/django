from django.urls import path
from .views import BoardListView, BoardWriteView, BoardDetailView, CommentWriteView

urlpatterns = [
    path('list/', BoardListView.as_view(), name='board_list'),
    path('write/', BoardWriteView.as_view(), name='board_write'),
    path('detail/<int:pk>/', BoardDetailView.as_view(), name='board_detail'),
    path('comment_write/<int:board_id>/', CommentWriteView.as_view(), name='comment_write')
]
