from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer, UserSerializer
from django.http import JsonResponse
from .tasks import add


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


@api_view(['POST'])
def create_comment(request):
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid():
        parent_id = request.data.get('parent')
        if parent_id is not None:
            # Validate and set the parent comment
            try:
                parent_comment = Comment.objects.get(id=parent_id)
                serializer.save(parent=parent_comment)
            except Comment.DoesNotExist:
                return Response({'error': 'Parent comment does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def add_numbers(request):
    # Assuming you pass 'x' and 'y' as query parameters to the view
    x = int(request.GET.get('x', 0))
    y = int(request.GET.get('y', 0))

    # Calling the asynchronous task
    result = add.delay(x, y)

    return JsonResponse({'status': 'The add task has been called. Check Celery for results.'})


@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
