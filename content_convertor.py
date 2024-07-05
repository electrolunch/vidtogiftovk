import time
import uuid
import requests
import os
class ContentConvertor():
    pass

class VideoConvertor(ContentConvertor):
    def __init__(self):
        self.api_key = "9db6e6096e83c3b00996d8843d8ab869"
        # self.api_key = "d7b887b133f8efa16fe1b6f55f1767cd"
        self.download_dir = r"downloads"
        self.url = "https://api.api2convert.com/v2/jobs"
        self.gif_name="video1.gif"

    async def ConvertToGif(self,vid_path,log_func):
        await log_func("upload mp4 to convertor")
        up_url=self.GetUploadUrl()
        gif_name = str(uuid.uuid4())
        gif_path=rf"{self.download_dir}\video"+gif_name+".gif"
        vid_path= vid_path
        resp=self.CreateJob(up_url,vid_path,gif_name)
        await log_func("conversation process...")
        self.WaitForAJob(resp.json()["id"]['job'])
        await log_func("start downloading gif")
        self.DownLoadGif(resp.json()["id"]['job'])
        await log_func("gif downloaded")
        return gif_path
        
    def WaitForAJob(self,job_id):
        while not self.should_stop(job_id):
            time.sleep(5)
    
    def should_stop(self,job_id):
        url = f"https://api.api2convert.com/v2/jobs/{job_id}"
        headers = {
            "x-oc-api-key": self.api_key,
            "Cache-Control": "no-cache"
        }
        response = requests.get(url, headers=headers)
        print(response.status_code)
        json_response=response.json()
        # print(json_response)
        return json_response['status']['code']=='completed'

    def GetUploadUrl(self):
        data={
            "conversion": [{
                "category": "image",
                "target": "gif"
            }]
            }

        headers = {
            "X-Oc-Api-Key": self.api_key,
            "Content-Type": "application/json",
            "Cache-Control": "no-cache"
        }
        response = requests.post(self.url, headers=headers, json=data)
        print(response.status_code)
        json_response=response.json()
        # print(json_response)
        result=json_response['server']+'/upload-file/'+json_response['id']
        # print(result)
        return result

    def CreateJob(self,url,vid_path,gif_name):
        file_uuid = str(uuid.uuid4())
        headers = {
        'x-oc-api-key': self.api_key,
        'x-oc-upload-uuid': file_uuid,
        }
        
        files=[
        ('file',(gif_name+'.mp4',open(vid_path,'rb'),{'Content-Type': 'video/mp4'}))
        ]
        response = requests.request("POST", url, headers=headers, files=files)
        print(response.status_code)
        # print(response.text)
        return response
    
    def DownLoadGif(self,job_id):
        url = f"https://api.api2convert.com/v2/jobs/{job_id}"
        headers = {
            "x-oc-api-key": self.api_key,
            "Cache-Control": "no-cache"
        }
        response = requests.get(url, headers=headers)
        print(response.status_code)
        json_response=response.json()
        # print(json_response)
        output_uri = json_response['output'][0]['uri']
        response = requests.get(output_uri)
        with open(os.path.join(self.download_dir, json_response["output"][0]["filename"]), "wb") as f:
            f.write(response.content)
            
