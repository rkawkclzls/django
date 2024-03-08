from django.db import models
from django.utils import timezone

class Post(models.Model):
    title = models.CharField(max_length = 200)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    updated_date = models.DateTimeField(blank=True, null=True)
    '''
    수정된 시각 필드 추가
    '''

    def publish(self):
        self.published_date = timezone.now()
        self.save()
    
    def save(self, *args, **kwargs):
        '''
        포스트가 데이터베이스에 이미 존재하는 경우, 즉 업데이트하는 경우
        '''
        if self.pk:
            '''
            포스트가 데이터베이스에 이미 존재하는 경우, 즉 업데이트 하는 경우
            '''
            self.updated_date = timezone.now() 
            '''
            수정된 시각을 현재 시간으로 업데이트
            ''' 
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title