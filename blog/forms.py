from django import forms
from .models import Post, Comment

def min_length_3_validator(value):
    if len(value) < 3:
        raise forms.ValidationError('title 3글자 이상 입력해주세요.')

class PostForm(forms.Form):
    title = forms.CharField(validators=[min_length_3_validator])
    text = forms.CharField(widget=forms.Textarea)

    def save(self, commit=True):
        post = Post(**self.cleaned_data)
        if commit:
            post.save()
        return post

class PostModelForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text',)

# ModelForm을 상
class CommentModelForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'text', )