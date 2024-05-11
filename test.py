import time
from content_poster import VkPoster as vkpost
   
vkp = vkpost()  

def log_func(text):
    print(text)
    # vp.func_log(text)
    pass

gpath="fa51832d-49df-4c96-9d45-e0837eb3b35f.gif"

while True:
    try:
        uuid=vkp.LoadAndPostToPioner(gpath,log_func)
        print(uuid)
        time.sleep(10) 
    # except ConnectionResetError:
    #     print("dfdfdfdfdfdfdfdfdfdfdfdfdfdfdfdfdfdf")
    # except ConnectionError:
    #     print("ConnectionError")
    except Exception as e:
        print("********************************")
        print(e)
        if str(e)=="('Connection aborted.', ConnectionResetError(10054, 'An existing connection was forcibly closed by the remote host', None, 10054, None))":
            time.sleep(10) 
            print("ConnectionError")
    break