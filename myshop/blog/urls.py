from django.urls import path
from . import views

app_name= "blog"

urlpatterns = [
    path("<slug:post_detail>/<int:year>/<int:month>/<int:day>/", views.postdetail, name="post_detail"),
    path("blog", views.postlist, name="blog_news")
]

