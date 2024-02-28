from django.shortcuts import render
from .models import Post


def blog_list(request):
    blogs = Post.objects.all()
    context = {"db": blogs}
    return render(request, "blog/blog_list.html", context)


def blog_detail(request, pk):
    blog = Post.objects.get(pk=pk)
    context = {"db": blog}
    return render(request, "blog/blog_detail.html", context)


def blog_test(request):
    return render(request, "blog/blog_test.html")