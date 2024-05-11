import asyncio
import logging
import re
import time
import uuid
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot, Dispatcher, executor, types
from instagram_parser import InstagramParser, InstagramPostInfo
import requests
from unittest.mock import Mock
class ContentProvider():
    logging.basicConfig(level=logging.INFO)
    pass

class VideoProvider(ContentProvider):
    def __init__(self):
        self.token = "5918821809:AAEX3SB9rIreD8CLOmsRLF2wB85ABUBquo4"
        self.bot = Bot(token=self.token)
        self.dp = Dispatcher(self.bot)
        self.scheduler = AsyncIOScheduler()
        self.scheduler.add_job(self.video_handler_cycle, "interval", seconds=50)
        self.video_handling_flag=True

        @self.dp.message_handler(content_types=types.ContentTypes.VIDEO)
        async def handle_docs_video(message: types.Message):
            await self.handle_docs_video(message)
            
        # @self.bot.message_handler(func=lambda message: True)
        # def echo_message(message):
        #     self.echo_message(message)
        @self.dp.message_handler(content_types=types.ContentTypes.TEXT)
        async def handle_docs_url(message: types.Message):
            await self.handle_docs_url(message)

        @self.dp.message_handler(commands=['loadurl'])
        def Loadurl(message):
            self.Loadurl(message)

        @self.dp.message_handler(commands=['loadvid'])
        def Video_loading_start(message):
            self.video_handling_flag=True
            self.bot.reply_to(message, 'Please load video:')
        
        @self.dp.message_handler(commands=['stoploadvid'])
        def Video_loading_start(message):
            self.video_handling_flag=False
            self.bot.reply_to(message, 'video will not loading')

        self.vid_func=None
        self.url_func=None
        self.video_queue = asyncio.Queue()

    def is_url(self,message: str) -> bool:
        url_regex = re.compile(
            r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        )
        return bool(url_regex.match(message))
    
    def is_instagram_url(self,message: str) -> bool:
        instagram_url_regex = re.compile(
            r'^https://www\.instagram\.com/.*$'
        )
        return bool(instagram_url_regex.match(message))
    
    async def handle_docs_url(self,message: types.Message):
        await self.bot.send_message(chat_id=message.chat.id, text="Check url...")
        if not self.is_url(message.text):
            await self.bot.send_message(chat_id=message.chat.id, text="It's not url")
            return
        if not self.is_instagram_url(message.text):
            await self.bot.send_message(chat_id=message.chat.id, text="It's not instagram url")
            return
        message.author_signature="inst_url"
        await self.video_queue.put(message)


    async def extract_video_url(self,message):
        await self.bot.send_message(chat_id=message.chat.id, text="Extracting video url...")
        url_or_shortcode = message.text
        parser = InstagramParser(url_or_shortcode)
        post_info = InstagramPostInfo(parser)
        video_url = post_info.video_url
        await self.bot.send_message(chat_id=message.chat.id, text=f"Video url: {video_url}")
        description = post_info.description
        if description:
            await self.bot.send_message(chat_id=message.chat.id, text=f"Description: {description}")
        parser.clear_cache()
        return video_url
        
        pass
        # await self.url_func(message.text)
    async def handle_docs_video(self,message: types.Message):
        await self.video_queue.put(message)
        # await self.video_handler_cycle()

    async def video_handler_cycle(self):
        if self.video_queue.qsize()>0:
            message = await self.video_queue.get()
            await self.video_handler(message)
            self.video_queue.task_done()
        # while True:
        #     if self.video_queue.qsize()>0:
        #         message = await self.video_queue.get()
        #         await self.video_handler(message)
        #         time.sleep(1)
        #         self.video_queue.task_done()

    async def video_handler(self, message):
        self.message=message
        if self.video_handling_flag is False: return
        if message.author_signature=="inst_url":
            if self.video_handling_flag is False: return
            video_url=await self.extract_video_url(message)
            response = requests.get(video_url)
            vid_uuid = str(uuid.uuid4())
            file_name="video"+vid_uuid+".mp4"
            with open(file_name, 'wb') as f:
                f.write(response.content)
            await self.bot.send_message(chat_id=message.chat.id, text="Video is loaded")
            await self.vid_func(file_name)
        else:
            await self.bot.send_message(chat_id=message.chat.id, text="Start loading...")
            vid_uuid = str(uuid.uuid4())
            file_name="video"+vid_uuid+".mp4"
            file_id = message.video.file_id
            file_info = await self.bot.get_file(file_id)
            print(file_info.file_path)
            await self.bot.download_file(file_info.file_path, file_name)
            await self.bot.send_message(chat_id=message.chat.id, text="Video is loaded")
            await self.vid_func(file_name)
        # self.video_handling_flag=False

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
        # loop=asyncio.get_event_loop()
        # loop.create_task(self.video_handler_cycle())
        # self.dp.loop.create_task(self.video_handler_cycle())
        # self.dp.loop.create_task(self.video_handler_cycle())
        # asyncio.create_task(self.video_handler_cycle())
        # asyncio.run(self.start_async())
        self.scheduler.start()
        executor.start_polling(self.dp, skip_updates=True)

        # self.dp.loop.create_task(self.video_handler_cycle())

    async def on_startup(self,_):
        await asyncio.create_task(self.scheduler.start())

    async def start_async(self):
        executor.start_polling(self.dp, skip_updates=True)

    async def func_log(self,text):
        # await self.bot.send_message(chat_id=self.message.chat.id, text=text)
        await self.bot.send_message(chat_id=self.message.chat.id, text=text)
        

    # @dp.message_handler(content_types=types.ContentTypes.TEXT)
    # async def echo(message: types.Message):
    #     await bot.send_message(chat_id=message.chat.id, text=message.text)
        