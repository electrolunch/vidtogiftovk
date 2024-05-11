#%%
import vk_api
import requests
import uuid
#%%
gif_path="video1.gif"
login="+79006398664"
password="ojnebgfhjljrc1"

def auth_handler():
    """ При двухфакторной аутентификации вызывается эта функция."""
    # Код двухфакторной аутентификации
    key = input("Enter authentication code: ")
    # Если: True - сохранить, False - не сохранять.
    remember_device = True
    return key, remember_device

# Authenticate and create an API session
vk_session = vk_api.VkApi(login, password,
 auth_handler=auth_handler,
 token="vk1.a.iAT3_sClCSwAkAMSGMc78Oi5ELK_Fi3ErGgsWS-J9sBDsUCzpLNvCX0fYs_hqHx5inT9zmBZCeOu76_DMOrNUv-S8P08Uog7e7ShbcVDUV-Sev81L4pz-FhD1zjgtqwYZ1PHX2eytXlvCzyD_NKzBU-5Uv_xT0gNjisyAZnxqEuRQhg5jpSHr1RA6D9Gd4PyzjxUm94oizkuGYK7PTQ_bg"
 )
vk_session.auth()
vk = vk_session.get_api()

# Define the group ID and message
group_id = -129592796
message = 'Check out this GIF!'

# Get the document upload server
# upload_url = vk.docs.getUploadServer()['upload_url']
# print(upload_url)
# # Upload the document
# response = requests.post(upload_url, files={'file': ('gif_path', open(gif_path, 'rb'))})
# response_json=response.json()
# print(response_json)
#%%
upload = vk_api.VkUpload(vk_session)
gif_uuid = str(uuid.uuid4())
doc = upload.document(gif_path,gif_uuid)
#%%
vk.wall.post(owner_id=group_id,message="...", 
attachments=[f"doc{doc['doc']['owner_id']}_{doc['doc']['id']}",f"doc{doc['doc']['owner_id']}_{doc['doc']['id']}"])

#%%


#%%
# # Get the server address for document upload
# upload_url = vk.docs.getWallUploadServer(group_id=group_id)['upload_url']

# # Upload the gif to the server
# response = requests.post(upload_url, files={'file': open(gif_path, 'rb')}).json()

# # Save the gif as a document
# doc = vk.docs.save(file=response['file'], title='GIF')[0]

# Define the attachment as the document
# attachment = f'doc{doc["owner_id"]}_{doc["id"]}'

# # Post the message with the attachment to the group's wall
# vk.wall.post(owner_id=group_id, message=message, attachments=attachment)
# %%
