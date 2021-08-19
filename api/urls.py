from django.urls import path

from . import views

urlpatterns = [
    path('comments/<int:pk>/upvote/', views.comment_upvote),
    path('comments/<int:pk>/downvote/', views.comment_downvote),
]