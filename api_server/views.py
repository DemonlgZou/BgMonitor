from django.shortcuts import render,HttpResponse
from DB_server.models import *
from DB_server import form
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.
from django.core import  serializers
from PIL import  Image,ImageChops
from django.shortcuts import render, HttpResponse
import os, cv2, json,subprocess,datetime
from DB_server.models import *
from django.db.models.signals import  post_save
import uuid,threading,os

class CJsonEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, datetime.datetime):
			return obj.strftime('%Y-%m-%d %H:%M:%S')
		elif isinstance(obj, datetime):
			return obj.strftime("%Y-%m-%d")
		else:
			return json.JSONEncoder.default(self, obj)

abs_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
static_path = os.path.join('static', 'images',)
img_save_path = os.path.join(abs_path,static_path)
video_save_path = os.path.join(abs_path,'static','video')
###分页展示###
def page(list,no,page):
	#list 数据查询出来的结果类型是 jquery[list],no是行数，page代表页数
	paginator = Paginator(list,no)
	try:
		info = paginator.page(page)

	except PageNotAnInteger:
		info = paginator.page(1)
	except EmptyPage:
		info = paginator.page(paginator.num_pages)

	return {"page":page,"total":paginator.num_pages,'data':info}


def file2video(px,length,weidth,pic_list,videos_name):
	#操作图片与视频转换的方法
		fps = int(px)
		fourcc = cv2.VideoWriter_fourcc('D', 'I', 'V', 'X')
		vi = cv2.VideoWriter(videos_name, fourcc, fps, (length, weidth))  # 这里的 数据后续要从数据库里面读取
		for i in pic_list:
			new = os.path.join(img_save_path, os.path.basename(i.path))
			img = cv2.imread(new)
			vi.write(img)
		vi.release()
		Video.objects.filter(video_path=videos_name).update(stat='created',size=os.stat(videos_name).st_size)

def upload_images(request):
	#接收client主机上agent软件发送来的主机信息和图片
	if request.method == 'POST':
		obj_file = request.FILES.get('file')

		#接收来自agent相关信息必要的参数如下，缺一均不会进行下步操作
		if request.POST.get('os') and request.POST.get('ip') and \
			  request.POST.get('user')and  request.POST.get('host_name') and\
			  request.POST.get('created_at')and request.POST.get('length')\
			  and request.POST.get('width') and request.POST.get('file_size'):

			info_created_time = request.POST.get('created_at')
			#通过接收前端信息去后台数据匹配员工和主机是否存在，不存在则写入到后台数据库，存在则进行下一步操作
			obj1 = Staff.objects.filter(No=request.POST.get('user')).first()
			if obj1 == None :
				User = Staff.objects.create(No=request.POST.get('user'),create_at=info_created_time)
				User.save()
			obj2 = Host.objects.filter(name=request.POST.get('host_name')).first()
			if obj2 == None:
				Host.objects.create(name=request.POST.get('host_name'),ip=request.POST.get('ip'),host_type=request.POST.get('os'))
			Host_id = Host.objects.get(name=request.POST.get('host_name')) #获取主机ID值
			User_id = Staff.objects.get(No=request.POST.get('user')) #获取用户ID值
			#判断静态文件目录是否存在，不存在创建
			if os.path.isdir(img_save_path) is False:
				subprocess.run('md %s'%img_save_path,shell=True)   #dos 创建文件夹 md,unxi是 mkdir
			#接收前端发送来的图片
			f = open(os.path.join(img_save_path, obj_file.name), 'wb')
			for chunk in obj_file.chunks():
				f.write(chunk)
			f.close()
			images = IMages.objects.last()  # 获取图片表里面的最后条数据，与当前传来的图片进行对比判断图片是否重复，重复则不写入后台
			if images != None:
				a = Image.open(images.asb_path)
				new_pic = os.path.join(img_save_path,obj_file.name)
				b = Image.open(new_pic)
				diff = ImageChops.difference(a,b)
				if diff.getbbox() is None:
					subprocess.run('del %s'%new_pic,shell=True)
				else:
					obj = IMages.objects.create(path=os.path.join(static_path, obj_file.name),
												size=request.POST.get('file_size'),
												length=request.POST.get('length'), width=request.POST.get('width'),
												create_at=request.POST.get('created_at'), host_id=Host_id.id,
												user_id=User_id.id,asb_path=os.path.join(img_save_path, obj_file.name),name=obj_file.name)
					obj.save()
			else:
				obj = IMages.objects.create(path=os.path.join(static_path, obj_file.name),
										size=request.POST.get('file_size'),
										length=request.POST.get('length'), width=request.POST.get('width'),
										create_at=request.POST.get('created_at'), host_id=Host_id.id,
										user_id=User_id.id,asb_path=os.path.join(img_save_path, obj_file.name),name=obj_file.name)
				obj.save()
			info = json.dumps({'code': 1, 'data': 'success'})
			return HttpResponse(info)
	else:
			return HttpResponse('erorr')



