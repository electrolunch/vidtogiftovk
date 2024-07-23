
import requests
import base64
import os
import time
import aiohttp
import asyncio

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


async def __get_account_images(username, access_token, page=0):
    """
    Получение изображений из аккаунта Imgur.

    Args:
        username: Имя пользователя Imgur.
        access_token: Access token, полученный после авторизации.
        page: Номер страницы для пагинации (по умолчанию 0).

    Returns:
        Список словарей с данными о изображениях или сообщение об ошибке.
    """

    url = f"https://api.imgur.com/3/account/{username}/images/{page}"
    headers = {"Authorization": f"Bearer {access_token}"}
    max_retries = 3
    retry_delay = 5

    async with aiohttp.ClientSession() as session:
        for attempt in range(max_retries):
            try:
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get('data', [])  # Возвращаем список изображений или пустой список
                    elif response.status == 503:
                        print(f"Attempt {attempt + 1}: Service unavailable (503). Retrying in {retry_delay} seconds...")
                        await asyncio.sleep(retry_delay)
                        continue
                    else:
                        response.raise_for_status()

            except aiohttp.ClientResponseError as e:
                print(f"Attempt {attempt + 1}: An error occurred: {e}")
                if attempt == max_retries - 1:
                    return {"error": str(e)}
                await asyncio.sleep(retry_delay)

        return {"error": "Max retries exceeded"}


async def __get_account_images2(access_token):
    """
    Получение изображений из аккаунта Imgur (для текущего пользователя).

    Args:
        access_token: Access token, полученный после авторизации.

    Returns:
        Список словарей с данными о изображениях или сообщение об ошибке.
    """

    url = "https://api.imgur.com/3/account/me/images"
    headers = {"Authorization": f"Bearer {access_token}"}
    max_retries = 3
    retry_delay = 5

    async with aiohttp.ClientSession() as session:
        for attempt in range(max_retries):
            try:
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get('data', [])  # Возвращаем список изображений или пустой список
                    elif response.status == 503:
                        print(f"Attempt {attempt + 1}: Service unavailable (503). Retrying in {retry_delay} seconds...")
                        await asyncio.sleep(retry_delay)
                        continue
                    else:
                        response.raise_for_status()

            except aiohttp.ClientResponseError as e:
                print(f"Attempt {attempt + 1}: An error occurred: {e}")
                if attempt == max_retries - 1:
                    return {"error": str(e)}
                await asyncio.sleep(retry_delay)

        return {"error": "Max retries exceeded"}

