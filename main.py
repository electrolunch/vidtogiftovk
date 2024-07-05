#%%
import asyncio
import os
import time
from content_provider2 import VideoProvider as vidp
from content_provider2 import Vk_provider as vkprov
from content_convertor import VideoConvertor as vconv
from content_poster import VkPoster as vkpost
from content_poster import Tposter as tpost
import tools as tools
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

async def upload_doc(doc_path, vkp, LogFunc):
    for i in range(0,5):
        try:
            await vkp.LoadAndPostToPioner(doc_path,LogFunc)
            os.remove(doc_path)
            break
        except Exception as e:
            if(str(e)=='An existing connection was forcibly closed by the remote host'):
                continue
            await LogFunc(str(e))

async def VideoHandler(v_path):
    try:
        gif_path=await vc.ConvertToGif(v_path,LogFunc)
        print("gif_path ",gif_path)
    except Exception as e:
        await LogFunc(str(e))
        os.remove(v_path)
        return
    
    try:         
        await LogFunc("Removing audio from video")
        sv_path=tools.add_string_to_filename(v_path,'_sv')
        print("sv_path ",sv_path)
        tools.remove_audio_ffmpeg(v_path,sv_path)
        await LogFunc("Audio removed")
        os.remove(v_path)
    except Exception as e:
        await LogFunc(str(e))
        sv_path=v_path
   
    # await LogFunc(gif_path)
    time.sleep(10)
    await LogFunc("upload gif to vk")
    await upload_doc(gif_path, vkp, LogFunc)
    await LogFunc("upload video to vk")
    await upload_doc(sv_path, vkp, LogFunc)

async def vk_post_handler(vkpostdata):
    print("пост из вк в телеграм")
    filepath=await tpst.post_to_tg(vkpostdata,LogFunc)


vkpr.SetVkPostHandler(vk_post_handler,LogFunc)
vp.SetVideoHandler(VideoHandler)

vp.Start()
