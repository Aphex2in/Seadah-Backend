"""
URL configuration for saedah project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from saedah import views
from django.conf import settings
from django.conf.urls.static import static
from .views import register_user, user_login, user_logout, user_profile

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.home_deals, name='home_deals'),
    path('users/', views.user_list),
    path('deals/', views.deals_list),
    path('deal/<int:id>', views.deal_detail),
    path('deal/<int:id>/upvote/', views.upvote_deal, name='upvote_deal'),
    path('deal/<int:id>/downvote/', views.downvote_deal, name='downvote_deal'),
    path('deal/<int:id>/like/', views.like_deal, name='like_deal'),
    path('search/', views.search_deals, name='search_deals'),
    path('register/', register_user, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('profile/', user_profile, name='profile'),
    path('profile/<int:id>', views.profile_detail),
    path('profile/<int:id>/deals/', views.profile_deals),
    path('profile/<int:id>/follow/', views.follow_or_unfollow_profile, name='follow_or_unfollow_profile'),
    path('profile/<int:id>/followers/', views.user_followers, name='user_followers'),
    path('profile/<int:id>/followings/', views.user_followings, name='user_followings'),
    path('profile/uploadimage/', views.upload_user_image, name='upload_user_image'),
    path('deal/<int:id>/comment/', views.comment_on_deal, name='comment_on_deal'),
    path('comment/<int:id>', views.comment_removeoredit, name='comment_removeoredit'),
    path('profile/<int:id>/show_comments/', views.show_user_comments, name='show_user_comments')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)