from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.views import LoginView, logout_then_login
from django.shortcuts import redirect, render
from .forms import SignupForm

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            signed_user = form.save()
            auth_login(request, signed_user)
            messages.success(request, "회원가입을 환영합니다.")
            signed_user.send_welcome_email()    # FIX : 비동기(Celery)화 추천
            next_url = request.GET.get('next', 'root')
            return redirect(next_url)
    else:
        form = SignupForm()
    return render(request, 'accounts/signup_form.html', {
        'form': form,
    } )

def logout(request):
    messages.success(request, "로그아웃되었습니다.")
    return logout_then_login(request)

login = LoginView.as_view(template_name="accounts/login_form.html")



