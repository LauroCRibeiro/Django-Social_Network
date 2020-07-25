from django.db import models
from django.utils.html import mark_safe

# Create your models here.
class Member(models.Model):
    full_name=models.CharField(max_length=200,default='')
    username=models.SlugField(max_length=300)
    email=models.EmailField(max_length=200)
    profile_img=models.ImageField(upload_to='profile_imgs/',blank=True)
    password=models.CharField(max_length=200)
    city=models.CharField(max_length=250,null=True,blank=True)
    state=models.CharField(max_length=300,null=True,blank=True)
    qualification=models.CharField(max_length=300,null=True,blank=True)
    work=models.TextField(null=True,blank=True)
    activate_status=models.BooleanField(default=True)
    reg_time=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name

# Post Data
class Post(models.Model):
    member_id=models.ForeignKey(Member,on_delete=models.CASCADE)
    post_content=models.TextField()
    post_image=models.ImageField(upload_to='post_imgs/',default='no')
    post_date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.post_content

    # Get Comments
    def comments(self):
        return self.comment_post.all().order_by('-id')

# Setting
class Setting(models.Model):
    login_banner=models.ImageField(upload_to='banner_imgs/')
    register_banner=models.ImageField(upload_to='banner_imgs/')

# Friends
class Friends(models.Model):
    member_id=models.ForeignKey(Member,on_delete=models.SET_NULL,related_name='member',null=True)
    friend_id=models.ForeignKey(Member,on_delete=models.SET_NULL,related_name='friend',null=True)
    friendship_date=models.DateTimeField(auto_now_add=True)
    accept_status=models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Friends"

# Comments
class Comment(models.Model):
    member_id=models.ForeignKey(Member,on_delete=models.SET_NULL,related_name='comment_member',null=True)
    post_id=models.ForeignKey(Post,on_delete=models.SET_NULL,related_name='comment_post',null=True)
    comment_body=models.TextField(default='',null=True)
    comment_time=models.DateTimeField(auto_now_add=True)
    comment_status=models.BooleanField(default=True)

# Likes
class Likes(models.Model):
    member_id=models.ForeignKey(Member,on_delete=models.SET_NULL,related_name='like_member',null=True)
    post_id=models.ForeignKey(Post,on_delete=models.SET_NULL,related_name='like_post',null=True)
    like_time=models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Likes"

# Notifications
class Notification(models.Model):
    member_id=models.ForeignKey(Member,on_delete=models.SET_NULL,related_name='notifications',null=True)
    receiver_id=models.ForeignKey(Member,on_delete=models.SET_NULL,related_name='notification_receiver',null=True)
    ref_id=models.IntegerField(null=True)
    ref_name=models.CharField(max_length=100,null=True)
    noti_content=models.CharField(max_length=300)
    read_status=models.BooleanField(default=True)

    