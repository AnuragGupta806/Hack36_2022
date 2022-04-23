from django.urls import path
from . import views

urlpatterns=[
    path('',views.home,name='news_home'),
    path('valiate/',views.validation_news,name='validation'),
    path('assign_role/',views.assign_role,name='assign_role')
]