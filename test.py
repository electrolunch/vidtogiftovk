#%%
# import asyncio
# import os
# import time
# from content_provider2 import VideoProvider as vidp
# from content_provider2 import Vk_provider as vkprov
# from content_convertor import VideoConvertor as vconv
from content_poster import VkPoster as vkpost
# from content_poster import Tposter as tpost
#%%
# vp=vidp()
# vc=vconv()
vkp = vkpost()
# vkpr=vkprov(vp.scheduler,vkp.vk)
# tpst=tpost(vp.scheduler,vp.dp)
vk_session=vkp.vk_session
vk=vkp.vk

