from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.utils import timezone
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import Post, Comment
from .forms import PostForm, PostModelForm, CommentModelForm


# Create your views here.
def post_list(request):
    # name = '장고'
    # return HttpResponse("""
    #     <h1>hello Django</h1>
    #     <p>{name}</p>
    #     <p>{user}</p>
    # """.format(name=name, user=request.user))
    # return render(request, 'blog/post_list.html')

    posts = Post.objects.filter(published_date__lte=timezone.now()).\
        order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post':post})

@login_required
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            post = Post.objects.create(author=User.objects.get(username=request.user.username)\
                                       , published_date=timezone.now(), title=form.cleaned_data['title'], text=form.cleaned_data['text'])
            # post = form.save(commit=False)
            # post.author = User.objects.get(username=request.user)
            # post.published_date = timezone.now()
            # post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        # 등록 Form을 보여준다
        form = PostModelForm()
    return render(request, 'blog/post_edit.html', {'form':form})

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

@login_required
def post_edit(request, pk):
    # DB에서 해당 pk와 매칭되는 Post 객체를 가져온다.
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        # 수정처리
        form = PostModelForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = User.objects.get(username=request.user)
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        # 수정하기 전에 데이터를 읽어옴
        form = PostModelForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form':form})

# Comment 승인
@login_required
def comment_approve(request, pk):
    pass

def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentModelForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            # comment 객체에 매칭되는 post id를 저장
            comment.post = post
            # DB에 저장됨
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentModelForm()
    return render(request, 'blog/add_comment_to_post.html', {'form':form})