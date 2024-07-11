#%%
import json
import vk_api

from content_poster import VkPoster as vkpost
# from content_poster import Tposter as tpost
#%%
import textwrap
width = 40
def print_with_width(text, width):
    wrapped_text = textwrap.wrap(text, width)
    for line in wrapped_text:
        print(line)
# vp=vidp()
# vc=vconv()
vkp = vkpost()
# vkpr=vkprov(vp.scheduler,vkp.vk)
# tpst=tpost(vp.scheduler,vp.dp)
vk_session=vkp.vk_session
vk=vkp.vk
vkupload:vk_api.VkUpload=vkp.upload
# t=vk_session.method('newsfeed.get', {'count': 10, 'source_ids': 'groups'})



group_id = 129592796
filepath=r"C:\Users\Sergey\Downloads\photo_2024-07-06_18-47-45.jpg"
# responce=vkupload.story(filepath, file_type="photo", group_id=group_id)

response=vk_session.method('stories.getPhotoUploadServer',{'v':5.131,'group_id':group_id,'add_to_news':1})

with open('temp.json', 'a', encoding="utf-8") as f:
    json.dump(response, f)

# with open('temp.txt', 'r', encoding="utf-8") as f:
#     response = json.load(f)

import requests

url = response['upload_url']

with open(filepath, 'rb') as file:
    files = {'file': file}
    response = requests.post(url, files=files)

response_data = response.json()
with open('temp.json', 'a', encoding="utf-8") as f:
    json.dump(response_data, f)


response=vk_session.method('stories.save',{'upload_results':response_data['response']['upload_result'],'v':5.131})
