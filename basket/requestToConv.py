#%%
import json
from PythonApplication1.onlineConvertRestApiModels import Conversion, Input, Status
import requests
from onlineConvertRestApiModels import Job
#%%
api_key = "9db6e6096e83c3b00996d8843d8ab869"

url = "https://api.api2convert.com/v2/jobs"
headers = {
    "X-Oc-Api-Key": api_key,
    "Content-Type": "application/json"
}

data = {
    "input": [{
        "type": "remote",
        "source": "https://rottenswamp.ru/images/yandex-l1ogo-1600x900_124ca.jpg"
    }],
    "conversion": [{
        "target": "png"
    }]
}
#%%
response = requests.post(url, headers=headers, json=data)
print(response.status_code)
json_response=response.json()
# print(response.json())
#%%
job_id=json_response["id"]

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
# %%
