from django.contrib import admin
from django.urls import path
from home import views
urlpatterns = [
    path('', views.index, name='home'),
    path('contact/', views.contact, name='contact'),
    path('add/', views.addBlog, name='add'),
    path('blog/<str:slug>/', views.singleBlog, name='blog'),
    path('edit/<str:slug>/', views.editBlog, name='blogedit'),
    path('delete/<int:id>/', views.deleteBlog, name='blogdelete'),
    path('login/', views.userLogin, name='login'),
    path('signup/', views.userSignup, name='signup'),
    path('logout/', views.userLogout, name='logout'),
    path('verify/<auth_token>', views.verify),
]
