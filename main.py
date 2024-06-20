#%%
import asyncio
import os
import time
from content_provider2 import VideoProvider as vidp
from content_provider2 import Vk_provider as vkprov
from content_convertor import VideoConvertor as vconv
from content_poster import VkPoster as vkpost
from content_poster import Tposter as tpost
#%%
vp=vidp()
vc=vconv()
vkp = vkpost()
vkpr=vkprov(vp.scheduler,vkp.vk)
tpst=tpost(vp.scheduler,vp.dp)

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

async def vk_post_handler(vkpostdata):
    print("пост из вк в телеграм")
    filepath=await tpst.post_to_tg(vkpostdata,LogFunc)
    # os.remove(filepath)


vkpr.SetVkPostHandler(vk_post_handler,LogFunc)
vp.SetVideoHandler(VideoHandler)

vp.Start()
