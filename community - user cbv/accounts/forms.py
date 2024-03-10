from django import forms

from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password

from django.core.exceptions import ValidationError

from .models import User
from .models import User

class LoginForm(forms.Form):
    useremail = forms.EmailField(
        error_messages={'required': '아이디를 입력해주세요.'},
        max_length=64,
        label="사용자 이메일"
    )
    password = forms.CharField(
        error_messages={'required': '비밀번호를 입력해주세요.'},
        widget=forms.PasswordInput,
        label="비밀번호"
    )
    
    def clean(self):
        cleaned_data = super().clean()
        useremail = cleaned_data.get('useremail')
        password = cleaned_data.get('password')

        if useremail and password:
            # User.DoesNotExist 예외를 처리합니다.
            try:
                user = User.objects.get(useremail=useremail)
                if not check_password(password, user.password):
                    raise forms.ValidationError('비밀번호가 틀립니다.')
                else:
                    cleaned_data['user'] = user
            except User.DoesNotExist:
                raise forms.ValidationError('등록되지 않은 이메일입니다.')
        return cleaned_data



class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput, label='비밀번호 확인')

    class Meta:
        model = User
        fields = ['username', 'useremail', 'password']  # 'email'을 'useremail'로 변경

    def clean_useremail(self):
        useremail = self.cleaned_data.get('useremail')
        if User.objects.filter(useremail=useremail).exists():
            raise forms.ValidationError('이 이메일은 이미 사용 중입니다.')
        return useremail

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password') != cleaned_data.get('password2'):
            self.add_error('password2', '비밀번호가 일치하지 않습니다.')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # 비밀번호 해시 처리
        if commit:
            user.save()
        return user



    