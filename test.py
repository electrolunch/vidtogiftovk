
from content_poster import VkPoster as vkpost
import random
# from content_poster import Tposter as tpost
#%%
# vp=vidp()
# vc=vconv()
vkp = vkpost()
# vkpr=vkprov(vp.scheduler,vkp.vk)
# tpst=tpost(vp.scheduler,vp.dp)
vk_session=vkp.vk_session
vk=vkp.vk
my_id=617202016
friends_getSuggestions=vk_session.method('friends.getSuggestions', {'count': 40, 'fields': "bdate, city, sex, country, nickname,followers_count, contacts"})

random_friend = random.choice(friends_getSuggestions["items"])
friends_getMutual=vk_session.method('friends.getMutual', {'source_uid':my_id , "target_uid": random_friend['id'],"order":"random","need_common_count":1})
friends_getMutual_count=friends_getMutual['common_count']
print(friends_getMutual_count)

t=vk_session.method('friends.add', {'user_id': random_friend['id']})