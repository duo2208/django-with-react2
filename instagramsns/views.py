from django.contrib import messages 
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from .forms import PostForm
from .models import Tag, Post

@login_required
def index(request):
    # User.objects.all() 은 유연하지 않은 방법
    suggested_user_list = get_user_model().objects.all()\
        .exclude(pk=request.user.pk)\
        .exclude(pk__in=request.user.following_set.all())[:5]
    return render(request, "instagramsns/index.html", {
        "suggested_user_list": suggested_user_list,
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
    return render(request, "instagramsns/post_detail.html", {
        "post": post,
    })

def user_page(request, username):
    # urls.py에서 넘겨받은 username이 
    # logined된 User가 가진 필드에 존재하는가를 체크해야 한다.
    page_user = get_object_or_404(get_user_model(), username=username, is_active=True)  # is_active로 접근이 허용된 사람이 아니면 404
    post_list = Post.objects.filter(author=page_user)
    post_list_count = post_list.count() # 실제 DB에 count 쿼리를 던진다.
    #len(post_list)로 쓰면 post_list 전체를 다 가져와서 메모리에 얹은 다음에 메모리상의 리스트의 갯수를 반환해므로 느리다.

    return render(request, "instagramsns/user_page.html",{
        "page_user": page_user,
        "post_list": post_list,
        "post_list_count": post_list_count,
    })