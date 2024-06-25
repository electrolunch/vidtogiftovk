#%%

import os
import uuid
import requests

im_path=r'video4fac7ff7-00a2-4e68-9547-1900929b5a18.mp4'
#%%
api_key = "9db6e6096e83c3b00996d8843d8ab869"

url = "https://api.api2convert.com/v2/jobs"
data={
    "conversion": [{
        "category": "image",
        "target": "gif"
    }]
}

headers = {
    "X-Oc-Api-Key": api_key,
    "Content-Type": "application/json",
    "Cache-Control": "no-cache"
}
#%%
response = requests.post(url, headers=headers, json=data)
print(response.status_code)
json_response=response.json()
print(json_response)
result=json_response['server']+'/upload-file/'+json_response['id']
print(result)


#%%
url = result

file_uuid = str(uuid.uuid4())
# headers = {
#     'x-oc-api-key': api_key,
#     'x-oc-upload-uuid': file_uuid,
#     'Cache-Control': 'no-cache',
#     'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW',
# }
headers = {
  'x-oc-api-key': api_key,
  'x-oc-upload-uuid': file_uuid,
}
data = {
    # 'decrypt_password': '123',
    # 'Content-Disposition': 'form-data; name="decrypt_password"',
    # 'fileName': im_path,
    # 'fileSize': os.path.getsize(im_path),
    # 'description': 'undefined'
}

files=[
  ('file',('video1.mp4',open(im_path,'rb'),{'Content-Type': 'video/mp4'}))
]

response = requests.request("POST", url, headers=headers, data=data, files=files)

# files = [
#     'file':  ('image.jpg',open(im_path, 'rb'),{'Content-Disposition': 'form-data; name="file"; filename="image.jpg"'},
#  {'Content-Type': 'image/jpg'})
# ]

# response = requests.post(url, headers=headers, data=data, files=files)

# response = requests.post(url, headers=headers,  files=files)
print(response.status_code)
print(response.text)
json_response=response.json()
# t=open(im_path, 'rb')
# {'Content-Disposition': 'form-data; name="file"; filename="file.jpg"'},
# {'Content-Type': 'image/jpg'})
#%%
# response = requests.post(url, headers=headers, json=data)
# print(response.status_code)
# json_response=response.json()
# print(response.json())
#%%
job_id=json_response["id"]['job']

url = f"https://api.api2convert.com/v2/jobs/{job_id}"
headers = {
    "x-oc-api-key": api_key,
    "Cache-Control": "no-cache"
}

response = requests.get(url, headers=headers)
print(response.status_code)
json_response=response.json()
print(json_response)
#%%
output_uri = json_response['output'][0]['uri']
response = requests.get(output_uri)

with open(json_response["output"][0]["filename"], "wb") as f:
    f.write(response.content)
# status = Status(json_response["status"])
# conversions = [Conversion(conv) for conv in json_response["conversion"]]
# inputs = [Input(**inp) for inp in json_response["input"]]

# json_response["status"] = status
# json_response["conversion"] = conversions
# json_response["input"] = inputs

# job = Job(**json_response)

#%%
# output_uri = json_response['output'][0]['uri']
# response = requests.get(output_uri)

# with open(json_response["output"][0]["filename"], "wb") as f:
#     f.write(response.content)
# status = Status(json_response["status"])
# conversions = [Conversion(conv) for conv in json_response["conversion"]]
# inputs = [Input(**inp) for inp in json_response["input"]]
# Content-Disposition: form-data; name="decrypt_password"
# json_response["status"] = status
# json_response["conversion"] = conversions
# json_response["input"] = inputs

# job = Job(**json_response)
# %%
# job_id=json_response["id"]

# url = f"https://api.api2convert.com/v2/jobs/{job_id}"
# headers = {
#     "x-oc-api-key": api_key,
#     "Cache-Control": "no-cache"
# }

# response = requests.get(url, headers=headers)
# print(response.status_code)
# json_response=response.json()
# print(json_response)