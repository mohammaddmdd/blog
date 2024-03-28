from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet
from rest_framework.authtoken.views import obtain_auth_token
from .views import register
from blog_app.api import api as ninja_api


router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', register, name='register'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('api/v2/', ninja_api.urls),
]
