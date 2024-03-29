from django.shortcuts import render,get_object_or_404,redirect
from .models import Post,video
from .forms import NewComment,PostCreateForm,VideoCreateForm
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.views.generic import CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse,HttpResponseRedirect
from django.urls import reverse 
import csv
from django.urls import resolve
def delete_video(request, video_id):
    video_instance = get_object_or_404(video, pk=video_id)
    if request.method == 'POST':
        video_instance.delete()
    return redirect('video')
def like_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user = request.user
    liked = False
    if user in post.likes.all():
        post.likes.remove(user)
        liked = False
    else:
        post.likes.add(user)
        liked = True
    total_likes = post.likes.count()

    return JsonResponse({'total_likes': total_likes, 'liked': liked})

def video_list(request):
    if request.method == 'POST': 
        form = VideoCreateForm(request.POST) 
        if form.is_valid():  
            form.save()  
            return redirect('video')  
    else:
        form = VideoCreateForm()  

    current_page = resolve(request.path_info).url_name
    
    # Fetch all videos
    videos = video.objects.all()

    # Handle search by video title
    video_title_search = request.GET.get('video_title_search')
    if video_title_search:
        videos = [video for video in videos if video.title.lower().find(video_title_search.lower()) != -1]

    # Pagination
    paginator = Paginator(videos, 2)
    page = request.GET.get('page', 1)  
    try:
        videos = paginator.page(page)
    except PageNotAnInteger:
        videos = paginator.page(1)
    except EmptyPage:
        videos = paginator.page(paginator.num_pages)

    context = {
        'title': 'فيديوهات',
        'videos': videos,
        'form': form,
        'current_page': current_page,
    }

    return render(request, 'blog/video.html', context)
def home(request):
    current_page = resolve(request.path_info).url_name     
    query = request.GET.get('video_title_search')
    posts = Post.objects.all()
    if query:
        posts = posts.filter(Q(title__icontains=query) | Q(content__icontains=query))
    paginator=Paginator(posts,10)
    page=request.GET.get('page')
    try:
        posts=paginator.page(page)
    except PageNotAnInteger:
            posts=paginator.page(1)
    except EmptyPage:
         posts=paginator.page(paginator.num_page)       
    context={'title':'الرئيسية',
             'posts':posts,
             'page':page,
             'current_page':current_page}
    return render(request,'blog/index.html',context)


def about(request):
    current_page = resolve(request.path_info).url_name     
    return render(request,'blog/about.html',{'title':'من هو أبو يعرب المرزوقي','current_page':current_page})

def post_detail(request,post_id):
    post=get_object_or_404(Post,pk=post_id)
    comments=post.comments.filter(active=True)
    comment_form=NewComment()
    New_Comment=None
    total_likes = post.total_likes()

    context={'title':post,
            'post':post,
            'comments':comments,
            'comment_form':comment_form,
            'total_likes':total_likes
            }
    if request.method=='POST':
        comment_form=NewComment(data=request.POST)
        if comment_form.is_valid():
            New_Comment=comment_form.save(commit=False)
            New_Comment.name = request.user.username
            New_Comment.post=post
            New_Comment.save()
            comment_form=NewComment()
    else:
        comment_form=NewComment()
    return render(request,'blog/detail.html',context)

def create_post_via_view(request):
    if request.user.is_authenticated:
        if request.user.email != 'abu-yaareb@moudawna.com':
            return redirect('/')
    from . import sync_posts
    try:
        with open('./data.csv', 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
                    
            for row in csv_reader:
                if len(row) >= 3:
                    title = row[0].strip()
                    content = row[1]
                    date = row[2].strip()
                    # Create a dictionary with the data for the form
                    data = {'title': title, 'content': content}
                    # Create an instance of the form with the provided data
                    form = PostCreateForm(data)
                    #check if the post alraedy exist
                    post = Post.objects.filter(title=title).first()
                    if post:    
                        #ignore the post if it already exist
                        continue   
                    # Check if the form is valid
                    if form.is_valid():
                        # Create a Post instance but don't save it yet
                        post_instance = form.save(commit=False)
                        # Set the author to the current user
                        post_instance.author = request.user
                        new_date = convert_date(date)
                        if new_date != None: 
                            post_instance.post_date = new_date 
                        # Save the Post instance
                        post_instance.save()
                    else:
                        # Print or log the errors if the form is not valid
                        print(f"Error creating post: {form.errors}")
            # Return a JSON response indicating success
            return redirect('/')
    except Exception as e:
        messages.error(request, "error oppening file")
        # Return a JSON response indicating failure with the error message
        return redirect('/')

from datetime import datetime

def convert_date(arabic_date):
    # Define a dictionary to map Arabic month names to their English counterparts
    arabic_to_english_month = {
        'يناير': 'January',
        'فبراير': 'February',
        'مارس': 'March',
        'إبريل': 'April',
        'أبريل':'April', # Add this line to handle the case where the Arabic letter 'إ' is replaced with 'أ
        'مايو': 'May',
        'يونيو': 'June',
        'يوليو': 'July',
        'أغسطس': 'August',
        'سبتمبر': 'September',
        'أكتوبر': 'October',
        'نوفمبر': 'November',
        'ديسمبر': 'December',
    }

    # Replace Arabic month names with English month names
    for arabic_month, english_month in arabic_to_english_month.items():
        arabic_date = arabic_date.replace(arabic_month, english_month)

    # Parse the date using the updated string, including the Arabic comma
    formatted_date = None

    try:
        parsed_date = datetime.strptime(arabic_date, "%d %B، %Y")
        formatted_date = parsed_date.strftime("%Y-%m-%d")
    except ValueError as e:
        print(f"Error: {e}")

    return formatted_date
          
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
          


