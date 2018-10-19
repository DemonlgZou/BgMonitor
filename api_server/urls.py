
from django.contrib import admin
from django.urls import path
from api_server import views
from django.conf.urls import  url, include
urlpatterns = [
		url(r'^upload_images/',views.upload_images),
		#url(r'^create_videos/',views.file2video),
		url(r'image_list/',views.image_list),
		url(r'^create_videos/',views.create_videos),
		url(r'^video_list/',views.video_list),

]
