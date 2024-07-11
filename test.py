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


t=vk_session.method('wall.get', {'count': 10,'owner_id':-146916884})
import json
#save
with open('vkpostdata.json', 'w', encoding="utf-8") as outfile:
    json.dump(t, outfile)

import requests

# URL of the video
url = 'https://vk.com/doc617202016_676921311?hash=RjmX9RE8eKzCgG9OfMZ3BEZcT02XtQpQV9FZea1YR6D&dl=GYYTOMRQGIYDCNQ:1720634395:zYet96IOJYhwq5sRZtgaL0zHhPkU1tqCQqGVyTh1sbz&api=1&mp4=1'

# Send a GET request to the URL
response = requests.get(url, stream=True)

# Path to save the video
video_path = 'video.mp4'

# with open(video_path, 'wb') as file:
#     file.write(response.content)
# Write the content to a file
with open(video_path, 'wb') as file:
    for chunk in response.iter_content(chunk_size=8192):
        if chunk:  # filter out keep-alive new chunks
            file.write(chunk)

print(f"Video downloaded successfully and saved as {video_path}")

