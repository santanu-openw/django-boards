# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import NewTopicForm , PostForm
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import UpdateView,ListView
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from django.shortcuts import render
from .models import Board, Topic, Post





#def home(request):
    #boards = Board.objects.all()
    #return render(request, 'boards/home.html', {'boards': boards})

class BoardListView(ListView):
    model = Board
    context_object_name = 'boards'
    template_name = 'boards/home.html' 

     

class TopicListView(ListView):
    model = Topic
    context_object_name = 'topics'
    template_name = 'boards/topics.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        kwargs['board'] = self.board
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.board = get_object_or_404(Board, pk=self.kwargs.get('pk'))
        queryset = self.board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
        return queryset      



     

@login_required
def new_topic(request, id):
    board = get_object_or_404(Board, id=id)
    user = User.objects.first()  # TODO: get the currently logged in user
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user
            )
            return redirect('board_topics', id=board.id)  # TODO: redirect to the created topic page
    else:
        form = NewTopicForm()
    return render(request, 'boards/new_topic.html', {'board': board, 'form': form})


def topic_posts(request, id, topic_id):
    topic = get_object_or_404(Topic, board_id=id, id=topic_id)
    topic.views += 1
    topic.save()
    return render(request, 'boards/topic_posts.html', {'topic': topic})


    
    
    


@login_required
def reply_topic(request, id, topic_id):
    topic = get_object_or_404(Topic, board_id=id, id=topic_id)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            return redirect('topic_posts', id=id, topic_id=topic_id)
    else:
        form = PostForm()
    return render(request, 'boards/reply_topic.html', {'topic': topic, 'form': form})


@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
    model = Post
    fields = ('message', )
    template_name = 'boards/edit_post.html'
    pk_url_kwarg = 'post_pk'
    context_object_name = 'post'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect('topic_posts', id=post.topic.board.id, topic_id=post.topic.id)    