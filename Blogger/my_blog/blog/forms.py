from django import forms
from .models import Comment,Post,video

class NewComment(forms.ModelForm):
    class Meta:
        model=Comment
        fields=('name','email','body')
class PostCreateForm(forms.ModelForm):
    title=forms.CharField(label='عنوان التدويتة')
    content=forms.CharField(label='النص',widget=forms.Textarea)
    class Meta:
        model=Post
        fields=['title','content'] 

class VideoCreateForm(forms.ModelForm):
    title=forms.CharField(label='عنوان اللقاء')
    url=forms.CharField(label='الرابط')
    class Meta:
        model=video
        fields=['title','url']       