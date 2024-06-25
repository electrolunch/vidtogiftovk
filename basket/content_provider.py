import uuid
import telebot


class ContentProvider():
    pass

class VideoProvider(ContentProvider):
    def __init__(self):
        self.token = "5918821809:AAEX3SB9rIreD8CLOmsRLF2wB85ABUBquo4"
        self.bot = telebot.TeleBot(self.token)
        self.video_handling_flag=True

        @self.bot.message_handler(content_types=['video'])
        def handle_docs_video(message):
            self.handle_docs_video(message)
            
        # @self.bot.message_handler(func=lambda message: True)
        # def echo_message(message):
        #     self.echo_message(message)

        @self.bot.message_handler(commands=['loadurl'])
        def Loadurl(message):
            self.Loadurl(message)

        @self.bot.message_handler(commands=['loadvid'])
        def Video_loading_start(message):
            self.video_handling_flag=True
            self.bot.reply_to(message, 'Please load video:')
        
        @self.bot.message_handler(commands=['stoploadvid'])
        def Video_loading_start(message):
            self.video_handling_flag=False
            self.bot.reply_to(message, 'video will not loading')

        self.vid_func=None
        self.url_func=None
    

    def Loadurl(self,message):
        print(message)
        # self.url_func(url)

    def send_welcome(self,message):
        self.bot.reply_to(message, "I'm ROBOT")
    

    def CallBack(func):
        print("dd")

    def SetUrlHandler(self,func):
        self.url_func=func

    def SetVideoHandler(self,func):
        self.vid_func=func

    def Start(self):
        self.bot.infinity_polling()

    
    def handle_docs_video(self,message):
        # file_name = message.json['video']['file_name']
        self.message=message
        if self.video_handling_flag is False: return
        self.bot.reply_to(message, "Start loading...")
        vid_uuid = str(uuid.uuid4())
        file_name="video"+vid_uuid+".mp4"
        file_info = self.bot.get_file(message.video.file_id)
        print(file_info.file_path)
        with open(file_name, "wb") as f:
            file_content = self.bot.download_file(file_info.file_path)
            f.write(file_content)
        self.bot.reply_to(message, "Video is loaded")
        self.vid_func(file_name)
        # self.video_handling_flag=False

    def func_log(self,text):
        self.bot.reply_to(self.message, text)
        

    def echo_message(self,message):
        self.bot.reply_to(message, message.text)
        