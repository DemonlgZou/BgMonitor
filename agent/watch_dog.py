import os,psutil,json,threading,subprocess

file_abs_path = os.path.abspath(__file__)
file_name = os.path.basename(file_abs_path)
info = psutil.Process(os.getpid())


def cmd(cmd):
	#执行启动listen agent的方法
	subprocess.run('start %s '%cmd,shell=True)

#打开客户机上的记录文件读取agent程序上次打开时的记录的相关信息，主要是pid号和程序的绝对路径
if os.path.isfile(r'C:\ProgramData\pid.txt'):
	os.system('attrib -H %s' % r'C:\ProgramData\pid.txt')
	with open(r'C:\ProgramData\pid.txt','r',encoding='utf-8') as f:
		for i in f:
			i=json.loads(i)
			pid_no = i.get('pid')
			pid_abs_path = i.get('file_abs_path')
			pid_name = os.path.splitext(os.path.basename(pid_abs_path))
			command = pid_abs_path.replace('.py', '.exe') #再次打开agent文件的命令
			try:
				#通过文件中pid号获取系统中是否存在pid
				obj = psutil.Process(pid_no)
				#若存在pid号但调用的程序不同的话则重新再次打开agent文件
				if os.path.splitext(obj.name())[0] != pid_name[0]:
					t= threading.Thread(target=cmd, args=(command,))
					t.start()
			except psutil.NoSuchProcess  as e:
				#若直接没有该进程号的话则直接打开agent文件
				t = threading.Thread(target=cmd,args=(command,))
				t.start()
	f.close()
			#暂未完善  如果没有相关的系统中没有相关记录文件，则直接访问接口调用后台数据再次启动agent文件
else:
		#如果文件不存在，请求服务器获取信息再次打开程序（暂未完善）
		pass
os.system('attrib +H %s' % r'C:\ProgramData\pid.txt')