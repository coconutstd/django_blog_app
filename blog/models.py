from django.db import models
from django import forms
from django.utils import timezone

def min_length_3_validator(value):
    if len(value) < 3:
        raise forms.ValidationError('3글자 이상 입력해주세요.')

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200, validators=[min_length_3_validator])
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    # test = models.TextField()

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

# Post에 달리는 댓글 Comment 클래스
class Comment(models.Model):
    # post 정보
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    # 댓글 작성자
    author = models.CharField(max_length=100)
    # 댓글 내용
    text = models.TextField()
    # 댓글 작성일자
    created_date = models.DateTimeField(default=timezone.now)
    # 댓글 승인여부
    approved_comment = models.BooleanField(default=False)

    # 댓글 승인하기
    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text

    # 승인된 comments만 반환해주는 함수 구현하기


