from . import views
from .views import * 
from django.urls import path


app_name = 'blog'


urlpatterns = [

#    path('', HomePageView.as_view(), name='home'),
path('', post_list, name='home'),
path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
path('about/', AboutPageView.as_view(), name='about'),
path('contact/', ContactPageView.as_view(), name='contact'),
path('<int:post_id>/share/', views.post_share, name='post_share'),

  
    
]