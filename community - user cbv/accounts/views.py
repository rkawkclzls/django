from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.views.generic.edit import FormView
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from django.contrib.auth import login
from django.contrib.auth import login as auth_login
from django.contrib.auth.views import LoginView as AuthLoginView
from django.contrib.auth.views import LogoutView as AuthLogoutView
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import AuthenticationForm  # LoginForm의 대체

from .forms import RegistrationForm 
from .forms import LoginForm
from .models import User

class HomeView(View):
    def get(self, request, *args, **kwargs):
        user_id = request.session.get('user')
        if user_id:
            user = User.objects.get(pk=user_id)
            return HttpResponse(f"Hello! {user}님")
        else:
            return HttpResponse("로그인 해주세요!")

class RegisterView(FormView):
    template_name = 'accounts/register.html'
    form_class = RegistrationForm  # RegistrationForm은 생성해야 함
    success_url = '/'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.password = make_password(form.cleaned_data['password'])
        user.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return render(self.request, 'accounts/register.html', {'form': form})



class LoginView(FormView):
    form_class = LoginForm
    template_name = 'accounts/login.html'
    success_url = '/'
    
    def form_valid(self, form):
        user = form.cleaned_data['user']
        auth_login(self.request, user)  
        return super().form_valid(form)


class LogoutView(AuthLogoutView):
    next_page = '/'
