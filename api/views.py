from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import CommentSerializer
from boards.models import Comment

# class CommentList(generics.ListAPIView):
#     serializer_class = CommentSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user
#         return Comment.objects.filter(user=user)

# class CommentListCreate(generics.ListCreateAPIView):
#     serializer_class = CommentSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user
#         return Comment.objects.filter(user=user)

#     def perform_create(self, serializer):
#         serializer.save(user.self.request.user)

# class CommentRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = CommentSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user
#         return Comment.objects.filter(user=user)

# class CommentUpdate(generics.UpdateAPIView):
#     serializer_class = CommentSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user
#         return Comment.objects.filter(user=user)

#     def perform_update(self, serializer):
#         serializer.instance.field = value
#         serializer.save()

# class CommentUpvote(generics.UpdateAPIView):
#     serializer_class = CommentSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         print(self.kwargs.get('pk'))
#         id = self.kwargs.get('pk')
#         return Comment.objects.filter(id=id)

#     def perform_update(self, serializer):
#         serializer.instance.karma = serializer.instance.karma + 1
#         serializer.save()

@api_view(['PUT', ])
def comment_upvote(request, pk):
    try:
        comment = Comment.objects.get(id=pk)
    except Comment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = CommentSerializer(comment, request.data)
        serializer.instance.karma = serializer.instance.karma + 1
        data = {}

        if serializer.is_valid():
            serializer.save()
            data["success"] = True
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', ])
def comment_downvote(request, pk):
    try:
        comment = Comment.objects.get(id=pk)
    except Comment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = CommentSerializer(comment, request.data)
        serializer.instance.karma = serializer.instance.karma - 1
        data = {}

        if serializer.is_valid():
            serializer.save()
            data["success"] = True
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    