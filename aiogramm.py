#%%
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
token="5918821809:AAEX3SB9rIreD8CLOmsRLF2wB85ABUBquo4"
bot = Bot(token=token)

dp = Dispatcher(bot)
#%%
@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def echo(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text=message.text)

@dp.message_handler(content_types=types.ContentTypes.VIDEO)
async def download_video(message: types.Message):
    print("1")
    await bot.send_message(chat_id=message.chat.id, text="video")
    # Get the file ID of the video
    file_id = message.video.file_id
    # # Get the file path of the video
    file = await bot.get_file(file_id)
    print("2")
    # # Download the video
    await bot.download_file(file.file_path, r'PythonApplication1\video.mp4')
    # # Send a message to confirm that the video was downloaded
    await bot.send_message(chat_id=message.chat.id, text='Video was downloaded!')

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(msg: types.Message):
    await msg.reply_to_message("hjhh")
#%%

# dp.start_polling(bot)

if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp)
# async def main():
#     dp.start_polling(bot)
    
# main()
# Запуск процесса поллинга новых апдейтов
# async def main():
#     await dp.start_polling(bot)

# if __name__ == "__main__":
#     asyncio.run(main())
#%%
# if __name__ == "__main__":
#     dp.start_polling()
# %%