async def __get_account_images3(username,client_id, access_token, page=0):
    """
    Получение изображений из аккаунта Imgur.

    Args:
        username: Имя пользователя Imgur.
        access_token: Access token, полученный после авторизации.
        page: Номер страницы для пагинации (по умолчанию 0).

    Returns:
        Список словарей с данными о изображениях или сообщение об ошибке.
    """

    url = f"https://api.imgur.com/3/account/{username}/submissions/0/newest"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {
    'album_previews': '1',
    'client_id': client_id,
    }
    max_retries = 3
    retry_delay = 5

    async with aiohttp.ClientSession() as session:
        for attempt in range(max_retries):
            try:
                async with session.get(url, headers=headers,params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get('data', [])  # Возвращаем список изображений или пустой список
                    elif response.status == 503:
                        print(f"Attempt {attempt + 1}: Service unavailable (503). Retrying in {retry_delay} seconds...")
                        await asyncio.sleep(retry_delay)
                        continue
                    else:
                        response.raise_for_status()

            except aiohttp.ClientResponseError as e:
                print(f"Attempt {attempt + 1}: An error occurred: {e}")
                if attempt == max_retries - 1:
                    return {"error": str(e)}
                await asyncio.sleep(retry_delay)

        return {"error": "Max retries exceeded"}

async def __get_image(client_id, image_hash):
    """
    Получение информации об изображении по его хэшу.

    Args:
        client_id: Client ID вашего приложения Imgur.
        image_hash: Хэш изображения.

    Returns:
        Словарь с данными об изображении или сообщение об ошибке.
    """

    url = f"https://api.imgur.com/3/image/{image_hash}"
    headers = {"Authorization": f"Client-ID {client_id}"}
    max_retries = 3
    retry_delay = 5

    async with aiohttp.ClientSession() as session:
        for attempt in range(max_retries):
            try:
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get('data', {})  # Возвращаем данные об изображении или пустой словарь
                    elif response.status == 503:
                        print(f"Attempt {attempt + 1}: Service unavailable (503). Retrying in {retry_delay} seconds...")
                        await asyncio.sleep(retry_delay)
                        continue
                    else:
                        response.raise_for_status()

            except aiohttp.ClientResponseError as e:
                print(f"Attempt {attempt + 1}: An error occurred: {e}")
                if attempt == max_retries - 1:
                    return {"error": str(e)}
                await asyncio.sleep(retry_delay)

        return {"error": "Max retries exceeded"}

async def __get_image2(username, image_id, access_token):
    """
    Получение информации об изображении по его ID и имени пользователя.

    Args:
        username: Имя пользователя Imgur.
        image_id: ID изображения.
        access_token: OAuth2 access token пользователя.

    Returns:
        Словарь с данными об изображении или сообщение об ошибке.
    """

    url = f"https://api.imgur.com/3/account/{username}/image/{image_id}"
    headers = {"Authorization": f"Bearer {access_token}"}
    max_retries = 3
    retry_delay = 5

    async with aiohttp.ClientSession() as session:
        for attempt in range(max_retries):
            try:
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get('data', {})
                    elif response.status == 503:
                        print(f"Attempt {attempt + 1}: Service unavailable (503). Retrying in {retry_delay} seconds...")
                        await asyncio.sleep(retry_delay)
                        continue
                    else:
                        response.raise_for_status()

            except aiohttp.ClientResponseError as e:
                print(f"Attempt {attempt + 1}: An error occurred: {e}")
                if attempt == max_retries - 1:
                    return {"error": str(e)}
                await asyncio.sleep(retry_delay)

        return {"error": "Max retries exceeded"}

async def __image_update(access_token, image_hash, title=None, description=None):
    """
    Обновление информации о изображении.

    Args:
        access_token: Access token, полученный после авторизации.
        image_hash: Хэш изображения.
        title: Новый заголовок изображения (необязательно).
        description: Новое описание изображения (необязательно).

    Returns:
        Словарь с данными об изображении или сообщение об ошибке.
    """

    url = f"https://api.imgur.com/3/image/{image_hash}"
    headers = {"Authorization": f"Bearer {access_token}"}
    data = {}
    if title:
        data['title'] = title
    if description:
        data['description'] = description

    max_retries = 3
    retry_delay = 5

    async with aiohttp.ClientSession() as session:
        for attempt in range(max_retries):
            try:
                async with session.post(url, headers=headers, data=data) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get('data', {})  # Возвращаем обновленные данные изображения
                    elif response.status == 503:
                        print(f"Attempt {attempt + 1}: Service unavailable (503). Retrying in {retry_delay} seconds...")
                        await asyncio.sleep(retry_delay)
                        continue
                    else:
                        response.raise_for_status()

            except aiohttp.ClientResponseError as e:
                print(f"Attempt {attempt + 1}: An error occurred: {e}")
                if attempt == max_retries - 1:
                    return {"error": str(e)}
                await asyncio.sleep(retry_delay)

        return {"error": "Max retries exceeded"}
# Пример вызова функции
# asyncio.run(__upload_image('your_client_id', 'your_access_token', 'path/to/image.jpg', 'Title', 'Description'))


async def __get_albums(client_id, username, page=0):
    """
    Получение списка альбомов пользователя Imgur.

    Args:
        client_id: Client ID вашего приложения Imgur.
        username: Имя пользователя Imgur.
        page: Номер страницы для пагинации (по умолчанию 0).

    Returns:
        Список словарей с данными об альбомах или сообщение об ошибке.
    """

    url = f"https://api.imgur.com/3/account/{username}/albums/{page}"
    headers = {"Authorization": f"Client-ID {client_id}"}
    max_retries = 3
    retry_delay = 5

    async with aiohttp.ClientSession() as session:
        for attempt in range(max_retries):
            try:
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get('data', [])  # Возвращаем список альбомов или пустой список
                    elif response.status == 503:
                        print(f"Attempt {attempt + 1}: Service unavailable (503). Retrying in {retry_delay} seconds...")
                        await asyncio.sleep(retry_delay)
                        continue
                    else:
                        response.raise_for_status()

            except aiohttp.ClientResponseError as e:
                print(f"Attempt {attempt + 1}: An error occurred: {e}")
                if attempt == max_retries - 1:
                    return {"error": str(e)}
                await asyncio.sleep(retry_delay)

        return {"error": "Max retries exceeded"}


async def __get_feed(access_token):
    """
    Получение ленты пользователя.

    Args:
        access_token: OAuth2 access token пользователя.

    Returns:
        Словарь с данными о ленте или сообщение об ошибке.
    """

    url = "https://api.imgur.com/3/feed"
    headers = {"Authorization": f"Bearer {access_token}"}
    max_retries = 3
    retry_delay = 5

    async with aiohttp.ClientSession() as session:
        for attempt in range(max_retries):
            try:
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get('data', {})
                    elif response.status == 503:
                        print(f"Attempt {attempt + 1}: Service unavailable (503). Retrying in {retry_delay} seconds...")
                        await asyncio.sleep(retry_delay)
                        continue
                    else:
                        response.raise_for_status()

            except aiohttp.ClientResponseError as e:
                print(f"Attempt {attempt + 1}: An error occurred: {e}")
                if attempt == max_retries - 1:
                    return {"error": str(e)}
                await asyncio.sleep(retry_delay)

        return {"error": "Max retries exceeded"}

async def __process_images(username,client_id,access_token, views_limit=1000):
    """
    Получает изображения аккаунта, фильтрует их по просмотрам 
    и обновляет описания, добавляя ссылки на предыдущее и следующее изображения.
    
    Args:
        access_token: Access token, полученный после авторизации.
        views_limit: Минимальное количество просмотров для фильтрации.
    """

    images = await __get_account_images3(username,client_id,access_token)

    # Фильтрация изображений по количеству просмотров
    # filtered_images = [img for img in images if img.get('views', 0) > views_limit]
    # replace_dict={'qx4wO1W':'ntlA2rX','4WK2PO4':'mwQkU9z','skFYb2r':'iyvdNJe','M2iuvzM':'wUjLfes','wG1r8Je':'iXbV3nQ','WL5VryB':'fOgFUyq',"bHjR1qO":"PDzxDzz","wUslrzW":"sJ6itNF",
    # "3EMPXms":"Enq4tkW","u4ekpro":"27OtVkq","YkjW1RB":"5GMbSXo",
    # "mmqJYcW":"G9h4BtB","s":""}
    # for image in filtered_images:
    #     for key, value in replace_dict.items():
    #         image['id']=image['id'].replace(key,value)
    filtered_images=images
    # Обновление описаний изображений
    for i, image in enumerate(filtered_images):
        description_parts = []
        if i > 0:
            prev_image = filtered_images[i - 1]
            description_parts.append(f"next post https://imgur.com/gallery/{prev_image['id']}")
        if i < len(filtered_images) - 1:
            next_image = filtered_images[i + 1]
            description_parts.append(f"previous post https://imgur.com/gallery/{next_image['id']}")
        
        new_description = "\n".join(description_parts)
        if new_description:
            await __image_update(access_token, image.get('cover', image.get('id')), description=new_description)

async def __get_gallery_image(client_id, gallery_image_hash):
    """
    Получение информации об изображении из галереи по его хэшу.

    Args:
        client_id: Client ID вашего приложения Imgur.
        gallery_image_hash: Хэш изображения из галереи.

    Returns:
        Словарь с данными об изображении или сообщение об ошибке.
    """

    url = f"https://api.imgur.com/3/gallery/image/{gallery_image_hash}"
    headers = {"Authorization": f"Client-ID {client_id}"}
    max_retries = 3
    retry_delay = 5

    async with aiohttp.ClientSession() as session:
        for attempt in range(max_retries):
            try:
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get('data', {})
                    elif response.status == 503:
                        print(f"Attempt {attempt + 1}: Service unavailable (503). Retrying in {retry_delay} seconds...")
                        await asyncio.sleep(retry_delay)
                        continue
                    else:
                        response.raise_for_status()

            except aiohttp.ClientResponseError as e:
                print(f"Attempt {attempt + 1}: An error occurred: {e}")
                if attempt == max_retries - 1:
                    return {"error": str(e)}
                await asyncio.sleep(retry_delay)

        return {"error": "Max retries exceeded"}

async def __get_gallery(client_id, section="hot", sort="viral", window="day", page=1, show_viral=True, show_mature=False, album_previews=True):
    """
    Получение информации о галерее.

    Args:
        client_id: Client ID вашего приложения Imgur.
        section: Секция галереи (например, "hot", "top", "user"). По умолчанию "hot".
        sort: Сортировка (например, "viral", "time", "rising"). По умолчанию "viral".
        window: Временной интервал (например, "day", "week", "month", "year", "all"). 
                По умолчанию "day".
        page: Номер страницы. По умолчанию 1.
        show_viral: Показывать ли вирусный контент. По умолчанию True.
        show_mature: Показывать ли контент для взрослых. По умолчанию False.
        album_previews: Показывать ли превью альбомов. По умолчанию True.

    Returns:
        Словарь с данными о галерее или сообщение об ошибке.
    """

    url = f"https://api.imgur.com/3/gallery/{section}/{sort}/{window}/{page}"
    params = {
        "showViral": str(show_viral).lower(),
        "mature": str(show_mature).lower(),
        "album_previews": str(album_previews).lower(),
    }
    headers = {"Authorization": f"Client-ID {client_id}"}
    max_retries = 3
    retry_delay = 5

    async with aiohttp.ClientSession() as session:
        for attempt in range(max_retries):
            try:
                async with session.get(url, headers=headers, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get('data', {})
                    elif response.status == 503:
                        print(f"Attempt {attempt + 1}: Service unavailable (503). Retrying in {retry_delay} seconds...")
                        await asyncio.sleep(retry_delay)
                        continue
                    else:
                        response.raise_for_status()

            except aiohttp.ClientResponseError as e:
                print(f"Attempt {attempt + 1}: An error occurred: {e}")
                if attempt == max_retries - 1:
                    return {"error": str(e)}
                await asyncio.sleep(retry_delay)

        return {"error": "Max retries exceeded"}

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

    # е=await __get_gallery_image(client_id,"qx4wO1W")
    # t=await __get_gallery_image(client_id, "qx4wO1W")
    t=await __get_account_images2(access_token)
    await __process_images("LaplandImg",client_id,access_token)
    # import json
    # with open('t.json', 'w', encoding='utf-8') as f:
    #     json.dump(t, f)
    # t=await __get_gallery(client_id)
    # t=await __get_image2("LaplandImg", "qx4wO1W", access_token)
    # t=await __get_feed(access_token)

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

