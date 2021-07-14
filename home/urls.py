from django.contrib import admin
from django.urls import path
from home import views
urlpatterns = [
    path('', views.index),
    path('add', views.addBlog),
    path('blog/<str:slug>', views.singleBlog),
    path('edit/<str:slug>', views.editBlog),
    path('delete/<int:id>', views.deleteBlog),
    path('login', views.userLogin),
    path('signup', views.userSignup),
    path('logout', views.userLogout),
    path('verify/<auth_token>', views.verify),
]
