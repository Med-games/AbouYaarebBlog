from django.urls import path
from . import views
urlpatterns=[
    path('',views.home,name='home'),
    path('about/',views.about,name='about'),
    path('detail/<int:post_id>',views.post_detail,name='detail'),
    path('new_post',views.POstCreateView.as_view(), name='new_post'),
    path('detail/<slug:pk>/update/',views.POstUpdateView.as_view(), name='update_post'),
    path('detail/<slug:pk>/delete/',views.PostDeleteView.as_view(), name='delete_post'),
    path('video/',views.video_list,name='video'),
    path('create-post', views.create_post_via_view, name='create_post'),
    path('like/<int:pk>/', views.like_view, name='like_post'),


]