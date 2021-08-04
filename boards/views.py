from django.db.models import Count
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import View, ListView, UpdateView
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.urls import reverse
# from django.core.paginator import Page, Paginator, EmptyPage, PageNotAnInteger

from .forms import NewThreadForm, CommentForm
from .models import Board, Thread, Comment

# def boards(request):
#     boards = Board.objects.all()    
#     return render(request, 'boards.html', {'boards': boards})

class BoardList(ListView):
    model = Board
    context_object_name = 'boards'
    template_name = './boards/boards/boards.html'

# def board_threads(request, pk):
#     board = get_object_or_404(Board, pk = pk)
#     queryset = board.threads.order_by('-last_comment_at').annotate(replies = Count('comments') - 1)
#     page = request.GET.get('page', 1)

#     paginator = Paginator(queryset, 20)

#     try:
#         threads = paginator.page(page)
#     except PageNotAnInteger:
#         threads = paginator.page(1)
#     except EmptyPage:
#         threads = paginator.page(paginator.num_pages)

#     return render(request, 'threads.html', {'board': board, 'threads': threads})

class ThreadList(ListView):
    model = Thread
    context_object_name = 'threads'
    template_name = './boards/threads/threads.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        kwargs['board'] = self.board
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.board = get_object_or_404(Board, pk = self.kwargs.get('pk'))
        queryset = self.board.threads.order_by('-last_comment_at').annotate(comment_count = Count('comments') - 1)
        return queryset

@method_decorator(login_required, name = 'dispatch')
class NewThread(View):
    def render(self, request, pk, form = None):
        form = form if form else NewThreadForm()
        board = get_object_or_404(Board, pk = pk)

        return render(request, './boards/threads/new_thread.html', {'board': board, 'form': form})

    def post(self, request, pk):
        form = NewThreadForm(request.POST)
        board = get_object_or_404(Board, pk = pk)

        if form.is_valid():
            thread = form.save(commit = False)
            thread.board = board
            thread.creator = request.user
            thread.save()
            
            Comment.objects.create(
                text = form.cleaned_data.get('text'),
                thread = thread,
                is_master = True,
                created_by = request.user
            )
            return redirect('view_thread', pk = pk, thread_pk = thread.pk)

        return self.render(request, pk, form)
    
    def get(self, request, pk):
        return self.render(request, pk)

class CommentList(ListView):
    model = Comment
    context_object_name = 'comments'
    template_name = './boards/comments/view_thread.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        session_key = f'viewed_thread_{self.thread.pk}'
        if not self.request.session.get(session_key, False):
            self.thread.views += 1
            self.thread.save()
            self.request.session[session_key] = True

        kwargs['thread'] = self.thread
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.thread = get_object_or_404(Thread, board__pk = self.kwargs.get('pk'), pk = self.kwargs.get('thread_pk'))
        queryset = self.thread.comments.order_by('created_at')
        return queryset

@method_decorator(login_required, name = 'dispatch')
class NewParentComment(View):
    def render(self, request, pk, thread_pk, form = None):
        form = form if form else CommentForm()
        thread = get_object_or_404(Thread, board__pk = pk, pk = thread_pk)

        return render(request, './boards/comments/new_parent_comment.html', {'thread': thread, 'form': form})

    def post(self, request, pk, thread_pk):
        form = CommentForm(request.POST)
        thread = get_object_or_404(Thread, board__pk = pk, pk = thread_pk)

        if form.is_valid():
            comment = form.save(commit = False)
            comment.thread = thread
            comment.created_by = request.user
            comment.save()

            thread.last_comment_at = timezone.now()
            thread.save()

            thread_url = reverse('view_thread', kwargs = {'pk': pk, 'thread_pk': thread_pk})
            thread_comment_url = f'{thread_url}?page={thread.get_page_count()}#{comment.pk}'

            return redirect(thread_comment_url)

        return self.render(request, pk, thread_pk, form)

    def get(self, request, pk, thread_pk):
        return self.render(request, pk, thread_pk)

@method_decorator(login_required, name = 'dispatch')
class CommentUpdate(UpdateView):
    model = Comment
    fields = ('text', )
    template_name = './boards/comments/edit_comment.html'
    pk_url_kwarg = 'comment_pk'
    context_object_name = 'comment'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by = self.request.user)

    def form_valid(self, form):
        comment = form.save(commit = False)
        comment.updated_at = timezone.now()
        comment.save()
        return redirect('view_thread', pk = comment.thread.board.pk, thread_pk = comment.thread.pk)