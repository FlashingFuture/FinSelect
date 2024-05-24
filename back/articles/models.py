from django.db import models
from django.conf import settings

# Create your models here.
class Article(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='게시물 작성자')
    title = models.CharField(max_length=100, verbose_name='제목')
    content = models.TextField(verbose_name='내용')
    article_file = models.FileField(upload_to='article_files/', blank=True, null=True, verbose_name='파일')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.IntegerField(default=0, verbose_name='조회수') 
    


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments', verbose_name='댓글단 글')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='댓글 작성자')
    content = models.TextField(verbose_name='댓글 내용')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.IntegerField(default=0, verbose_name='조회수') 


