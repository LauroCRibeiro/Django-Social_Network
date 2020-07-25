from django.contrib import admin

# Register your models here.
from .models import *

class PostInline(admin.TabularInline):
    model=Post
# Show Comment in Post
class CommentInline(admin.TabularInline):
    model=Comment
# Show Likes
class LikeInline(admin.TabularInline):
    model=Likes
class MemberAdminModel(admin.ModelAdmin):
    list_display=('full_name','username','email','activate_status','reg_time')
    search_fields=('full_name','username')
    inlines=[PostInline]
admin.site.register(Member,MemberAdminModel)

class SettingAdminModel(admin.ModelAdmin):
    list_display=('id','login_banner','register_banner')
admin.site.register(Setting,SettingAdminModel)

class PostAdminModel(admin.ModelAdmin):
    list_display=('post_content','post_image')
    inlines=[CommentInline,LikeInline]
admin.site.register(Post,PostAdminModel)
# Friends Model
class FriendsAdminModel(admin.ModelAdmin):
    list_display=('member_id','friend_id','friendship_date')
admin.site.register(Friends,FriendsAdminModel)
# Comments Modal
class CommentAdminModel(admin.ModelAdmin):
    list_display=('member_id','post_id','comment_body')
admin.site.register(Comment,CommentAdminModel)
# Likes Modal
class LikeAdminModel(admin.ModelAdmin):
    list_display=('member_id','post_id')
admin.site.register(Likes,LikeAdminModel)

# Notification Modal
class NotificationAdminModel(admin.ModelAdmin):
    readonly_fields=('member_id','ref_id','ref_name','noti_content','read_status')
    list_display=('ref_name','member_id','receiver_id','noti_content')
admin.site.register(Notification,NotificationAdminModel)
