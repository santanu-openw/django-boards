"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
#from django.contrib import admin
#from django.contrib.auth import views as auth_views
#from django.urls import path
#from boards import views
#from accounts import views as accounts_views
#from django.conf.urls import url



from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from django.urls import path

from accounts import views as accounts_views
from boards import views





urlpatterns = [
    #url(r'^$', views.home, name='home'),
    #url(r'^admin/', admin.site.urls),

   path('admin/', admin.site.urls),
   path('signup/', accounts_views.signup, name='signup'),
   path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
   path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
   path('logout/', auth_views.LogoutView.as_view(), name='logout'),
   url(r'^settings/account/$', accounts_views.UserUpdateView.as_view(), name='my_account'),
   #path('', views.home, name='home'),
   url(r'^$', views.BoardListView.as_view(), name='home'),
   #path('boards/<id>/', views.board_topics, name='board_topics'),
   url(r'^boards/(?P<pk>\d+)/$', views.TopicListView.as_view(), name='board_topics'),
   path('boards/<id>/new/', views.new_topic, name='new_topic'),
   path('boards/<id>/topics/<topic_id>', views.topic_posts, name='topic_posts'),
   path('boards/<id>/topics/<topic_id>/reply/', views.reply_topic, name='reply_topic'),
   
   url(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/posts/(?P<post_pk>\d+)/edit/$',
       views.PostUpdateView.as_view(), name='edit_post'),
   
   


   #path('boards/(?P<pk>\d+)/$', views.board_topics, name='board_topics'),
   #url(r'^boards/(?P<pk>\d+)/new/$', views.new_topic, name='new_topic'),
   # url(r'^boards/(?P<pk>\d+)/$', views.board_topics, name='board_topics'),
   #url(r'^signup/$', accounts_views.signup, name='signup'),
]
