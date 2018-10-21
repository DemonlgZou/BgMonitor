from django.views.static import serve
from django.conf.urls import  url
from web_server.Views import views
from UGW_listen_demo import settings
urlpatterns = [
    url(r'index.html/',views.index,name='index'),
    url(r'staff.html/',views.staff,name='staff_add'),
    url(r'images.html/',views.images,name='images_list'),
    url(r'videos.html/',views.videos,name='video_add'),
    url(r'videos_watch.html/',views.videos_watch,name='video_watch'),
    url(r'user.html/',views.user,name='user_add'),
    url(r'host.html/',views.host,name='host_add'),
    url(r'log.html/',views.logs,name='log_list'),
    url(r'login.html/',views.login_on,name='login'),
    url(r'logout.html/',views.logout_out,name='logout'),
   # url(r'static/(?P<path>.*)$', serve, {"document_root": settings.STATIC_ROOT}),


]
