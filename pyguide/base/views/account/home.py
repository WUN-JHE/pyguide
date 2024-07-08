from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.


def login_page(request):
    # 已經登入
    if request.user.is_authenticated:
        return redirect('student_index')
    # 未登入
    else:
        # 收到登入 request 
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            # 驗證POST過來的帳號密碼
            user = authenticate(request, username = username, password = password)
            # 驗證成功，有帳號回來
            if user is not None:
                # 修改 request，改成登入狀態
                login(request, user)
                if request.user.user_extension.login_identity == "student":
                    return redirect('student_index')
                elif request.user.user_extension.login_identity == "teacher":
                    return redirect('teacher_index')
        return render(request, 'account/login.html')

def logout_user(request):
    logout(request)
    return redirect('login_page')
