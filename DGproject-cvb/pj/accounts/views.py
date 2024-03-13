from django.shortcuts import render, redirect
from django.views import View
from .models import User
from django.contrib.auth.hashers import make_password
from .forms import LoginForm
from django.contrib import messages

# HomeView는 home.html 템플릿을 렌더링합니다.
class HomeView(View):
    def get(self, request):
        return render(request, 'accounts/home.html')


# RegisterView는 사용자 등록을 처리합니다.
class RegisterView(View):
    def get(self, request):
        return render(request, 'accounts/register.html')

    def post(self, request):
        # POST 요청에서 폼 데이터 가져오기
        username = request.POST.get('username', None)
        useremail = request.POST.get('useremail', None)
        password = request.POST.get('password', None)
        re_password = request.POST.get('re_password', None)

        err_data = {}
        if not (username and useremail and password and re_password):
            err_data['error'] = '모든 값을 입력해주세요.'  # 필드가 누락된 경우 오류 메시지
        elif password != re_password:
            err_data['error'] = '비밀번호가 다릅니다.'  # 비밀번호가 일치하지 않는 경우 오류 메시지
        else:
            # 중복 체크
            if User.objects.filter(username=username).exists():
                err_data['error'] = '이미 사용 중인 이름입니다.'  # 중복된 이름인 경우 오류 메시지
            elif User.objects.filter(useremail=useremail).exists():
                err_data['error'] = '이미 사용 중인 이메일입니다.'  # 중복된 이메일인 경우 오류 메시지
            else:
                # 새로운 User 객체를 생성하고 데이터베이스에 저장
                user = User(
                    username=username,
                    useremail=useremail,
                    password=make_password(password),
                )
                user.save()
                messages.success(request, '회원가입이 완료되었습니다! 로그인 페이지로 이동합니다.')  # 성공 메시지
                return redirect('/accounts/login/')

        return render(request, 'accounts/register.html', err_data)


# LoginView는 사용자 로그인을 처리합니다.
class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'accounts/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            request.session['user'] = form.user_id
            return redirect('/')
        return render(request, 'accounts/login.html', {'form': form})


# LogoutView는 사용자 로그아웃을 처리합니다.
class LogoutView(View):
    def get(self, request):
        return self.logout(request)

    def post(self, request):
        return self.logout(request)

    def logout(self, request):
        if request.session.get('user'):
            del (request.session['user'])
        return redirect('/')


