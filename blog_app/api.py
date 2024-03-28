# app_name/api.py
from ninja import NinjaAPI
from .models import Post
from .schemas import PostSchema

api = NinjaAPI()

@api.get("/posts", response=list[PostSchema])
def list_posts(request):
    posts = Post.objects.all()
    return posts