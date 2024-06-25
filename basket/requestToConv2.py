#%%
# from PythonApplication1.onlineConvertRestApiModels import Job,Input,Conversion
from onlineConvertRestApiModels import Conversion, Input, Job
import requests
#%%
api_key = "9db6e6096e83c3b00996d8843d8ab869"
source ="https://rottenswamp.ru/images/yandex-l1ogo-1600x900_124ca.jpg"
url = "https://api.api2convert.com/v2/jobs"

job=Job.from_dict({
    "input": [{
        "type": "remote",
        "source": "https://rottenswamp.ru/images/yandex-l1ogo-1600x900_124ca.jpg"
    }],
    "conversion": [{
        "target": "png"
    }]
})


data=job.to_json()

headers = {
    "X-Oc-Api-Key": api_key,
    "Content-Type": "application/json"
}

# job.input=Input()
#%%
data=job.to_json()
response = requests.post(url, headers=headers, json=data)
print(response.status_code)
json_response=response.json()