from django.shortcuts import render
from django.shortcuts import get_object_or_404
from blog.models import Post

# Create your views here.
def postlist(request):
    posts = Post.objects.all()
    return render(request, "blog/list.html", {"posts":posts})


def postdetail(request, year, month, day, post_detail):
    post_detail = get_object_or_404(Post, slug=post_detail, publish__year=year, publish__month=month, publish__day= day )
    return render(request, "blog/detail.html", {"post_detail":post_detail})


