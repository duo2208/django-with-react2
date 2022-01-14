from django.contrib import messages 
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from .forms import PostForm, CommentForm
from .models import Tag, Post
from datetime import timedelta

@login_required
def index(request):
    timesince = timezone.now() - timedelta(days=3)
    post_list = Post.objects.all()\
        .filter(
            Q(author=request.user) |
            Q(author__in=request.user.following_set.all())
        )\
        .filter(
            created_at__gte = timesince # greater than equal
        )

    # User.objects.all() 은 유연하지 않은 방법
    suggested_user_list = get_user_model().objects.all()\
        .exclude(pk=request.user.pk)\
        .exclude(pk__in=request.user.following_set.all())[:5]

    comment_form = CommentForm()

    return render(request, "instagramsns/index.html", {
        "post_list": post_list,
        "suggested_user_list": suggested_user_list,
        "comment_form": comment_form,
    })

@login_required 
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)  # DB에 당장 저장하지 않는다
            post.author = request.user
            post.save()
            post.tag_set.add(*post.extract_tag_list())  # 리스트 형식이므로 * 붙여주기
            messages.success(request, "포스팅을 저장했습니다.")
            return redirect(post)   # get_absolute_url 활용
    else:
        form = PostForm()
    
    return render(request, 'instagramsns/post_form.html ', {
        "form": form,
    })

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comment_form = CommentForm()
    return render(request, "instagramsns/post_detail.html", {
        "post": post,
        "comment_form": comment_form,
    })

@login_required
def post_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.like_user_set.add(request.user)
    messages.success(request, f"포스팅#{post.pk}를 좋아합니다.")
    redirect_url = request.META.get("HTTP_REFERER", "root")
    return redirect(redirect_url)

@login_required
def post_dislike(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.like_user_set.remove(request.user)
    messages.success(request, f"포스팅#{post.pk} 좋아요를 취소합니다.")
    redirect_url = request.META.get("HTTP_REFERER", "root")
    return redirect(redirect_url)

def user_page(request, username):
    # urls.py에서 넘겨받은 username이 
    # logined된 User가 가진 필드에 존재하는가를 체크해야 한다.
    page_user = get_object_or_404(get_user_model(), username=username, is_active=True)  # is_active로 접근이 허용된 사람이 아니면 404
    post_list = Post.objects.filter(author=page_user)
    post_list_count = post_list.count() # 실제 DB에 count 쿼리를 던진다.
    #len(post_list)로 쓰면 post_list 전체를 다 가져와서 메모리에 얹은 다음에 메모리상의 리스트의 갯수를 반환해므로 느리다.
    
    if request.user.is_authenticated:   # 로그인이 되어 있다면 User 객체 리턴, 아닐시 AnonymousUser 객체 리턴
        is_follow = request.user.following_set.filter(pk=page_user.pk).exists()
    else:
        is_follow = False

    return render(request, "instagramsns/user_page.html",{
        "page_user": page_user,
        "post_list": post_list,
        "post_list_count": post_list_count,
        "is_follow": is_follow,
    })

@login_required
def comment_new(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)

    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            # author와 와 post 에 대한 필드를 채우지 않았으므로
            # DB 저장을 지연시킨다.
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()

            if request.is_ajax():
                return render(request, "instagramsns/_comment.html", {
                    "comment": comment,
                })
    
            return redirect(comment.post)
            
    else:
        form = CommentForm()
    return render(request, "instagramsns/comment_form.html", {
        "form": form,
    })