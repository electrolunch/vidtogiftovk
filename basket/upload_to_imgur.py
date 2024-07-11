
import requests
import base64
import os
import time

async def authenticate(client_id, client_secret):
    auth_url = f'https://api.imgur.com/oauth2/authorize?client_id={client_id}&response_type=token&state=application_state'
    
    # Откройте URL в браузере
    print(f"Пожалуйста, авторизуйтесь по ссылке: {auth_url}")
    
    # Шаг 2: Вставка URL из браузера с токеном
    response_url = input("Вставьте URL, полученный после авторизации: ")
    # response_url=r"https://imgur.com/?state=application_state#access_token=cad3b5d9e6dc88cf6410f8e731e7489dccaf0191&expires_in=315360000&token_type=bearer&refresh_token=2c279fdf8b7f87bb87057c4ca622205e6addc851&account_username=Electrolunch&account_id=166826917"
    # Парсинг URL
    token_start = response_url.find("access_token=") + len("access_token=")
    token_end = response_url.find("&", token_start)
    
    if token_start != -1 and token_end != -1:
        access_token = response_url[token_start:token_end]
        return access_token
        
    else:
        print("Токен не найден в URL. Пожалуйста, убедитесь, что вы вставили правильный URL.")



async def get_access_token(client_id, client_secret):
    with open("imgtok.txt", "r") as f:
        line = f.read().strip()
    
    # Извлечение токена из строки
    if line.startswith("access_token="):
        tok = line.split("=", 1)[1].strip("'\"")
    else:
        tok = await authenticate(client_id, client_secret)
        if tok is None:
            print("Не удалось получить токен. Попробуйте ещё раз.")
            return
        with open("imgtok.txt", "w") as f:
            f.write(f"access_token={tok}")

    return tok
    


import requests
import time

def upload_image(client_id, access_token, image_path, title, description):
    """
    Загрузка изображения на Imgur.

    Args:
        client_id: Client ID вашего приложения Imgur.
        access_token: Access token, полученный после авторизации.
        image_path: Путь к изображению для загрузки.
        title: Заголовок изображения.
        description: Описание изображения.

    Returns:
        Словарь с данными ответа от Imgur API или сообщение об ошибке.
    """
    
    url = "https://api.imgur.com/3/image"
    headers = {"Authorization": f"Bearer {access_token}"}
    max_retries = 3
    retry_delay = 5  # время задержки перед повторной попыткой (в секундах)

    files = {
        'image': (image_path, open(image_path, 'rb'), 'video/mp4'),
    }
    data = {
        "title": title,
        "description": description
    }

    for attempt in range(max_retries):
        try:
            response = requests.post(url, headers=headers, data=data, files=files)
            
            if response.status_code == 503:
                print(f"Attempt {attempt+1}: Service unavailable (503). Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                continue
            elif response.status_code == 413:
                print("Request Entity Too Large (413). The image size is too large to upload.")
                return {"error": "Request Entity Too Large (413). The image size is too large to upload."}
            
            response.raise_for_status()  # вызвать исключение для плохих ответов (4xx, 5xx)
            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt+1}: An error occurred: {e}")
            if attempt == max_retries - 1:
                return {"error": str(e)}
            time.sleep(retry_delay)

    return {"error": "Max retries exceeded"}

import aiohttp
import asyncio
import time

async def __upload_image(client_id, access_token, image_path, title, description):
    """
    Загрузка изображения на Imgur.

    Args:
        client_id: Client ID вашего приложения Imgur.
        access_token: Access token, полученный после авторизации.
        image_path: Путь к изображению для загрузки.
        title: Заголовок изображения.
        description: Описание изображения.

    Returns:
        Словарь с данными ответа от Imgur API или сообщение об ошибке.
    """
    
    url = "https://api.imgur.com/3/image"
    headers = {"Authorization": f"Bearer {access_token}"}
    max_retries = 3
    retry_delay = 5  # время задержки перед повторной попыткой (в секундах)

    async with aiohttp.ClientSession() as session:
        for attempt in range(max_retries):
            try:
                with open(image_path, 'rb') as f:
                    image_data = f.read()
                    
                data = aiohttp.FormData()
                data.add_field('image', image_data, filename=image_path, content_type='video/mp4')
                data.add_field('title', title)
                data.add_field('description', description)

                async with session.post(url, headers=headers, data=data) as response:
                    if response.status == 503:
                        print(f"Attempt {attempt+1}: Service unavailable (503). Retrying in {retry_delay} seconds...")
                        await asyncio.sleep(retry_delay)
                        continue
                    elif response.status == 413:
                        print("Request Entity Too Large (413). The image size is too large to upload.")
                        return {"error": "Request Entity Too Large (413). The image size is too large to upload."}

                    response.raise_for_status()  # вызвать исключение для плохих ответов (4xx, 5xx)
                    return await response.json()

            except aiohttp.ClientResponseError as e:
                print(f"Attempt {attempt+1}: An error occurred: {e}")
                if attempt == max_retries - 1:
                    return {"error": str(e)}
                await asyncio.sleep(retry_delay)

        return {"error": "Max retries exceeded"}

# Пример вызова функции
# asyncio.run(__upload_image('your_client_id', 'your_access_token', 'path/to/image.jpg', 'Title', 'Description'))

# Пример вызова функции
async def async_upload(client_id, access_token, image_path, title, description):
    return asyncio.run(__upload_image(client_id, access_token, image_path, title, description))

async def main():
    client_id = "5c58ec0f53b4cc1"
    client_secret = "953870f77524e3742c55571ac4cd2811fd0162a2"

    # Аутентификация и получение access_token
    access_token=await get_access_token(client_id, client_secret)

    # Путь к изображению для загрузки
    image_path = r"D:\PProjects\vidtogiftovk\downloads\video31e57c7b-6950-4b53-a3ff-7655178215a5_.mp4"

    # Загрузка изображения
    title = ""
    description = ""
    response = await __upload_image(client_id, access_token, image_path, title, description)

    if "error" in response:
        print("Ошибка при загрузке изображения:")
        print(response["error"])

    # Вывод результата
    if response["success"]:
        print("Изображение успешно загружено:")
        print(response["data"]["link"])
    else:
        print("Ошибка при загрузке изображения:")
        print(response)


if __name__ == "__main__":
    # Замените на ваши client_id и client_secret
    asyncio.run(main())  # Запуск асинхронной функции main()

