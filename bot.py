#%%
import telebot
token="5918821809:AAEX3SB9rIreD8CLOmsRLF2wB85ABUBquo4"

#%%
bot = telebot.TeleBot(token)
# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Hi there, I am EchoBot.
I am here to echo your kind words back to you. Just say anything nice and I'll say the exact same thing to you!\
""")


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)


@bot.message_handler(content_types=['video'])
def handle_docs_video(message):
    file_name = message.json['video']['file_name']
    file_info = bot.get_file(message.video.file_id)
    print(file_info.file_path)
    with open(file_name, "wb") as f:
        file_content = bot.download_file(file_info.file_path)
        f.write(file_content)
    bot.reply_to(message, f"OK. Сохранил {file_name}")

#%%
bot.infinity_polling()
# %%
# class VideoProvider():
#     pass

#     def pr():
#         print("dd")