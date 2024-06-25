

# display_handle = display(None, display_id=True)
# for img in base64Frames:
#     display_handle.update(Image(data=base64.b64decode(img.encode("utf-8"))))
#     time.sleep(0.025)# from IPython.display import display, Image, Audio

import cv2  # We're using OpenCV to read video, to install !pip install opencv-python
import base64
import time
import numpy as np
from openai import OpenAI
import os
import requests
from dotenv import load_dotenv
load_dotenv(r"D:\PProjects\NN\botaireader\.env")
from langchain_openai import ChatOpenAI
from langchain.schema.messages import HumanMessage, SystemMessage
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.callbacks import get_openai_callback

def mse(imageA, imageB):
    # Среднеквадратичная ошибка между двумя изображениями
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])
    return err

video = cv2.VideoCapture(r"D:\PProjects\vidtogiftovk\downloads\doc617202016.gif")

base64Frames = []
last_frame = None
while video.isOpened():
    success, frame = video.read()
    if not success:
        break

    # if last_frame is not None and mse(last_frame, frame) < 1000:
    #     continue
    resize_factor = 0.4
    frame = cv2.resize(frame, (int(frame.shape[1] * resize_factor), int(frame.shape[0] * resize_factor)))

    _, buffer = cv2.imencode(".jpg", frame)
    base64Frames.append(base64.b64encode(buffer).decode("utf-8"))
    last_frame = frame

video.release()
print(len(base64Frames), "frames read.")
# frame_counter = len(base64Frames)
# import imageio
# images = [cv2.imdecode(np.frombuffer(base64.b64decode(frame), np.uint8), cv2.IMREAD_COLOR) for frame in base64Frames]
# imageio.mimsave('output.gif', images)
# exit()
def generate_image_dicts(image_strings):
    return [
        {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{img_str}", 
                "detail": "auto",
            },
        } for img_str in image_strings
    ]

image_dicts=generate_image_dicts(base64Frames)
prompt = ChatPromptTemplate.from_messages([
    SystemMessage(
        content="Ты специалист в русской поэзии. Ты помогаешь писать стихи в стиле разных поэтов."
    ),
    HumanMessage(
        content=[
            {"type": "text", "text": "Напиши стихотворение в стиле {poet} на основе приложенного набора фреймов из видео"},
            *image_dicts
        ]
    )
    ]
)
chat = ChatOpenAI(model="gpt-4o", max_tokens=4000, temperature=0.95, api_key=os.getenv("OPENAI_API_KEY"))
chain = prompt | chat | StrOutputParser()
with get_openai_callback() as cb:
    res=chain.invoke({"poet": "Цветаева"})
    print(cb)
print(res)
    


