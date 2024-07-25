
from content_poster import VkPoster as vkpost
# from content_poster import Tposter as tpost
from datetime import datetime
# vp=vidp()
# vc=vconv()
vkp = vkpost()
# vkpr=vkprov(vp.scheduler,vkp.vk)
# tpst=tpost(vp.scheduler,vp.dp)
vk_session=vkp.vk_session
vk=vkp.vk

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

friends_getSuggestions=vk_session.method('friends.getSuggestions', {'count': 100, 'fields': 'bdate'})

friends_getSuggestions_has_bdate = [friend for friend in friends_getSuggestions['items'] if friend.get('bdate')]

friends_getSuggestions_has_year = [friend for friend in friends_getSuggestions_has_bdate if calculate_age(friend['bdate']) != "error"]

friends_getSuggestions_over_40 = [friend for friend in friends_getSuggestions_has_year if calculate_age(friend['bdate']) > 40]


friends_getMutual=vk_session.method('friends.getMutual', {'source_uid': 617202016, "target_uid": 89968313,"order":"random","need_common_count":1})
print(len(t1))

friends_getMutual_count=friends_getMutual['count']