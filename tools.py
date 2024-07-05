from moviepy.editor import VideoFileClip

import os
def remove_audio_from_video(input_path, output_path):
    # Загрузить видео
    video = VideoFileClip(input_path)
    
    try:
        # Удалить аудио
        video_no_audio = video.without_audio()
        
        # Сохранить результат
        video_no_audio.write_videofile(output_path, codec='libx264')
    finally:
        # Закрыть видеофайлы
        video.close()
        video_no_audio.close()



def add_string_to_filename(filename, string_to_add):
    # Разделить имя файла и его расширение
    name, ext = os.path.splitext(filename)
    
    # Добавить строку к имени файла
    new_name = f"{name}{string_to_add}{ext}"
    
    return new_name