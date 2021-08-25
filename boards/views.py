from django.db.models import Count
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import View, ListView, UpdateView
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.db.models import Q
# from django.core.paginator import Page, Paginator, EmptyPage, PageNotAnInteger

import time

from .forms import NewThreadForm, CommentForm
from .models import Board, Thread, Comment

from utility.utility import get_text_as_markdown

# def boards(request):
#     boards = Board.objects.all()    
#     return render(request, 'boards.html', {'boards': boards})

class BoardList(ListView):
    model = Board
    context_object_name = 'boards'
    template_name = './boards/boards/board_list.html'

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
    template_name = './boards/threads/thread_list.html'
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

class CommentList(View):
    def get(self, request, pk, thread_pk):
        self.request = request
        self.board_pk = pk
        self.thread_pk = thread_pk
        
        self.thread = get_object_or_404(Thread, board__pk = pk, pk = thread_pk)
        
        # if you haven't viewed this thread this session, then increase views.
        session_key = f'viewed_thread_{self.thread_pk}'
        if not self.request.session.get(session_key, False):
            self.thread.views += 1
            self.thread.save()
            self.request.session[session_key] = True

        # create obj list for template
        queryset = self.thread.comments.order_by('created_at')

        self.comments = []

        def get_comment_data_from_queryset_obj(obj, layer=0):
            children = queryset.filter(~Q(parent=-1)).filter(parent=obj.pk).order_by('created_at')

            children_data = []

            for c in children:
                children_data.append(get_comment_data_from_queryset_obj(c, layer + 1))

            return {
                'pk': obj.pk,
                'text': get_text_as_markdown(obj.text),
                'parent': obj.parent,
                'children': children_data,
                'is_master': obj.is_master,
                'created_by': {
                    'username': obj.created_by.username,
                    'comments_count': obj.created_by.comments.count(),
                },
                'created_at': obj.created_at,
                'thread': {
                    'pk': obj.thread.pk,
                    'board': {
                        'pk': obj.thread.board.pk,
                    }
                },
                'karma': obj.karma,
                'layer': layer,
                'logged_in_user': {
                    'name': self.request.user.username,
                    'id': self.request.user.id,
                    'profile': {
                        'comments_upvoted': self.request.user.profile.comments_upvoted,
                        'comments_downvoted': self.request.user.profile.comments_downvoted,
                    }
                }
            }

        for q in queryset:
            self.comments.append(get_comment_data_from_queryset_obj(q))

        return render(request, './boards/comments/comment_list.html', {'thread': self.thread, 'comments': self.comments})

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
class EditComment(View):
    def render(self, request, pk, thread_pk, form = None):
        form = form if form else CommentForm()
        thread = get_object_or_404(Thread, board__pk = pk, pk = thread_pk)

        return render(request, './boards/comments/edit_comment.html', {'thread': thread, 'form': form})

    def post(self, request, pk, thread_pk, comment_pk):
        form = CommentForm(request.POST)
        thread = get_object_or_404(Thread, board__pk = pk, pk = thread_pk)
        old_comment = thread.comments.filter(id = comment_pk).first()

        if form.is_valid():
            comment = form.save(commit = False)
            comment.id = old_comment.id
            comment.is_master = old_comment.is_master
            comment.parent = old_comment.parent
            comment.created_at = old_comment.created_at
            comment.updated_at = timezone.now()
            comment.created_by = old_comment.created_by
            comment.thread = old_comment.thread
            comment.karma = old_comment.karma
            comment.save()

            # Sleep for 1 second, because front end waits for 500ms for database to update before refresh.
            # What this does after the 1 seconds is irrelevant because the iframe containing it will be gone.
            time.sleep(1000)

            thread_url = reverse('view_thread', kwargs = {'pk': pk, 'thread_pk': thread_pk})
            thread_comment_url = f'{thread_url}?page={thread.get_page_count()}#{comment.pk}'

            return redirect(thread_comment_url)

        return self.render(request, pk, thread_pk, form)

    def get(self, request, pk, thread_pk, comment_pk):
        thread = get_object_or_404(Thread, board__pk = pk, pk = thread_pk)
        comment = thread.comments.filter(id = comment_pk).first()

        form = CommentForm(instance = comment)

        return self.render(request, pk, thread_pk, form)

