from django.shortcuts import render,redirect
from .forms import UserCreationForms,LoginForm,UserUpdateForm,ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from blog.models import Post,User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.core.mail import send_mail
from django.conf import settings



def register(request):
    if request.method == 'POST':
        form = UserCreationForms(request.POST)
        if form.is_valid():
            cleaned_email = form.cleaned_data['email']  
            form.clean_email()  

            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password1'])
            
            existing_user = User.objects.filter(email=new_user.email).first()
            if existing_user:
                messages.error(request, 'هذا البريد موجود بالفعل')
                return redirect('register')

            new_user.save()

            messages.success(request, f'لقد تمت عملية التسجيل بنجاح {new_user} مرحبا ')
            welcome_message = 'مرحبًا بكم في صفحة الدكتور ابو يعرب المروزقي'
            #email = cleaned_email  

            #send_mail(
             #   'الدكتور ابو يعرب المروزقي',
              #  welcome_message,
               # settings.EMAIL_HOST_USER,
                #[email],
                #fail_silently=False,
            #)

            return redirect('/')

    else:
        form = UserCreationForms()

    return render(request, 'user/register.html', {'title': 'التسجيل', 'form': form})
def login_user(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('profile')
        else:
                messages.warning(request,' اعادة اسم المستخدم او كلمة المرور')
    return render(request, 'user/login.html', {
        'title': 'تسجيل الدخول',
    })


def logout_user(request):
    logout(request)
    return redirect('/')

@login_required(login_url='login')
def profile(request):
    posts=Post.objects.filter(author=request.user)
    post_list=Post.objects.filter(author=request.user)
    paginator=Paginator(post_list,10)
    page=request.GET.get('page')
    try:
        post_list=paginator.page(page)
    except PageNotAnInteger:
            post_list=paginator.page(1)
    except EmptyPage:
         post_list=paginator.page(paginator.num_page)  
    return render(request,'user/profile.html',{  
        'title':'الملف الشخصي',
        'posts':posts,
        'page':page,
        'post_list':post_list,
     })
@login_required(login_url='login')
def profile_update(request):
    if request.method=='POST':
        user_form=UserUpdateForm(request.POST,instance=request.user)
        if user_form.is_valid() and profile_form.is_valid():
             user_form.save()
             profile_form.save()
             messages.success(request,'لقد تمت عملية التسجيل  بنجاح')
             return redirect('profile')
    else:
        user_form=UserUpdateForm(instance=request.user)
        profile_form=ProfileUpdateForm(instance=request.user.profile)
        return render (request,'user/profile_update.html',{
          'title':'تعديل الملف الشخصي',
          'user_form':user_form,
     })