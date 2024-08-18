
from content_poster import VkPoster as vkpost
import random
from datetime import datetime
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
friends_getSuggestions=vk_session.method('friends.getSuggestions', {'count': 100, 'fields': "bdate, city, sex, country, nickname,followers_count, contacts"})

friends_getSuggestions_has_bdate = [friend for friend in friends_getSuggestions['items'] if friend.get('bdate')]
friends_getSuggestions_has_year = [friend for friend in friends_getSuggestions_has_bdate if calculate_age(friend['bdate']) != "error"]

friends_getSuggestions_over_40 = [friend for friend in friends_getSuggestions_has_year if calculate_age(friend['bdate']) > 30]

friends_getSuggestions_non_men = [friend for friend in friends_getSuggestions_over_40 if friend.get('sex') != 2]
print(len(friends_getSuggestions_non_men))

friends_getSuggestions["items"]=friends_getSuggestions_non_men

random_friend = random.choice(friends_getSuggestions["items"])

# random_friend = random.choice(friends_getSuggestions["items"])
friends_getMutual=vk_session.method('friends.getMutual', {'source_uid':my_id , "target_uid": random_friend['id'],"order":"random","need_common_count":1})
friends_getMutual_count=friends_getMutual['common_count']
print(friends_getMutual_count)

t=vk_session.method('friends.add', {'user_id': random_friend['id']})

def calculate_age(date_str):
    if not date_str:
        return "Дата не указана"
    
    try:
        # Предполагаем, что формат даты - день.месяц.год
        day, month, year = map(int, date_str.split('.'))
        birth_date = datetime(year, month, day)
        today = datetime.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return age
    except ValueError:
        return "error"