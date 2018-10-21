from django.shortcuts import render, redirect,HttpResponseRedirect
import datetime
from django.contrib.auth import  login,logout,authenticate
from DB_server.models import *


class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)


def auth(func):
    #负责做用户登陆认证的方法
    def inner(request,*args,**kwargs):
        request.session.clear_expired()
        try:
            print (request.session.exists(request.COOKIES['sessionid']))
            if   request.session.exists(request.COOKIES['sessionid']) is False:

                return redirect('/web/login.html')
            else:

                return func (request,*args,**kwargs)
        except KeyError:
            return redirect('/web/login.html')
    return  inner


top = Menu.objects.filter(top='1')
child = Menu.objects.filter(child='1')
menu_list ={'top':top,'child':child}

@auth
def index(request):
    return render(request,'index.html',menu_list)

@auth
def user(request):

   return render(request,'user.html',menu_list)

@auth
def images(request):

   return  render(request,'images.html',menu_list)

@auth
def staff(request):
   return  render(request,'staff.html',menu_list)

@auth
def host(request):
   return  render(request,'host.html',menu_list)

@auth
def videos(request):
   return  render(request,'videos.html',menu_list)

@auth
def videos_watch(request):
   return  render(request,'videos_watch.html',menu_list)

@auth
def logs(request):
   return  render(request,'log.html',menu_list)

def login_on(request):
    if request.method == 'GET':
        request.session['login_from'] = request.META.get('HTTP_REFERER', '/')

    elif    request.method == 'POST':
            user1 = request.POST.get('username')
            pwd =request.POST.get('password')
           # print(user1,pwd)
            user = authenticate(request,username=user1,password=pwd)
            #print(user)
            if user is not None:
               login(request,user)
               return HttpResponseRedirect('/web/index.html')
    return render(request,'login.html')


def page_not_found(request):
    return render(request,'error-404.html')

def server_wrong(request):
    return render(request,'error-500.html')

def logout_out(request):
    logout(request)
    return render(request,'logout.html')