from django.shortcuts import render,get_object_or_404
from .models import Post,video
from .forms import NewComment,PostCreateForm,VideoCreateForm
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.views.generic import CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.db.models import Q

     
def video_list(request):
    videos = video.objects.all()
    paginator = Paginator(videos, 1)
    page = request.GET.get('page', 1)  # Default to page 1 if not specified
    form = VideoCreateForm()

    try:
        videos = paginator.page(page)
    except PageNotAnInteger:
        videos = paginator.page(1)
    except EmptyPage:
        videos = paginator.page(paginator.num_pages)

    context = {
        'videos': videos,
        'form': form,
    }

    return render(request, 'blog/video.html', context)
def home(request):
    query = request.GET.get('post_search')
    posts = Post.objects.all()
    if query:
        posts = posts.filter(Q(title__icontains=query) | Q(content__icontains=query))
    paginator=Paginator(posts,2)
    page=request.GET.get('page')
    try:
        posts=paginator.page(page)
    except PageNotAnInteger:
            posts=paginator.page(1)
    except EmptyPage:
         posts=paginator.page(paginator.num_page)       
    context={'title':'الصفحة ',
             'posts':posts,
             'page':page,}
    return render(request,'blog/index.html',context)


def about(request):
    return render(request,'blog/about.html',{'title':'من انا'})


def post_detail(request,post_id):
    post=get_object_or_404(Post,pk=post_id)
    comments=post.comments.filter(active=True)
    comment_form=NewComment()
    New_Comment=None
    context={'title':post,
            'post':post,
            'comments':comments,
            'comment_form':comment_form,
            }
    if request.method=='POST':
        comment_form=NewComment(data=request.POST)
        if comment_form.is_valid():
            New_Comment=comment_form.save(commit=False)
            New_Comment.post=post
            New_Comment.save()
            comment_form=NewComment()
    else:
        comment_form=NewComment()
    return render(request,'blog/detail.html',context)
class POstCreateView(LoginRequiredMixin,CreateView):
     model=Post
     #fields=['title','content']
     template_name='blog/new_post.html'
     form_class=PostCreateForm

     def form_valid(self,form):
          form.instance.author=self.request.user
          return super().form_valid(form)
class POstUpdateView(UserPassesTestMixin,LoginRequiredMixin,UpdateView):
     model=Post
     #fields=['title','content']
     template_name='blog/new_post.html'
     form_class=PostCreateForm

     def form_valid(self,form):
          form.instance.author=self.request.user
          return super().form_valid(form)
     
     def test_func(self) :
          post=self.get_object()
          if self.request.user == post.author:
               return True
          else:
               return False
class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
     model=Post 
     success_url='/'
     def test_func(self) :
          post=self.get_object()
          if self.request.user == post.author:
               return True
          else:
               return False
          

