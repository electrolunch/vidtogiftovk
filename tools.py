from moviepy.editor import VideoFileClip
import subprocess
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

def remove_audio_ffmpeg(input_path, output_path):
    # Команда для удаления аудио с помощью FFmpeg
    command = [
        'ffmpeg', 
        '-i', input_path,  # Входной файл
        '-c', 'copy',      # Копировать видео и аудио потоки без перекодирования
        '-an',             # Удалить все аудиодорожки
        output_path        # Выходной файл
    ]
    
    # Запуск команды
    subprocess.run(command, check=True)

def add_string_to_filename(filename, string_to_add):
    # Разделить имя файла и его расширение
    name, ext = os.path.splitext(filename)
    
    # Добавить строку к имени файла
    new_name = f"{name}{string_to_add}{ext}"
    
    return new_name


def write_line_to_file(file_line, filename='temp.txt'):
    with open(filename, 'a') as f:
        f.write(file_line + '\n')

def remove_line_from_file(file_line, filename='temp.txt'):
    if not os.path.isfile(filename):
        return
    with open(filename, 'r') as f:
        lines = f.readlines()
    with open(filename, 'w') as f:
        for line in lines:
            if line.strip() != file_line:
                f.write(line)

def check_line_in_file(file_line, filename='temp.txt'):
    if not os.path.isfile(filename):
        return False
    with open(filename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if line.strip() == file_line:
                return True
    return False