import time
import vk_api
import uuid

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
        self.login="+79006398664"
        self.group_id = -129592796
        self.password="Z0YVyjWe47!fd-S"
        self.token="vk1.a.iAT3_sClCSwAkAMSGMc78Oi5ELK_Fi3ErGgsWS-J9sBDsUCzpLNvCX0fYs_hqHx5inT9zmBZCeOu76_DMOrNUv-S8P08Uog7e7ShbcVDUV-Sev81L4pz-FhD1zjgtqwYZ1PHX2eytXlvCzyD_NKzBU-5Uv_xT0gNjisyAZnxqEuRQhg5jpSHr1RA6D9Gd4PyzjxUm94oizkuGYK7PTQ_bg"
        self.vk_session = vk_api.VkApi(
            login="+79006398664",
            password="Z0YVyjWe47!fd-S",
            auth_handler=self.auth_handler,
            token="vk1.a.iAT3_sClCSwAkAMSGMc78Oi5ELK_Fi3ErGgsWS-J9sBDsUCzpLNvCX0fYs_hqHx5inT9zmBZCeOu76_DMOrNUv-S8P08Uog7e7ShbcVDUV-Sev81L4pz-FhD1zjgtqwYZ1PHX2eytXlvCzyD_NKzBU-5Uv_xT0gNjisyAZnxqEuRQhg5jpSHr1RA6D9Gd4PyzjxUm94oizkuGYK7PTQ_bg",
            captcha_handler=captcha_handler,# функция для обработки капчи
            # app_id=6287487  
            )
        self.vk_session.auth()
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
