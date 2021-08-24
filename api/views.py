from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import CommentSerializer, ProfileSerializer
from boards.models import Comment, Profile

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
def comment_upvote(request, user_id, pk): 
    try:
        comment = Comment.objects.get(id=pk)
    except Comment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        commentSerializer = CommentSerializer(comment, request.data)
        data = {}

        try:
            profile = Profile.objects.get(user_id=user_id)
        except Profile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        profileSerializer = ProfileSerializer(profile, request.data)
        if profileSerializer.instance.comments_upvoted is None or pk not in profileSerializer.instance.comments_upvoted:
            if profileSerializer.instance.comments_downvoted is None or pk not in profileSerializer.instance.comments_downvoted:

                if profileSerializer.instance.comments_upvoted is not None:
                    profileSerializer.instance.comments_upvoted.append(pk)
                else:
                    profileSerializer.instance.comments_upvoted = '{' + str(pk) + '}'

                commentSerializer.instance.karma = commentSerializer.instance.karma + 1

                if profileSerializer.is_valid():
                    if commentSerializer.is_valid():
                        commentSerializer.save()
                        profileSerializer.save()
                        data["success"] = True
                    else:
                        return Response(commentSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(profileSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                if profileSerializer.instance.comments_downvoted is not None:
                    profileSerializer.instance.comments_downvoted.remove(pk)

                if profileSerializer.instance.comments_upvoted is not None:
                    profileSerializer.instance.comments_upvoted.append(pk)
                else:
                    profileSerializer.instance.comments_upvoted = '{' + str(pk) + '}'

                commentSerializer.instance.karma = commentSerializer.instance.karma + 2

                if profileSerializer.is_valid():
                    if commentSerializer.is_valid():
                        commentSerializer.save()
                        profileSerializer.save()
                        data["success"] = True
                    else:
                        return Response(commentSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(profileSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            print('pk already in upvoted array')
        return Response(data=data)

@api_view(['PUT', ])
def comment_undo_upvote(request, user_id, pk):
    try:
        comment = Comment.objects.get(id=pk)
    except Comment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        commentSerializer = CommentSerializer(comment, request.data)
        data = {}

        try:
            profile = Profile.objects.get(user_id=user_id)
        except Profile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        profileSerializer = ProfileSerializer(profile, request.data)
        if profileSerializer.instance.comments_upvoted is not None and pk in profileSerializer.instance.comments_upvoted:
            profileSerializer.instance.comments_upvoted.remove(pk)
            commentSerializer.instance.karma = commentSerializer.instance.karma - 1

            if profileSerializer.is_valid():
                if commentSerializer.is_valid():
                    commentSerializer.save()
                    profileSerializer.save()
                    data["success"] = True
                else:
                    return Response(commentSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(profileSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            print("pk should be there if we're undoing, so button is in wrong state. send back 200 so it toggles back to correct state")
        return Response(data=data)

@api_view(['PUT', ])
def comment_downvote(request, user_id, pk):
    try:
        comment = Comment.objects.get(id=pk)
    except Comment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        commentSerializer = CommentSerializer(comment, request.data)
        data = {}

        try:
            profile = Profile.objects.get(user_id=user_id)
        except Profile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        profileSerializer = ProfileSerializer(profile, request.data)
        if profileSerializer.instance.comments_downvoted is None or pk not in profileSerializer.instance.comments_downvoted:
            if profileSerializer.instance.comments_upvoted is None or pk not in profileSerializer.instance.comments_upvoted:

                if profileSerializer.instance.comments_downvoted is not None:
                    profileSerializer.instance.comments_downvoted.append(pk)
                else:
                    profileSerializer.instance.comments_downvoted = '{' + str(pk) + '}'

                commentSerializer.instance.karma = commentSerializer.instance.karma - 1

                if profileSerializer.is_valid():
                    if commentSerializer.is_valid():
                        commentSerializer.save()
                        profileSerializer.save()
                        data["success"] = True
                    else:
                        return Response(commentSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(profileSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                if profileSerializer.instance.comments_upvoted is not None:
                    profileSerializer.instance.comments_upvoted.remove(pk)

                if profileSerializer.instance.comments_downvoted is not None:
                    profileSerializer.instance.comments_downvoted.append(pk)
                else:
                    profileSerializer.instance.comments_downvoted = '{' + str(pk) + '}'

                commentSerializer.instance.karma = commentSerializer.instance.karma - 2

                if profileSerializer.is_valid():
                    if commentSerializer.is_valid():
                        commentSerializer.save()
                        profileSerializer.save()
                        data["success"] = True
                    else:
                        return Response(commentSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(profileSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            print('pk already in downvoted array')
        return Response(data=data)

@api_view(['PUT', ])
def comment_undo_downvote(request, user_id, pk):
    try:
        comment = Comment.objects.get(id=pk)
    except Comment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        commentSerializer = CommentSerializer(comment, request.data)
        data = {}

        try:
            profile = Profile.objects.get(user_id=user_id)
        except Profile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        profileSerializer = ProfileSerializer(profile, request.data)
        if profileSerializer.instance.comments_downvoted is not None and pk in profileSerializer.instance.comments_downvoted:
            profileSerializer.instance.comments_downvoted.remove(pk)
            commentSerializer.instance.karma = commentSerializer.instance.karma + 1

            if profileSerializer.is_valid():
                if commentSerializer.is_valid():
                    commentSerializer.save()
                    profileSerializer.save()
                    data["success"] = True
                else:
                    return Response(commentSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(profileSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            print("pk should be there if we're undoing, so button is in wrong state. send back 200 so it toggles back to correct state")
        return Response(data=data)