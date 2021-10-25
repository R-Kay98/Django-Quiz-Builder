"""djtest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from django.urls import path, include
from users import views as user_views

urlpatterns = [
	path('admin/', admin.site.urls),
	path('register/', user_views.register, name='register'),
	path('profile/', user_views.profile, name='profile'),
	path('profile/deletequiz/<str:parameter>', user_views.delete_quiz, name='deletequiz'),
	path('profile/create/deletequestion/<str:parameter>', user_views.delete_question, name='deletequestion'),
	path('profile/create/', user_views.choose_question, name='choose_question'),
	path('profile/create/multiplechoice/<str:parameter>', user_views.new_mc_question, name='multiplechoice'),
	path('profile/create/multiplechoice/complete/', user_views.mc_complete, name='mc_complete'),
	path('profile/create/shortanswer/<str:parameter>', user_views.new_sa_question, name='shortanswer'),
	path('profile/create/shortanswer/complete/', user_views.sa_complete, name='sa_complete'),
	path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
	path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
	path('', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
	path('profile/startquiz/', user_views.start_quiz, name='start_quiz'),
]