def image_list(request):
	#向前端发送展示图片信息的接口文件
	new_data = []
	t = 1 #计数
	Page = request.POST.get('page') if request.POST.get('page') else 1 #取前端传来的页面值，没传则为1
	row = request.POST.get('rows') if request.POST.get('rows') else 10 #取前端传来的每页行数值，没传则为10
	if request.POST.get('_search') == 'true':
			pass

	else:
		obj = page(IMages.objects.all(),row,Page)
		records = IMages.objects.count() #查询最大数据的条数
	#处理返回给前端的数据
		for i in obj.get('data'):
			if i != None:
				#print(i)
				No = i.user.No ##员工号
				host = '%s+%s'%(i.host.name,i.host.ip)  #登陆主机
				px = "%s*%s"%(i.length,i.width) #像素
				name = i.name  #图片名
				id = t    #id
				created_at = str(i.create_at)  #生成时间
				size = str(i.size) #图片大小
				new_data.append({'id':id,"No":No,"host":host,"px":px,'created':created_at,"size":size,"name":name})
				t +=1
		obj.pop('data')
		obj.update({'rows':new_data,'records':records})
		return HttpResponse(json.dumps(obj), content_type="application/json")

def create_videos(request):
	#生成报告
	No = request.POST.get('No')
	host = request.POST.get('host')
	ip = request.POST.get('ip')
	start = request.POST.get('start')
	end = request.POST.get('end')
	px = request.POST.get('px')
	staff_id = Staff.objects.filter(No=No).first()
	if staff_id:
		obj= Staff.objects.get(id=staff_id.id).User.first()
		if No and host and ip and start and end and px:
			obj_user = Staff.objects.filter(No=No).first()
			obj_host = Host.objects.filter(name=host,ip=ip).first()
			obj_img = IMages.objects.filter(user_id=obj_user.id,host_id=obj_host.id).filter(create_at__range=(start,end))
			videos_name = str(uuid.uuid1()).replace('-','')
			file_name = os.path.join(video_save_path, videos_name+'.mp4')
			if obj_img :
				Video.objects.create(user_id=obj_user.id,host_id=obj_host.id,stat='generated',start_at=start,end_at=end,video_path=file_name,url=videos_name)
				t = threading.Thread(target=file2video,args=(px,obj.length,obj.width,obj_img,file_name,))
				t.start()
				return HttpResponse(json.dumps({'msg':{'sucess':'ok'}}),content_type="application/json")
			else:
				return HttpResponse()
	return HttpResponse(json.dumps({'msg':{'error':'ok'}}),content_type="application/json")

def video_list(request):
	#展示视频信息内容#
	if request.method =="POST":
			print(request.POST.get('_search'))
			print(request.POST.get('filters'))
			new_data = []
			t = 1  # 计数
			Page = request.POST.get('page') if request.POST.get('page') else 1  # 取前端传来的页面值，没传则为1
			row = request.POST.get('rows') if request.POST.get('rows') else 10  # 取前端传来的每页行数值，没传则为10
			obj = page(Video.objects.all(), row, Page)
			records = Video.objects.count()  # 查询最大数据的条数
			# 处理返回给前端的数据
			for i in obj.get('data'):
				if i != None:
					No = i.user.No  ##员工号
					host = '%s+%s' % (i.host.name, i.host.ip)  # 登陆主机
					name = i.url  # 图片名
					nid = t  # id
					created_at = str(i.create_at)  # 生成时间
					size = str(i.size)  # 视频大小
					stat = i.stat
					start_time = str(i.start_at)
					end_time = str(i.end_at)
					create_name = str(i.create_name)
					new_data_info={'id': nid, "No": No, "host": host,"create_name":create_name,
						 'created_time': created_at,"url": name,'start_time':start_time,"end_time":end_time}
					if stat == 'created':
						new_data_info.update({'size':size,'stat':'已生成'})
					elif stat == 'generating':
						new_data_info.update({'stat':'正在生成'})
					else:
						new_data_info.update({'stat': '没有'})
					t += 1
					new_data.append(new_data_info)
			obj.pop('data')
			obj.update({'rows': new_data, 'records': records})
			return HttpResponse(json.dumps(obj), content_type="application/json")
	else:
		error = {'code':404,'data':None,'msg':'action type is worng'}
		return HttpResponse (json.dumps(error))
