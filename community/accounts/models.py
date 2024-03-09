from django.db import models

class User(models.Model):
    username = models.CharField(max_length=64)
    useremail = models.EmailField(max_length=64)
    password = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username
    
    class Meta:
        db_table = 'community_user'
        verbose_name = '커뮤니티 사용자'
        '''
        가시적으로 표시될 어드민페이지의 이름명을
        커뮤니티 사용자라고 지정
        '''
        verbose_name_plural = '커뮤니티 사용자'
        '''
        plural은 복수형으로 나타날 이름을 커뮤니티 사용자로
        통합해준것
        '''
# Create your models here.
