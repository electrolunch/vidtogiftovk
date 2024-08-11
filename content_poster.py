from enum import IntEnum
import os
import time
import jconfig.memory
import vk_api
import uuid
import requests
from aiogram.types import InputFile
from tenacity import retry, stop_after_attempt, wait_fixed
import jconfig 
import getpass
import tools as tools
import aiohttp
import asyncio
import random
from datetime import datetime

class ContentPoster():
    pass
download_dir = 'downloads'
def auth_handler():
    """ При двухфакторной аутентификации вызывается эта функция."""
    # Код двухфакторной аутентификации
    key = input("Enter authentication code: ")
    # Если: True - сохранить, False - не сохранять.
    remember_device = True
    return key, remember_device

def captcha_handler(captcha):
    """ При возникновении капчи вызывается эта функция и ей передается объект
        капчи. Через метод get_url можно получить ссылку на изображение.
        Через метод try_again можно попытаться отправить запрос с кодом капчи
    """

    key = input("Enter captcha code {0}: ".format(captcha.get_url())).strip()

    # Пробуем снова отправить запрос с капчей
    return captcha.try_again(key)

class Permissions1(IntEnum):
    """
    Перечисление прав пользователя.
    Список прав получается побитовым сложением (x | y) каждого права.
    Подробнее в документации VK API: https://vk.com/dev/permissions
    """

    #: Пользователь разрешил отправлять ему уведомления
    #: (для flash/iframe-приложений).
    #: Не работает с этой библиотекой.
    # NOTIFY = 1

    #: Доступ к друзьям.
    FRIEND = 2

    #: Доступ к фотографиям.
    PHOTOS = 2**2

    #: Доступ к аудиозаписям.
    #: При отсутствии доступа к закрытому API аудиозаписей это право позволяет
    #: только загрузку аудио.
    # AUDIO = 2**3

    #: Доступ к видеозаписям.
    VIDEO = 2**4

    # : Доступ к историям.
    STORIES = 2**6

    #: Доступ к wiki-страницам.
    # PAGES = 2**7

    #: Добавление ссылки на приложение в меню слева.
    # ADD_LINK = 2**8

    #: Доступ к статусу пользователя.
    # STATUS = 2**10

    #: Доступ к заметкам пользователя.
    # NOTES = 2**11

    #: Доступ к расширенным методам работы с сообщениями.
    # MESSAGES = 2**12

    #: Доступ к обычным и расширенным методам работы со стеной.
    WALL = 2**13

    #: Доступ к расширенным методам работы с рекламным API.
    # ADS = 2**15

    #: Доступ к API в любое время. Рекомендуется при работе с этой библиотекой.
    OFFLINE = 2**16

    #: Доступ к документам.
    DOCS = 2**17

    #: Доступ к группам пользователя.
    # GROUPS = 2**18

    #: Доступ к оповещениям об ответах пользователю.
    # NOTIFICATIONS = 2**19

    #: Доступ к статистике групп и приложений пользователя, администратором которых он является.
    # STATS = 2**20

    #: Доступ к email пользователя.
    # EMAIL = 2**22

    #: Доступ к товарам.
    # MARKET = 2**27

class VkPoster(ContentPoster):
    def __init__(self):
        self.login="+79006398664"
        self.group_id = -129592796
        self.password="Dbdh566)/$"
        self.token=getpass.getpass("Введите token: ")
        self.vk_session = vk_api.VkApi(
            # login=self.login,
            # password=self.password,
            auth_handler=self.auth_handler,
            token=self.token,
            captcha_handler=captcha_handler,# функция для обработки капчи
            app_id=51944886,
            # app_id=1,
            # config=jconfig.memory.MemoryConfig,
            # api_version='5.131',
            scope=sum(Permissions1)
            )
        # self.vk_session.auth()
        self.vk = self.vk_session.get_api()
        self.upload = vk_api.VkUpload(self.vk_session)

    def auth_handler(self):
        key = input("Enter authentication code: ")
        # Если: True - сохранить, False - не сохранять.
        remember_device = True
        return key, remember_device

    async def LoadAndPostToPioner(self,doc_path,log_func):
        # gif_uuid = str(uuid.uuid4())
        await log_func(f"start uploading doc {doc_path}")
        doc = self.upload.document(doc_path, os.path.basename(doc_path))
        # doc = self.upload.document_message(gif_path,peer_id=19156483)
        self.vk.wall.post(owner_id=self.group_id,message="", 
        attachments=[f"doc{doc['doc']['owner_id']}_{doc['doc']['id']}"])
        await log_func("doc uploaded to vk")
        return doc_path
    
    async def LoadSnegovikStory(self,video_path,log_func):
        # gif_uuid = str(uuid.uuid4())
        await log_func(f"start uploading video {video_path}")
        doc = self.upload.story(video_path, file_type="video",link_url=r"https://vk.com/vk_lapland")
        # doc = self.upload.document_message(gif_path,peer_id=19156483)
        self.vk.wall.post(owner_id=self.group_id,message="", 
        attachments=[f"doc{doc['doc']['owner_id']}_{doc['doc']['id']}"])
        await log_func("doc uploaded to vk")
        return doc
    def calculate_age(self,date_str):
        if not date_str:
            return "Дата не указана"
        
        try:
            # Предполагаем, что формат даты - день.месяц.год
            day, month, year = map(int, date_str.split('.'))
            birth_date = datetime(year, month, day)
            today = datetime.today()
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            return age
        except ValueError:
            return "error"

    async def add_random_friend_from_suggestions(self,log_func):
        my_id=617202016


        for i in range(50):
            await log_func("get friends_getSuggestions")
            friends_getSuggestions=self.vk_session.method('friends.getSuggestions', {'count': 100, 'fields': 'bdate'})

            friends_getSuggestions_has_bdate = [friend for friend in friends_getSuggestions['items'] if friend.get('bdate')]
            friends_getSuggestions_has_year = [friend for friend in friends_getSuggestions_has_bdate if self.calculate_age(friend['bdate']) != "error"]
            print("friends_getSuggestions_over_40 = [...]")
            friends_getSuggestions_over_40 = [friend for friend in friends_getSuggestions_has_year if self.calculate_age(friend['bdate']) > 40]
            if len(friends_getSuggestions_over_40) != 0:
                break
            time.sleep(3)

        if len(friends_getSuggestions_over_40) == 0:
            return

        friends_getSuggestions["items"]=friends_getSuggestions_over_40

        random_friend = random.choice(friends_getSuggestions["items"])
        await log_func("get friends_getMutual")
        friends_getMutual=self.vk_session.method('friends.getMutual', {'source_uid':my_id , "target_uid": random_friend['id'],"order":"random","need_common_count":1})
        friends_getMutual_count=friends_getMutual['common_count']
        print(friends_getMutual_count)
        await log_func(f"friends_getMutual_count {friends_getMutual_count}")
        if friends_getMutual_count > 1:
            t=self.vk_session.method('friends.add', {'user_id': random_friend['id']})
            return "ok"
    

