from rest_framework import viewsets
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from django.http import JsonResponse
from .tasks import add

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


def add_numbers(request):
    # Assuming you pass 'x' and 'y' as query parameters to the view
    x = int(request.GET.get('x', 0))
    y = int(request.GET.get('y', 0))

    # Calling the asynchronous task
    result = add.delay(x, y)

    return JsonResponse({'status': 'The add task has been called. Check Celery for results.'})