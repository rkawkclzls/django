from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.core.paginator import Paginator
from .models import Board, Comment
from .forms import BoardForm, CommentForm
from accounts.models import User
from tag.models import Tag

class BoardWriteView(View):
    def get(self, request):
        if not request.session.get('user'):
            return redirect('/accounts/login')
        form = BoardForm()
        return render(request, 'boards/board_write.html', {'form': form})

    def post(self, request):
        if not request.session.get('user'):
            return redirect('/accounts/login')
        form = BoardForm(request.POST)
        if form.is_valid():
            user_id = request.session.get('user')
            user = User.objects.get(pk=user_id)
            tags = form.cleaned_data['tags'].split(',')

            board = Board()
            board.title = form.cleaned_data['title']
            board.contents = form.cleaned_data['contents']
            board.writer = user
            board.save()

            for tag in tags:
                if not tag:
                    continue
                _tag, _ = Tag.objects.get_or_create(name=tag)
                board.tags.add(_tag)

            return redirect('/boards/list')
        return render(request, 'boards/board_write.html', {'form': form})

class BoardDetailView(View):
    def get(self, request, pk):
        board = get_object_or_404(Board, pk=pk)
        comments = CommentForm()
        comment_view = Comment.objects.filter(post=pk)
        return render(request, 'boards/board_detail.html', {'board': board, 'comments': comments, 'comment_view': comment_view})

class BoardListView(View):
    def get(self, request):
        all_boards = Board.objects.all().order_by('-id')
        page = int(request.GET.get('p', 1))
        paginator = Paginator(all_boards, 5)
        boards = paginator.get_page(page)
        return render(request, 'boards/board_list.html', {'boards': boards})

class CommentWriteView(View):
    def post(self, request, board_id):
        comment_write = CommentForm(request.POST)
        user_id = request.session['user']
        user = User.objects.get(pk=user_id)
        if comment_write.is_valid():
            comments = comment_write.save(commit=False)
            comments.post = get_object_or_404(Board, pk=board_id)
            comments.author = user
            comments.save()
        return redirect('board_detail', pk=board_id)