class Tposter(ContentPoster):
    def __init__(self,scheduler,dp):
        self.scheduler=scheduler
        self.dp=dp
        self.bot=dp.bot
        self.channel_id='@t_lapland'


    async def post_to_tg(self, vk_post_data, log_func):
        try:
            type = vk_post_data['attachments'][0]['type']
            text = vk_post_data['text']
            file_hash = vk_post_data['hash']
            print(text)

            if type == 'photo':
                url = vk_post_data['attachments'][0][type]['sizes'][-1]['url']
                await log_func(url)
                await self.send_photo(text, url)
                self.write_hash_to_file(file_hash)
                
            elif type == 'doc':
                url = vk_post_data['attachments'][0][type]['url']
                filepath = await self.download_file(url)
                await log_func(url)
                await self.send_doc2(text, filepath)
                os.remove(filepath)
                self.write_hash_to_file(file_hash)
                return filepath

        except Exception as e:
            if "File too large for uploading" in str(e):
                self.write_hash_to_file(file_hash)
            if "not found" in str(e):
                self.write_hash_to_file(file_hash)
            await log_func(str(e))

    def write_hash_to_file(self,file_hash, filename='hash.txt'):
        tools.write_line_to_file(file_hash, filename)

    def remove_hash_from_file(self,file_hash, filename='hash.txt'):
        tools.remove_line_from_file(file_hash, filename)

    async def download_file(self,url, download_dir=download_dir):
        response = requests.get(url)
        filename = url.split('/')[-1].split('_')[0] + '.gif'
        filepath = os.path.join(download_dir, filename)
        with open(filepath, 'wb') as f:
            f.write(response.content)
        return filepath
            
    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    async def send_doc(self, text, url):
        try:
            await self.bot.send_document(chat_id=self.channel_id, document=url,caption=text)
        except Exception as e:
            raise e

    # def send_doc2_retry_error_callback(last_exception, attempt_number):
    #     return None # echo -n > filename.txt
    
    # @retry(stop=stop_after_attempt(3), wait=wait_fixed(2), retry_error_callback=send_doc2_retry_error_callback)
    async def send_doc2(self, text, filepath):
        input_file = InputFile(filepath)
        await self.bot.send_animation(chat_id=self.channel_id, animation=input_file,caption=text)

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    async def send_photo(self, text, url):
        await self.bot.send_photo(chat_id=self.channel_id, photo=url,caption=text)
        # await self.bot.send_message(self.channel_id, text)

    async def write_message(self, text,LogFunc):
        await self.bot.send_message(self.channel_id, text)


class ImgurPoster(ContentPoster):
    def __init__(self,scheduler):
        self.scheduler=scheduler
        self.channel_id='@t_lapland'
        client_id = "5c58ec0f53b4cc1"
        self.client_id = client_id
        client_secret = "953870f77524e3742c55571ac4cd2811fd0162a2"
        self.client_secret = client_secret


    async def authenticate(self):
        client_id=self.client_id
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
    async def get_access_token(self,client_id=None, client_secret=None):
        line=""
        with open("imgtok.txt", "r") as f:
            line = f.read().strip()
        
        # Извлечение токена из строки
        if line.startswith("access_token="):
            tok = line.split("=", 1)[1].strip("'\"")
        else:
            tok = await self.authenticate(client_id, client_secret)
            if tok is None:
                print("Не удалось получить токен. Попробуйте ещё раз.")
                return
            with open("imgtok.txt", "w") as f:
                f.write(f"access_token={tok}")

        return tok
    async def __upload_image(self,client_id, access_token, image_path, title, description):
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
    
    async def post_video(self, video_path,log_func, title=".", description=""):
        try:
            await log_func(f"start uploading video to imgur {video_path}")
            access_token = await self.get_access_token()
            response = await self.__upload_image(self.client_id, access_token, video_path, title, description)
            if "error" in response:
                await log_func("Ошибка при загрузке изображения:")
                await log_func(response["error"])
                return None
            self.v_link = response['data']['link']
            return response
        except Exception as e:
            await log_func(e)
