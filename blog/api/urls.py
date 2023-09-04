from django.urls import path
from .views import blog, comment

urlpatterns = [
    path('', blog.BlogListCreateView.as_view()),
] 