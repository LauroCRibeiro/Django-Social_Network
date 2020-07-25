from django.shortcuts import render,HttpResponse,redirect
from django.contrib import messages
from django.core import serializers
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from .models import *
import json
def home(request):
    if 'loginMember' in request.session:
        decoded_data=json.loads(request.session['memberData'])
        member_id=decoded_data[0]['pk']
        member=Member.objects.get(pk=member_id)
    else:
        return redirect('login')
    posts=Post.objects.select_related('member_id').order_by('-id')
    return render(request,'home.html',{'member':member,'posts':posts})

# Create Post
def create_post(request):
    if 'loginMember' in request.session:
        if request.method=='POST':
            decoded_data=json.loads(request.session['memberData'])
            member_id=decoded_data[0]['pk']
            member=Member.objects.get(pk=member_id)
            post_content=request.POST['post_content']
            post=Post.objects.create(member_id=member,post_content=post_content)
            messages.success(request,'Post has been shared successfully.')
            return redirect('/')
        else:
            return HttpResponse('Invalid response!!')
    else:
        return redirect('login')

# Create Post With Image
def create_post_with_image(request):
    if 'loginMember' in request.session:
        if request.method=='POST':
            decoded_data=json.loads(request.session['memberData'])
            member_id=decoded_data[0]['pk']
            member=Member.objects.get(pk=member_id)
            post_content=request.POST['post_content']
            post_img = request.FILES['post_image']
            fs=FileSystemStorage(location='media/post_imgs/')
            filename=fs.save(post_img.name,post_img)
            # uploaded_file_url=fs.url(filename)
            post=Post.objects.create(member_id=member,post_content=post_content,post_image=filename)
            messages.success(request,'Post has been shared successfully.')
            return redirect('/')
        else:
            return HttpResponse('Invalid response!!')
    else:
        return redirect('login')

def login(request):
    settings=Setting.objects.first()
    return render(request,'login.html',{'settings':settings})

def register(request):
    settings=Setting.objects.first()
    return render(request,'register.html',{'settings':settings})

# Profile
def profile(request):
    if 'loginMember' in request.session:
        decoded_data=json.loads(request.session['memberData'])
        member_id=decoded_data[0]['pk']
        member=Member.objects.get(pk=member_id)
        return render(request,'profile.html',{'member':member})
    else:
        return redirect('login')

# Friends
def friends(request):
    if 'loginMember' in request.session:
        decoded_data=json.loads(request.session['memberData'])
        member_id=decoded_data[0]['pk']
        friends=Friends.objects.filter(Q(member_id=member_id)|Q(friend_id=member_id)).order_by('-id')
        member=Member.objects.get(pk=member_id)
        return render(request,'friends.html',{'friends':friends,'member':member})
    else:
        return redirect('login')

# Notification
def notification(request):
    if 'loginMember' in request.session:
        decoded_data=json.loads(request.session['memberData'])
        member_id=decoded_data[0]['pk']
        member=Member.objects.get(pk=member_id)
    else:
        return redirect('login')
    notifications=Notification.objects.filter(receiver_id=member).order_by('-id')
    return render(request,'notification.html',{'notifications':notifications,'member':member})

# Create Member
def create_member(request):
    if request.method=='POST':
        full_name=request.POST['fname']
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        thread=Member.objects.create(full_name=full_name,username=username,email=email,password=password)
        messages.success(request,'You have been registered successfully.')
        return redirect('register')
    else:
        return HttpResponse('Invalid Request!!')

# Member Login
def member_login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        member=Member.objects.filter(username=username,password=password,activate_status=True).count()
        if member>0:
            member=Member.objects.filter(username=username,password=password,activate_status=True)
            request.session['loginMember']=True
            request.session['memberData']=serializers.serialize('json',member)
            return redirect('/')
        else:
            messages.error(request,'Invalid Username/Password!!')
            return redirect('login')
    else:
        return HttpResponse('Invalid Request!!')

# Member Logout
def logout(request):
    del request.session['loginMember']
    del request.session['memberData']
    return redirect('login')

# Ajax Search
def ajax_search(request):
    if request.method=='POST':
        searchStr=request.POST['search']
        decoded_data=json.loads(request.session['memberData'])
        member_id=decoded_data[0]['pk']
        searchResult=Member.objects.filter(full_name__icontains=searchStr).exclude(pk=member_id).order_by('-id')
        if(searchResult.count()>0):
            data={
                'bool':True,
                'result':serializers.serialize('json',searchResult),
                'totalResult':searchResult.count()
            }
        else:
            data={
                'bool':False
            }
        return JsonResponse(data)

# Update Profile Image
def update_profile_image(request):
    if 'loginMember' in request.session:
        if request.method=='POST':
            decoded_data=json.loads(request.session['memberData'])
            member_id=decoded_data[0]['pk']
            member=Member.objects.get(pk=member_id)
            profile_img = request.FILES['profile_img']
            fs=FileSystemStorage(location='media/profile_imgs/')
            filename=fs.save(profile_img.name,profile_img)
            # uploaded_file_url=fs.url(filename)
            post=Member.objects.filter(id=member_id).update(profile_img='profile_imgs/'+filename)
            messages.success(request,'Profile has been update successfully.')
            return redirect('/profile')
        else:
            return HttpResponse('Invalid response!!')
    else:
        return redirect('profile')

