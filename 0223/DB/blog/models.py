from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=100)
    contents = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  # 처음 생성될 때에만
    updated_at = models.DateTimeField(auto_now=True)  # 수정될 때마다

    def __str__(self):
        return f"제목: {self.title}, 생성시간: {self.created_at}, 수정시간: {self.updated_at}"