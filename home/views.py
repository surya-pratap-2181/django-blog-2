from django.shortcuts import redirect, render
from home.models import Blog, MyUser
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.template.defaultfilters import slugify, title
import random

# Create your views here.


def index(request):
    data = Blog.objects.all()
    context = {"data": data}
    return render(request, "index.html", context)


def userLogin(request):
    try:
        if request.method == "POST":
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            # No backend authenticated the credentials
            messages.error(request, 'Invalid Credentials!!')
            return redirect('/')
    except:
        if request.user.is_anonymous:
            return redirect('/')
        else:
            return redirect("/")


# SignUp here


def userSignup(request):
    if request.method == "POST":
        email = request.POST['email']
        dob = request.POST['dob']
        fullname = request.POST['fullname']
        mobile = request.POST['mobile']
        password = request.POST['password']
        user = MyUser.objects.create_user(
            email=email, date_of_birth=dob, mobile=mobile, full_name=fullname, password=password)
        messages.success(request, 'User Created Successfully')
        login(request, user)
        return redirect('/')
    else:
        # No backend authenticated the credentials
        messages.error(request, 'Something Went Wrong')
        return redirect('/')


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
        messages.success(request, 'Your Blog Has been added!!')
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
