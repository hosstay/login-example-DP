from django.db.models import Count
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView, ListView
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.urls import reverse
# from django.core.paginator import Page, Paginator, EmptyPage, PageNotAnInteger

from .forms import NewThreadForm, PostForm
from .models import Board, Thread, Post

# def boards(request):
#     boards = Board.objects.all()    
#     return render(request, 'boards.html', {'boards': boards})

class BoardListView(ListView):
    model = Board
    context_object_name = 'boards'
    template_name = './boards/boards/boards.html'

# def board_threads(request, pk):
#     board = get_object_or_404(Board, pk = pk)
#     queryset = board.threads.order_by('-last_updated').annotate(replies=Count('posts') - 1)
#     page = request.GET.get('page', 1)

#     paginator = Paginator(queryset, 20)

#     try:
#         threads = paginator.page(page)
#     except PageNotAnInteger:
#         threads = paginator.page(1)
#     except EmptyPage:
#         threads = paginator.page(paginator.num_pages)

#     return render(request, 'threads.html', {'board': board, 'threads': threads})

class ThreadListView(ListView):
    model = Thread
    context_object_name = 'threads'
    template_name = './boards/threads/threads.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        kwargs['board'] = self.board
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.board = get_object_or_404(Board, pk=self.kwargs.get('pk'))
        queryset = self.board.threads.order_by('-last_updated').annotate(replies=Count('posts') - 1)
        return queryset

@login_required
def new_thread(request, pk):
    board = get_object_or_404(Board, pk = pk)

    if request.method == 'POST':
        form = NewThreadForm(request.POST)
        if form.is_valid():
            thread = form.save(commit = False)
            thread.board = board
            thread.creator = request.user
            thread.save()
            
            Post.objects.create(
                message = form.cleaned_data.get('message'),
                thread = thread,
                created_by = request.user
            )
            return redirect('view_thread', pk = pk, thread_pk = thread.pk)
    else:
        form = NewThreadForm()

    return render(request, './boards/threads/new_thread.html', {'board': board, 'form': form})

class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = './boards/posts/view_thread.html'
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
        self.thread = get_object_or_404(Thread, board__pk=self.kwargs.get('pk'), pk=self.kwargs.get('thread_pk'))
        queryset = self.thread.posts.order_by('created_at')
        return queryset

@login_required
def new_parent_post(request, pk, thread_pk):
    thread = get_object_or_404(Thread, board__pk = pk, pk = thread_pk)
    
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit = False)
            post.thread = thread
            post.created_by = request.user
            post.save()

            thread.last_updated = timezone.now()
            thread.save()

            thread_url = reverse('view_thread', kwargs = {'pk': pk, 'thread_pk': thread_pk})
            thread_post_url = f'{thread_url}?page={thread.get_page_count()}#{post.pk}'

            return redirect(thread_post_url)
    else:
        form = PostForm()
    return render(request, './boards/posts/new_parent_post.html', {'thread': thread, 'form': form})

@method_decorator(login_required, name = 'dispatch')
class PostUpdateView(UpdateView):
    model = Post
    fields = ('message', )
    template_name = './boards/posts/edit_post.html'
    pk_url_kwarg = 'post_pk'
    context_object_name = 'post'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by = self.request.user)

    def form_valid(self, form):
        post = form.save(commit = False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect('view_thread', pk = post.thread.board.pk, thread_pk = post.thread.pk)