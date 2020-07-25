from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns=[
    path('',views.home,name='home'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('register/',views.register,name='register'),
    path('profile/',views.profile,name='profile'),
    path('update-profile-detail',views.update_profile_detail,name='update-profile-detail'),
    path('update-password',views.update_password,name='update-password'),
    path('friends/',views.friends,name='friends'),
    path('notifications/',views.notification,name='notifications'),

    # Create Member
    path('create-member',views.create_member,name='create-member'),
    # Member Login
    path('member-login',views.member_login,name='member-login'),
    # Create Post
    path('create-post',views.create_post,name='create-post'),
    # Create Post
    path('create-post-with-image',views.create_post_with_image,name='create-post-with-image'),
    # Update Profile Image
    path('update-profile-image',views.update_profile_image,name='update-profile-image'),
    # Ajax Search
    path('search',views.ajax_search,name='search'),
    # Member Detail
    path('member/<slug:username>/<int:id>',views.member_detail,name='member-detail'),
    # Add Friend
    path('add-friend',views.add_friend,name='add-friend'),
    path('delete-friend',views.delete_friend,name='delete-friend'),
    path('friend/friends/<int:id>',views.friend_friends,name='friend-friends'),
    # Post Comments
    path('post-comment',views.post_comment,name='post-comment'),
    # Post Likes
    path('post-like',views.post_like,name='post-like'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
