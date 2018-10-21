from django.views.static import serve
from  UGW_listen_demo import settings
from django.contrib import admin
from django.urls import path
from django.conf.urls import  url, include,handler404,handler500
from .settings import STATIC_ROOT
urlpatterns = [
   # path('admin/', admin.site.urls),
    url('^api/', include('api_server.urls')),
    url('^web/', include('web_server.urls')),
    url('^db/', include('DB_server.urls')),
    url(r'^images/(?P<path>.*)$', serve, {'document_root': r'D:\UGW_listen_demo\static\images'}),
    url(r'^videos/(?P<path>.*)$', serve, {'document_root': r'D:\UGW_listen_demo\static\video'}),
    url(r'^static/(?P<path>.*)$', serve, {"document_root":STATIC_ROOT}),

]
#handler404 = 'web_server.Views.views.page_not_found'
#handler500 = 'web_server.Views.views.server_wrong'