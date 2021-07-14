from django.shortcuts import redirect, render
from home.models import Blog, MyUser
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.template.defaultfilters import slugify, title
import random
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required


# Create your views here.


def index(request):
    data = Blog.objects.all()
    context = {"data": data}
    return render(request, "index.html", context)


# def userLogin(request):
#     try:
#         if request.method == "POST":
#             email = request.POST['email']
#             password = request.POST['password']
#             user = authenticate(username=email, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect("/")
#         else:
#             # No backend authenticated the credentials
#             messages.error(request, 'Invalid Credentials!!')
#             return redirect('/')
#     except:
#         if request.user.is_anonymous:
#             return redirect('/')
#         else:
#             return redirect("/")


def userLogin(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_obj = MyUser.objects.filter(email=email).first()
        if user_obj is None:
            messages.info(request, 'User not found.')
            return redirect('/')
        # profile_obj = Profile.objects.filter(user=user_obj).first()
        if not user_obj.is_verified:
            messages.info(
                request, 'Your Account is not verified!! Check Your Mail')
            return redirect('/')
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Invalid Credentials!!')
            return redirect('/')
    return render(request, '/')

# SignUp here


def userSignup(request):
    if request.method == "POST":
        email = request.POST['email']
        dob = request.POST['dob']
        fullname = request.POST['fullname']
        mobile = request.POST['mobile']
        password = request.POST['password']
        auth_token = str(uuid.uuid4())
        print(auth_token)
        user_obj = MyUser.objects.filter(email=email).first()
        if user_obj:
            messages.error(request, 'Email Already Exists')
            return redirect('/')
        user = MyUser.objects.create_user(
            email=email, date_of_birth=dob, mobile=mobile, auth_token=auth_token, full_name=fullname, password=password)
        send_mail_after_registration(email, auth_token)
        messages.success(
            request, 'We have sent you an email!! Please Check Your email and verify Your account')
        return redirect('/')
        # messages.success(request, 'SignUp Successful')
        # login(request, user)
        # return redirect('/')
    else:
        # No backend authenticated the credentials
        messages.error(request, 'Something Went Wrong')
        return redirect('/')


def verify(request, auth_token):
    user_obj = MyUser.objects.filter(auth_token=auth_token).first()
    if user_obj:
        if user_obj.is_verified:
            messages.info(request, 'You were already Verified')
            return redirect("/")
        user_obj.is_verified = True
        user_obj.save()
        messages.success(request, 'Your Account is Verified!! Login Now')
        return redirect('/')


def send_mail_after_registration(email, token):
    subject = 'Your accounts need to be verified'
    message = f'Hi, Click the link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)


def userLogout(request):
    logout(request)
    return redirect('/')


def addBlog(request):
    if request.user.is_anonymous:
        return redirect('/')
    if request.method == "POST":
        title = request.POST['title']
        desc = request.POST['desc']
        title_slug = slugify(title)
        existing_slug = Blog.objects.filter(title_slug=title_slug).exists()
        if existing_slug:
            title_slug = title_slug + str(random.randint(0, 9999))
        # user = request.POST['user']
        user = request.user
        new = Blog(title=title, desc=desc, title_slug=title_slug, user=user)
        new.save()
        messages.success(request, 'Your Blog is added Successfully!!')
        return redirect('/')
    return render(request, "add.html")


def singleBlog(request, slug):
    blog = Blog.objects.get(title_slug=slug)
    data = {'data': blog}
    return render(request, 'blog.html', data)


def editBlog(request, slug):
    if request.user.is_anonymous:
        return redirect('/')
    edit = Blog.objects.get(title_slug=slug)
    if request.method == "POST":
        edit.title = request.POST['title']
        edit.desc = request.POST['desc']
        edit.save()
        messages.success(request, 'Your Blog Has been Edited Successfully!!')
        return redirect('/')
    return render(request, "edit.html", {'data': edit})


def deleteBlog(request, id):
    if request.user.is_anonymous:
        return redirect('/')
    data = Blog.objects.get(id=id)
    data.delete()
    messages.error(request, "Blog Deleted Successfully!!")
    return redirect('/')
