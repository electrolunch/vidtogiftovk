#%%
import asyncio
import os
import time
from content_provider2 import VideoProvider as vidp
from content_provider2 import Vk_provider as vkprov
from content_convertor import VideoConvertor as vconv
from content_poster import VkPoster as vkpost
from content_poster import Tposter as tpost
from content_poster import ImgurPoster as imgpost
import tools as tools
#%%
vp=vidp()
vc=vconv()
vkp = vkpost()
vkpr=vkprov(vp.scheduler,vkp.vk)
tpst=tpost(vp.scheduler,vp.dp)
tpst_imgur=tpost(vp.scheduler,vp.dp)
tpst_imgur.channel_id='@imgurlinks'
imgpst=imgpost(vp.scheduler)
async def LogFunc(text):
    await vp.func_log(text)
    print(text)
    pass

async def upload_doc(doc_path, vkp, LogFunc):
    for i in range(0,5):
        try:
            await vkp.LoadAndPostToPioner(doc_path,LogFunc)
            break
        except Exception as e:
            if(str(e)=='An existing connection was forcibly closed by the remote host'):
                continue
            await LogFunc(str(e))

async def VideoHandler(v_path,v_uuid,message_text):
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
    title=vidp.title if vidp.title else "-"
    result=await imgpst.post_video(sv_path, LogFunc,title=title)
    vidp.title=""
    if result is not None:
        await LogFunc("post imgur link to tg. title="+title)
        await tpst_imgur.write_message(str(imgpst.v_link),LogFunc)


    os.remove(sv_path)

async def vk_post_handler(vkpostdata):
    print("пост из вк в телеграм")
    filepath=await tpst.post_to_tg(vkpostdata,LogFunc)

    pass


vkpr.SetVkPostHandler(vk_post_handler,LogFunc)
vp.SetVideoHandler(VideoHandler)

vp.Start()
