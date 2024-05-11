#%%
import asyncio
import os
import time
from content_provider2 import VideoProvider as vidp
from content_convertor import VideoConvertor as vconv
from content_poster import VkPoster as vkpost

#%%
vp=vidp()
vc=vconv()
vkp = vkpost()

async def LogFunc(text):
    await vp.func_log(text)
    print(text)
    pass

async def VideoHandler(v_path):
    try:
        gif_path=await vc.ConvertToGif(v_path,LogFunc)
        os.remove(v_path)
    except Exception as e:
        await LogFunc(str(e))
        os.remove(v_path)
        return
    # await LogFunc(gif_path)
    time.sleep(10)
    for i in range(0,5):
        try:
            await vkp.LoadAndPostToPioner(gif_path,LogFunc)
            os.remove(gif_path)
            break
        except Exception as e:
            if(str(e)=='An existing connection was forcibly closed by the remote host'):
                continue
            await LogFunc(str(e))
            # os.remove(gif_path)




vp.SetVideoHandler(VideoHandler)

vp.Start()