@method_decorator(login_required, name = 'dispatch')
class ReplyComment(View):
    def render(self, request, pk, thread_pk, form = None):
        form = form if form else CommentForm()
        thread = get_object_or_404(Thread, board__pk = pk, pk = thread_pk)

        return render(request, './boards/comments/new_comment.html', {'thread': thread, 'form': form})

    def post(self, request, pk, thread_pk, comment_pk):
        form = CommentForm(request.POST)
        thread = get_object_or_404(Thread, board__pk = pk, pk = thread_pk)

        if form.is_valid():
            comment = form.save(commit = False)
            comment.thread = thread
            comment.created_by = request.user
            comment.parent = comment_pk
            comment.save()

            thread.last_comment_at = timezone.now()
            thread.save()

            # Sleep for 1 second, because front end waits for 500ms for database to update before refresh.
            # What this does after the 1 seconds is irrelevant because the iframe containing it will be gone.
            time.sleep(1000)

            thread_url = reverse('view_thread', kwargs = {'pk': pk, 'thread_pk': thread_pk})
            thread_comment_url = f'{thread_url}?page={thread.get_page_count()}#{comment.pk}'

            return redirect(thread_comment_url)

        return self.render(request, pk, thread_pk, form)

    def get(self, request, pk, thread_pk, comment_pk):
        return self.render(request, pk, thread_pk)

class ViewComment(View):
    def get(self, request, pk, thread_pk, comment_pk):
        self.request = request
        self.board_pk = pk
        self.thread_pk = thread_pk
        self.comment_pk = comment_pk
        
        self.thread = get_object_or_404(Thread, board__pk = pk, pk = thread_pk)
        
        # if you haven't viewed this thread this session, then increase views.
        session_key = f'viewed_thread_{self.thread_pk}'
        if not self.request.session.get(session_key, False):
            self.thread.views += 1
            self.thread.save()
            self.request.session[session_key] = True

        # create obj list for template
        queryset = self.thread.comments.order_by('created_at')

        self.comments = []

        def get_comment_data_from_queryset_obj(obj, layer=0):
            children = queryset.filter(~Q(parent=-1)).filter(parent=obj.pk).order_by('created_at')

            children_data = []

            for c in children:
                children_data.append(get_comment_data_from_queryset_obj(c, layer + 1))

            return {
                'pk': obj.pk,
                'text': get_text_as_markdown(obj.text),
                'parent': obj.parent,
                'children': children_data,
                'is_master': obj.is_master,
                'created_by': {
                    'username': obj.created_by.username,
                    'comments_count': obj.created_by.comments.count(),
                },
                'created_at': obj.created_at,
                'thread': {
                    'pk': obj.thread.pk,
                    'board': {
                        'pk': obj.thread.board.pk,
                    }
                },
                'karma': obj.karma,
                'layer': layer,
                'logged_in_user': {
                    'name': self.request.user.username,
                    'id': self.request.user.id,
                    'profile': {
                        'comments_upvoted': self.request.user.profile.comments_upvoted,
                        'comments_downvoted': self.request.user.profile.comments_downvoted,
                    }
                }
            }

        for q in queryset:
            if (q.id == comment_pk):
                comment_data = get_comment_data_from_queryset_obj(q)
                
                # trick comment_list template into behaving like this linked comment is the top level parent,
                # but save off parent so it can be referenced for the parent link
                comment_data["old_parent"] = comment_data["parent"]
                comment_data["parent"] = -1
                
                self.comments.append(comment_data)

        print(self.comments)

        return render(request, './boards/comments/comment_list.html', {'thread': self.thread, 'comments': self.comments})
