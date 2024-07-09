from quiz.views import *
from django.urls import path, include

app_name = 'quiz'
urlpatterns = [
    path('',test_view,name='index'),
    path('<int:qid>/', quiz_single, name='single'),
    path('result/<int:result_id>/', quiz_result, name='result'),
]