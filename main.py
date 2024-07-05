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
        # print("v_path ",v_path)
        gif_path=await vc.ConvertToGif(v_path,LogFunc)
        await LogFunc("Removing audio from video")
        sv_path=tools.add_string_to_filename(v_path,'_sv')
        print("sv_path ",sv_path)
        tools.remove_audio_from_video(v_path,sv_path)
        await LogFunc("Audio removed")
        os.remove(v_path)
    except Exception as e:
        await LogFunc(str(e))
        os.remove(v_path)
        return
    # await LogFunc(gif_path)
    time.sleep(10)
    await LogFunc("upload gif to vk")
    gif_name = os.path.basename(gif_path)
    await upload_doc(gif_name, vkp, LogFunc)
    await LogFunc("upload video to vk")
    sv_name=os.path.basename(sv_path)
    await upload_doc(sv_name, vkp, LogFunc)

async def vk_post_handler(vkpostdata):
    print("пост из вк в телеграм")
    filepath=await tpst.post_to_tg(vkpostdata,LogFunc)


vkpr.SetVkPostHandler(vk_post_handler,LogFunc)
vp.SetVideoHandler(VideoHandler)

vp.Start()
