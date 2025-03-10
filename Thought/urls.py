from django.urls import path
from . import views


urlpatterns = [path('',views.home, name='home'),
               path('profile_list/', views.profile_list, name ='profile_list'),
               path('profile/<int:pk>', views.profile, name='profile'),
               path('logout/', views.logout_user, name='logout'),
               path('login/', views.login_user, name='login'),
               path('register', views.register_user, name='register')
]