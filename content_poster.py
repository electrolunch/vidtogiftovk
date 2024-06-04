import time
import vk_api
import uuid
from tenacity import retry, stop_after_attempt, wait_fixed
class ContentPoster():
    pass

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

class VkPoster(ContentPoster):
    def __init__(self):
        self.login="+00000"
        self.group_id = -129592796
        self.password=")))))"
        self.token="vk1.eeee"
        self.vk_session = vk_api.VkApi(
            # login=self.login,
            # password=self.password,
            # auth_handler=self.auth_handler,
            token="vk1.a.mFcyBXeNbNk2Ke9JALkKsNq8wn0sNeHtXGTACd8t3G0Yp602uszs_wClOH-m9PW72nJD09KnU6bu77sTmwl11rQ_IV7euur_idf3hPYX-iORPGLfh-iPrpXvVHKxNtPV8I-IGg91g1_MN3uVvLQrt-YjIZMhOjLyz6URns-LNN1p65I0XeMGHffbnzTO_FZOWURi1gJbyDegqtZYtuqMMQ",
            # captcha_handler=captcha_handler,# функция для обработки капчи
            # app_id=7614654  
            # app_id=3698024
            )
        # self.vk_session.auth()
        self.vk = self.vk_session.get_api()
        self.upload = vk_api.VkUpload(self.vk_session)

    def auth_handler(self):
        key = input("Enter authentication code: ")
        # Если: True - сохранить, False - не сохранять.
        remember_device = True
        return key, remember_device

    async def LoadAndPostToPioner(self,gif_path,log_func):
        # gif_uuid = str(uuid.uuid4())
        await log_func(f"start uploading gif {gif_path}")
        doc = self.upload.document(gif_path,gif_path)
        # doc = self.upload.document_message(gif_path,peer_id=19156483)
        self.vk.wall.post(owner_id=self.group_id,message="", 
        attachments=[f"doc{doc['doc']['owner_id']}_{doc['doc']['id']}"])
        await log_func("gif uploaded to vk")
        return gif_path

class Tposter(ContentPoster):
    def __init__(self,scheduler,dp):
        self.scheduler=scheduler
        self.dp=dp
        self.bot=dp.bot
        self.channel_id='@t_lapland'

    async def post_to_tg(self,vk_post_data,log_func):
        try:
            # print(vk_post_data)
            type=vk_post_data['attachments'][0]['type']
            text=vk_post_data['text']
            print(text)
            if type=='photo':
                url=vk_post_data['attachments'][0][type]['sizes'][-1]['url']
                await log_func(url)
                await self.send_photo(text, url)
            if type=='doc':
                url=vk_post_data['attachments'][0][type]['url']
                await log_func(url)
                await self.send_doc(text, url)
        except Exception as e:
            await log_func(str(e))
            
    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    async def send_doc(self, text, url):
        await self.bot.send_animation(chat_id=self.channel_id, animation=url,caption=text)

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    async def send_photo(self, text, url):
        await self.bot.send_photo(chat_id=self.channel_id, photo=url,caption=text)
        # await self.bot.send_message(self.channel_id, text)