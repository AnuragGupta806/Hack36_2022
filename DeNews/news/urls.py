from django.urls import path
from . import views

urlpatterns=[
    path('',views.home,name='news_home'),
    path('validate_news/',views.validation_news,name='validation'),
    path('assign_role/',views.assign_role,name='assign_role'),
    path('assign_news/',views.assign_news,name='assign_news'),
    path('validate/<int:id>/<int:nid>/',views.validate,name='validate'),
    path('report/<int:nid>/',views.report,name='report'),
    path('reader/',views.readerView,name='reader'),
    path('validators/',views.validatorView,name='validator'),
    path('publisher/',views.publisherView,name='publisher'),
    path('creator/',views.creatorView,name='creator'),
    path('publisher/createNews',views.createNews,name='create_news'),
]