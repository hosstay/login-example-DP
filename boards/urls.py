from django.urls import path
from boards import views as board_views

urlpatterns = [
    # path('', board_views.boards, name = 'boards'),
    path('', board_views.BoardList.as_view(), name = 'boards'),
    # path('boards/<int:pk>/', board_views.board_threads, name = 'board_threads'),
    path('<int:pk>/', board_views.ThreadList.as_view(), name = 'board_threads'),
    path('<int:pk>/new/', board_views.NewThread.as_view(), name = 'new_thread'),

    # comment urls
    path('<int:pk>/threads/<int:thread_pk>/', board_views.CommentList.as_view(), name = 'view_thread'),
    path('<int:pk>/threads/<int:thread_pk>/new_parent_comment/', board_views.NewParentComment.as_view(), name = 'new_parent_comment'),
    path('<int:pk>/threads/<int:thread_pk>/comments/<int:comment_pk>/edit/', board_views.EditComment.as_view(), name = 'edit_comment'),
    path('<int:pk>/threads/<int:thread_pk>/comments/<int:comment_pk>/reply/', board_views.ReplyComment.as_view(), name = 'reply_comment'),
]