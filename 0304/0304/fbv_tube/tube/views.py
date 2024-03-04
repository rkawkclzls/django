from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Comment, Tag
from .forms import CommentForm, PostForm


def tube_list(request):
    posts = Post.objects.all()
    return render(request, "tube/tube_list.html", {"posts": posts})


def tube_detail(request, pk):
    post = Post.objects.get(pk=pk)
    form = CommentForm()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            author = request.user
            message = form.cleaned_data["message"]
            c = Comment.objects.create(author=author, message=message, post=post)
            c.save()
    return render(request, "tube/tube_detail.html", {"post": post, "form": form})


@login_required
def tube_create(request):
    if request.method == "GET":
        form = PostForm()
        context = {"form": form}
        return render(request, "tube/tube_create.html", context)
    elif request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save()
            return redirect("tube_list")
        else:
            context = {"form": form}
            return render(request, "tube/tube_create.html", context)


@login_required
def tube_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # 내가 쓴 게시물만 업데이트 가능
    if post.author != request.user:
        return redirect("tube_list")

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect("tube_detail", pk=post.pk)
    else:
        form = PostForm(instance=post)
        context = {"form": form, "pk": pk}
        return render(request, "tube/tube_update.html", context)


@login_required
def tube_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # 내가 쓴 게시물만 삭제 가능
    if post.author != request.user:
        return redirect("tube_list")

    if request.method == "POST":
        post.delete()
    return redirect("tube_list")


def tube_tag(request, tag):
    posts = Post.objects.filter(tags__name__iexact=tag)
    return render(request, "tube/tube_list.html", {"posts": posts})
