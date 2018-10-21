from django.db import models
from rest_framework import permissions
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.db.models import Q ,F
import json
from rest_framework.authtoken.models import Token
# Create your models here.

class Staff(models.Model):
	#记录员工信息内容
	No = models.CharField(max_length=128, verbose_name='员工号', unique=True)
	name = models.CharField(max_length=128, verbose_name='姓名', null=True, blank=True)
	dept = models.CharField(max_length=128, verbose_name='部门', null=True, blank=True)
	create_at = models.DateTimeField(verbose_name='创建时间')
	desc = models.CharField(max_length=128, blank=True, null=True, verbose_name='备注信息')

	class Meta:
		db_table = 'ugw_staff'
		verbose_name = '员工信息'
		verbose_name_plural = '员工信息'


class Host(models.Model):
	#记录计算机信息内容
	name = models.CharField(max_length=128, verbose_name='机器名', unique=True)
	ip = models.GenericIPAddressField(verbose_name='ip地址')
	host_type = models.CharField(max_length=256, blank=True, null=True, verbose_name='主机类型')
	mac_addr = models.CharField(max_length=128, blank=True, null=True, verbose_name='物理地址')

	info = models.CharField(max_length=128,blank=True,null=True,verbose_name='主机参数')
	class Meta:
		db_table = 'ugw_host'
		verbose_name = '主机信息'
		verbose_name_plural = '主机信息'

class Dept(models.Model):
	#设置部门
	dname = models.CharField(max_length=256,verbose_name='部门名称')
	class Meta:
		db_table = 'ugw_dept'
		verbose_name = '部门表'
		verbose_name_plural = '部门表'


class Menu(models.Model):
	#设置结合路由设置动态菜单
	cname = models.CharField(max_length=128,verbose_name='路由别名')
	url = models.URLField(max_length=128,verbose_name='页面路由',null=True)
	top = models.CharField(max_length=128,verbose_name='顶级菜单',null=True)
	child = models.CharField(max_length=32,verbose_name='子菜单',null=True)
	is_top = models.SmallIntegerField(verbose_name='父及菜单',null=True)
	name = models.CharField(max_length=32,verbose_name='中文名字')
	class Meta:
		db_table = 'ugw_menu'
		verbose_name = '路由菜单表'
		verbose_name_plural = '路由菜单表'



class Role(models.Model):
	#权限表
	#group_id = models.ForeignKey(Group,related_name='group',on_delete=None)
	menu_id = models.ForeignKey(Menu,related_name='menu',on_delete=None)
	role_type = models.CharField(max_length=32,verbose_name='角色类型')
	class Meta:
		db_table = 'ugw_role'
		verbose_name = '权限表'
		verbose_name_plural = '权限表'



class Permission(models.Model):
	#系统访问授权表
	user_id = models.ForeignKey(User,related_name='user',blank=True,null=True,on_delete=None,verbose_name='用户权限id')
	group_id = models.ForeignKey(Group,related_name='group',blank=True,null=True,on_delete=None,verbose_name='组权限id')
	role = models.ForeignKey(Role,related_name='role',blank=True,null=True,on_delete=None,verbose_name='权限信息')

	class Meta:
		db_table = 'ugw_permission'
		verbose_name = '访问权限表'
		verbose_name_plural = '访问权限表'


class IMages(models.Model):
	#生成图片信息
	name = models.CharField(max_length=128,verbose_name='图片名')
	path = models.FilePathField(max_length=128, verbose_name='图片物理存放位置')
	size = models.IntegerField(verbose_name='图片文件大小')
	length = models.IntegerField(verbose_name='图片分辨率之长')
	width = models.IntegerField(verbose_name='图片分辨率之宽')
	create_at = models.DateTimeField(verbose_name='图片创建时间')
	desc = models.CharField(max_length=128, blank=True, null=True, verbose_name='备注信息')
	user = models.ForeignKey(Staff, related_name='User', on_delete=models.CASCADE)
	host = models.ForeignKey(Host, related_name='Host', on_delete=models.CASCADE)
	asb_path = models.CharField(max_length=256,verbose_name='绝对路径')
	def __str__(self):
		return "{'id':%s,'path':%s,'size':%s,'length':%s,'width':%s,'create_at':%s,'desc':%s}" % (
		self.id, self.path,self.size, self.length, self.width, self.create_at, self.desc)

	class Meta:
		db_table = 'ugw_images'
		verbose_name = '图片信息'
		verbose_name_plural = '图片信息'


class Video(models.Model):
	#记录生成视频相关信息
	video_path = models.CharField(max_length=256, verbose_name='视频存放位置', unique=True)
	stat_type = (('generating', '生成中'), ('created', '生成完毕'), ('null', '没有报告'),)
	stat = models.CharField(choices=stat_type, verbose_name='视频状态', max_length=256)
	url = models.URLField(verbose_name='访问URL地址', blank=True)
	start_at = models.DateTimeField(verbose_name='视频开始时间',)
	end_at = models.DateTimeField(verbose_name='视频结束时间',)
	create_at = models.DateTimeField(verbose_name='创建时间', null=True, blank=True,auto_now_add=True,auto_created=True)
	user = models.ForeignKey(Staff, related_name='video', on_delete=models.CASCADE)
	host = models.ForeignKey(Host, related_name='video', on_delete=models.CASCADE)
	size = models.IntegerField(verbose_name='视频大小',null=True,blank=True)
	create_name = models.CharField(verbose_name='创建者',max_length=128,null=True,blank=True)
	class Meta:
		db_table = 'ugw_video'
		verbose_name = '视频信息'
		verbose_name_plural = '视频信息'


class Mirror(models.Model):
	pid = models.SmallIntegerField(verbose_name='pid号')
	started = models.DateTimeField(verbose_name='创建时间',auto_created=True,auto_now_add=True,null=True)
	host = models.CharField(max_length=128,verbose_name='主机名')
	ip = models.GenericIPAddressField(verbose_name='IP地址')
	path = models.FilePathField(verbose_name='文件路径')
	name = models.CharField(max_length=128,verbose_name='文件名')
	class Meta:
		db_table = 'ugw_pid'
		verbose_name = '客户端pid信息'
		verbose_name_plural = '客户端pid信息'


class Logging(models.Model):
	#记录操作日志相关信息
	type = models.CharField(max_length=20, verbose_name='操作类型')
	info = models.CharField(max_length=256, verbose_name='操作内容')
	create_at = models.DateTimeField(verbose_name='操作时间')
	user = models.ForeignKey(Staff, related_name='logging', on_delete=None)
	host = models.ForeignKey(Host, related_name='logging', on_delete=None)

	class Meta:
		db_table = 'ugw_log'
		verbose_name = '日志信息'
		verbose_name_plural = '日志信息'

# def images_list1(request):
# 	print( request.POST.get('_search') )
# 	if request.POST.get('_search') == 'true':
# 		rule = json.loads(request.POST.get('filters')).get('groupOp')
# 		#print(rule)
# 		parms = json.loads(request.POST.get('filters')).get('rules')
# 		#print(parms)
# 		res = Q()
# 		r_query = IMages.objects.get('%s')%t
# 		if rule	 == 'AND':
# 			for i in parms:
# 				print(i)
# 				if i.get('op') == 'eq':
# 					rule_info = '%s=%s'%(i.get('field'),i.get('data'))

#token = Token.objects.create(user_id=4)

