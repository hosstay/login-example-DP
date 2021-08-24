from django.urls import path

from . import views

urlpatterns = [
    path('user/<int:user_id>/comment/<int:pk>/upvote/', views.comment_upvote),
    path('user/<int:user_id>/comment/<int:pk>/undo/upvote/', views.comment_undo_upvote),
    path('user/<int:user_id>/comment/<int:pk>/downvote/', views.comment_downvote),
    path('user/<int:user_id>/comment/<int:pk>/undo/downvote/', views.comment_undo_downvote),
]