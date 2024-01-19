from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserCreationForms(forms.ModelForm):
    username=forms.CharField(label='اسم المستخدم', max_length=50,help_text='اسم المستخدم لا يمكن ان يحتوي على مسافات')
    email=forms.EmailField(label='البريد الاكتروني')
    first_name=forms.CharField(label='الاسم الاول')
    last_name=forms.CharField(label='الاسم الثاني')
    password1=forms.CharField(label='كلمة المرور',widget=forms.PasswordInput(attrs={'placeholder': '9 ارقام و احرف'}),min_length=8)
    password2=forms.CharField(label=' تاكيد كلمة المرور',widget=forms.PasswordInput(),min_length=9)

    class Meta:
        model=User
        fields=('username','email','first_name','last_name',
                'password1','password2',)
    def clean_password2(self):
        cd=self.cleaned_data
        if cd['password1']!=cd['password2']:
            raise forms.ValidationError('كلمة المرور غير متطابفة')
        return cd['password2']
    def clean_email(self):
        cd=self.cleaned_data
        if User.objects.filter(email=cd['email']).exists():
            raise forms.ValidationError('هذا البريد موجود بالفعل ')
        return cd['email']
class LoginForm(forms.ModelForm):
    username=forms.CharField(label='اسم المستخدم')
    password=forms.CharField(label=' كلمة المرور',widget=forms.PasswordInput())
    class Meta:
        model=User
        fields=('username','password')
class UserUpdateForm(forms.ModelForm):
    first_name=forms.CharField(label='الاسم الاول')
    last_name=forms.CharField(label='الاسم الثاني')
    email=forms.EmailField(label='البريد الاكتروني')
    class Meta:
        model=User
        fields=('first_name','last_name','email')
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=('image',)

