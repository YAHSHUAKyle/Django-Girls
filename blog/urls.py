from django.urls import path, include
from . import views
from .api.views.blog import BlogRetrieveUpdateDeleteView
from .api.views.comment import CommentListCreateView, CommentRetrieveUpdateDeleteView
from .api.views.api_auth import CustomAuthToken
from .api.views import comment


urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('drafts/', views.post_draft_list, name='post_draft_list'),
    path('post/<pk>/publish/', views.post_publish, name='post_publish'),
    path('post/<pk>/remove/', views.post_remove, name='post_remove'),
    path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    path('comment/<int:pk>/approve/', views.comment_approve, name='comment_approve'),
    path('comment/<int:pk>/remove/', views.comment_remove, name='comment_remove'),
    path('api/', include('blog.api.urls')),
    path('api/<int:pk>/', BlogRetrieveUpdateDeleteView.as_view()),
    path('apicomment/', CommentListCreateView.as_view()),
    path('apicomment/<int:pk>/', CommentRetrieveUpdateDeleteView.as_view()),
    path('api-token-auth/', CustomAuthToken.as_view()),
    path('api/<int:pk>/comment', comment.post_comment_list_create_view, name='post-comment-list'),
]