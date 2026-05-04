from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('analyze/', views.analyze_resume, name='analyze'),
    path('gemini/', views.gemini_suggestions, name='gemini'),
    path('login/', views.login_page, name='login'),
    path('signup/', views.signup_page, name='signup'),
    path('launch/', views.launch_page, name='launch'),
    path('logout/', views.logout_page, name='logout'),
]

