from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from ..serializers.comment import CommentSerializer
from blog.models import Comment
from rest_framework.authentication import TokenAuthentication
from rest_framework.authentication import BasicAuthentication
from rest_framework.authentication import SessionAuthentication
from django.http import Http404
from ...models import Comment, Post


class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    

class CommentRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

class PostCommentListCreateView(generics.ListCreateAPIView):
     queryset = Comment.objects.all()
     serializer_class = CommentSerializer

     def get_queryset(self):
        post_id = self.kwargs.get('pk')
        
        queryset = Comment.objects.filter(post=post_id)
        if not queryset.exists():
            raise Http404("Post does not exist")

        return queryset

     def get_serializer_class(self):
        if self.request.method == 'POST':
            return CommentSerializer  
        return super().get_serializer_class()

     def perform_create(self, serializer):
        list = Post.objects.filter(pk=self.kwargs.get('pk'))
        if not list.exists():
            raise Http404("Post does not exist")

        serializer.save(post=list[0])
post_comment_list_create_view = PostCommentListCreateView.as_view()