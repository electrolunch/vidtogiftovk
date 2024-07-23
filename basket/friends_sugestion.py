
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

friends_getSuggestions=vk_session.method('friends.getSuggestions', {'count': 10, 'fields': ['bdate','sex','photo_200_orig',"contacts"]})

friends_getMutual=vk_session.method('friends.getMutual', {'source_uid': 617202016, "target_uid": 89968313,"order":"random","need_common_count":1})
print(len(t1))

friends_getMutual_count=friends_getMutual['count']