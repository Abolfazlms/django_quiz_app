from django.urls import path
from . import views

app_name = 'account' 
urlpatterns = [
    #login
    path('login/',views.login_view, name='login'),
    #logout
    path('logout',views.logout_view, name='logout'),
    #register
    path('signup/',views.signup_view, name='signup'),
]