# Update Profile Detail
def update_profile_detail(request):
    if 'loginMember' in request.session:
        if request.method=='POST':
            decoded_data=json.loads(request.session['memberData'])
            member_id=decoded_data[0]['pk']
            member=Member.objects.get(pk=member_id)
            full_name=request.POST['full_name']
            email=request.POST['email']
            city=request.POST['city']
            state=request.POST['state']
            quali=request.POST['quali']
            work=request.POST['work']
            member=Member.objects.filter(id=member_id).update(
                full_name=full_name,
                email=email,
                city=city,
                state=state,
                qualification=quali,
                work=work
            )
            messages.success(request,'Profile has been update successfully.')
            return redirect('/profile')
        else:
            return HttpResponse('Invalid response!!')
    else:
        return redirect('profile')

# Member Detail
def member_detail(request,username,id):
    friend_status=False
    if 'loginMember' in request.session:
        decoded_data=json.loads(request.session['memberData'])
        member_id=decoded_data[0]['pk']
        member=Member.objects.get(pk=id)
        # Check member if friend of logged in user or not
        check=Friends.objects.filter(Q(member_id=member_id,friend_id=id) | Q(member_id=id,friend_id=member_id)).count()
        if(check>0):
            friend_status=True
    else:
        return redirect('login')
    posts=Post.objects.select_related('member_id').filter(member_id=id).order_by('-id')
    return render(request,'member-detail.html',{'member':member,'posts':posts,'friend_status':friend_status,'member_id':member_id})

# Update Password
def update_password(request):
    if 'loginMember' in request.session:
        if request.method=='POST':
            decoded_data=json.loads(request.session['memberData'])
            member_id=decoded_data[0]['pk']
            member=Member.objects.get(pk=member_id)
            new_password=request.POST['new_password']
            member=Member.objects.filter(id=member_id).update(password=new_password)
            messages.success(request,'Password has been changed!!')
            return redirect('/logout')
        else:
            return HttpResponse('Invalid response!!')
    else:
        return redirect('profile')

# Add Friend
def add_friend(request):
    if request.method=='POST':
        member_id=Member.objects.get(pk=request.POST['member_id'])
        friend_id=Member.objects.get(pk=request.POST['friend_id'])
        check=Friends.objects.filter(member_id=member_id,friend_id=friend_id).count()
        if check > 0:
            data={
                'bool':False
            }
        else:
            Friends.objects.create(member_id=member_id,friend_id=friend_id)
            # Create Notification When Like Post
            noti_content=member_id.full_name+' sent you friend request'
            Notification.objects.create(member_id=member_id,receiver_id=friend_id,ref_id=request.POST['friend_id'],noti_content=noti_content,ref_name='friend_request')
            data={
                'bool':True
            }
        return JsonResponse(data)

# Delete Friend
def delete_friend(request):
    if request.method=='POST':
        member_id=Member.objects.get(pk=request.POST['member_id'])
        friend_id=Member.objects.get(pk=request.POST['friend_id'])
        check=Friends.objects.filter(member_id=member_id,friend_id=friend_id).count()
        if check > 0:
            Friends.objects.filter(member_id=member_id,friend_id=friend_id).delete()
            # Create Notification When Like Post
            noti_content=member_id.full_name+' delete friendship'
            Notification.objects.create(member_id=member_id,receiver_id=friend_id,ref_id=request.POST['friend_id'],noti_content=noti_content,ref_name='cancel_friend')
            data={
                'bool':True
            }
        else:
            data={
                'bool':False
            }
        return JsonResponse(data)

# Friends of Friend
def friend_friends(request,id):
    if 'loginMember' in request.session:
        decoded_data=json.loads(request.session['memberData'])
        member_id=decoded_data[0]['pk']
        friends=Friends.objects.filter(member_id=id).exclude(friend_id=member_id)
        member=Member.objects.get(pk=id)
        return render(request,'friends.html',{'friends':friends,'member':member})
    else:
        return redirect('login')

# Post Comments
def post_comment(request):
    if request.method=='POST':
        member_id=Member.objects.get(pk=request.POST['member_id'])
        comment=request.POST['comment']
        post=Post.objects.get(pk=request.POST['post_id'])
        receiver=Member.objects.get(pk=request.POST['receiver_id'])
        comment=Comment.objects.create(post_id=post,member_id=member_id,comment_body=comment)
        # Create Notification When Create Comment
        # Create Notification When Like Post
        noti_content=member_id.full_name+' commented on your post'
        Notification.objects.create(member_id=member_id,receiver_id=receiver,ref_id=request.POST['post_id'],noti_content=noti_content,ref_name='comment')
        comments=Comment.objects.filter(post_id=request.POST.get('post_id')).order_by('-id')
        if comment:
            data={
                'bool':True,
                'comments':serializers.serialize('json',comments),
            }
        else:
            data={
                'bool':False,
                'comments':serializers.serialize('json',comments),
            }
        return JsonResponse(data)

# Post Like
def post_like(request):
    if request.method=='POST':
        member_id=Member.objects.get(pk=request.POST['member_id'])
        post=Post.objects.get(pk=request.POST['post_id'])
        check=Likes.objects.filter(post_id=post,member_id=member_id).count()
        if check>0:
            Likes.objects.filter(post_id=post,member_id=member_id).delete()
            totalLikes=Likes.objects.filter(post_id=post).count()
            data={
                'bool':False,
                'totalLikes':totalLikes
            }
        else:
            Likes.objects.create(post_id=post,member_id=member_id)
            # Create Notification When Like Post
            noti_content=member_id.full_name+' liked your post'
            receiver=Member.objects.get(pk=request.POST['receiver_id'])
            Notification.objects.create(member_id=member_id,receiver_id=receiver,ref_id=request.POST['post_id'],noti_content=noti_content,ref_name='like')
            totalLikes=Likes.objects.filter(post_id=post).count()
            data={
                'bool':True,
                'totalLikes':totalLikes
            }
        return JsonResponse(data)


