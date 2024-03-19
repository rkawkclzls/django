from django.contrib.auth.models import AbstractUser
from django.db import models

# abstractuser와 abstractbaseuser의 차이점은 
# abstractuser는 username, password, first_name, last_name, email, is_staff, is_active, is_superuser, last_login, date_joined를 기본으로 가지고 있고, 
# abstractbaseuser는 password, last_login, is_superuser, username을 기본으로 가지고 있습니다.
# 초급자에게 권하는 방법은 abstractuser를 사용하는 것입니다. abstractbaseuser는 너무 많은 것을 구현해야 하기 때문입니다.

class User(AbstractUser):
    # 추가 필드 예시
    bio = models.TextField(blank=True) # 사용자 기분 정보
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)

###################################
# users > urls.py (생성 후 저장)

from django.urls import path
from .views import (
    UserCreateView,
    UserDetailView,
)

# 로그인은 JWT를 사용하므로, 회원가입과 유저 정보 조회만 구현
urlpatterns = [
    path('signup/', UserCreateView.as_view(), name='signup'),
    path('user/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
]