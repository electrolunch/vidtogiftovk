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

t=vk_session.method('newsfeed.get', {'count': 10, 'source_ids': 'groups'})
import json
#save
with open('vkpostdata.json', 'w', encoding="utf-8") as outfile:
    json.dump(t, outfile)

items=t['items']

print(len(items))



min_likes=0
min_reposts=0
min_views=0

filtered_items = []
for item in items:
    if item['type'] == 'post':
        filtered_items.append(item)
print(len(filtered_items))

items = filtered_items
filtered_items = []
for item in items:
    if (item['likes']['count'] >= min_likes and 
        item['reposts']['count'] >= min_reposts and 
        item['views']['count'] >= min_views):
        filtered_items.append(item)
print(len(filtered_items))

filtered_items_has_photo = []
filtered_items_has_one_photo = []
for item in filtered_items:
    # Проверяем наличие вложений типа "photo"
    has_photo = False
    photo_count = 0
    for attachment in item.get('attachments', []):
        if attachment['type'] == 'photo':
            has_photo = True
            photo_count += 1

    if has_photo:
        filtered_items_has_photo.append(item)

    if photo_count == 1:
        filtered_items_has_one_photo.append(item)

print(len(filtered_items_has_photo))
print(len(filtered_items_has_one_photo))
# response = vk.wall.get(owner_id=-146916884, count=10)
import json



work_items=filtered_items_has_one_photo
result = []
for item in work_items:
    text = item.get('text', '')  # Получаем текст поста (или пустую строку, если нет текста)
    post_url=f"https://vk.com/wall{item['owner_id']}_{item['post_id']}"
    # Находим фото максимального размера
    max_photo_url = None
    max_photo_height = 0

    for attachment in item.get('attachments', []):
        if attachment['type'] == 'photo':
            for size in attachment['photo']['sizes']:
                if size['height'] > max_photo_height:
                    max_photo_height = size['height']
                    max_photo_url = size['url']

    result.append((post_url,text, max_photo_url))  # Добавляем кортеж (text, photo_url) в результат

print(result)