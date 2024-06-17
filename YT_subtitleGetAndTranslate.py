from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
from googletrans import Translator
from datetime import timedelta
import re

def format_time(seconds):
    """
    Converts seconds to SRT time format (HH:MM:SS,MS).
    """
    delta = timedelta(seconds=seconds)
    hours, remainder = divmod(delta.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)
    seconds, milliseconds = divmod(seconds, 1)
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02},{int(milliseconds*1000):03}"

def sanitize_filename(filename):
    """
    Sanitizes a string to be used as a valid filename.
    """
    return re.sub(r'[\/:*?"<>|]', '_', filename)

# 輸入影片URL
video_url = 'https://www.youtube.com/watch?v=d3UTywBDSW4'

# 獲取影片信息
yt = YouTube(video_url)
video_id = yt.video_id
video_title = sanitize_filename(yt.title)  # 清理文件名

# 獲取字幕
transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

# 選擇需要的語言的字幕
transcript = transcript_list.find_transcript(['ja'])  # 選擇日語字幕
transcript_data = transcript.fetch()

# 提取所有需要翻譯的文本
texts_to_translate = [entry['text'] for entry in transcript_data]

# 初始化翻譯器
translator = Translator()

# 嘗試逐條翻譯文本
translated_texts = []
for text in texts_to_translate:
    try:
        translated = translator.translate(text, dest='zh-tw')
        if translated and translated.text:
            translated_texts.append(translated.text)
        else:
            translated_texts.append(text)
            print(f"翻譯失敗，API返回None，原文保留: {text}")
    except Exception as e:
        translated_texts.append(text)  # 如果翻譯失敗，保留原文本
        print(f"翻譯 '{text}' 失敗: {e}")
    

# 將翻譯後的文本與時間戳配對
translated_transcript = []
for entry, translated_text in zip(transcript_data, translated_texts):
    translated_transcript.append({
        'start': entry['start'],
        'duration': entry['duration'],
        'original_text': entry['text'],
        'translated_text': translated_text
    })

# 保存為srt文件，使用影片標題作為文件名
with open(f'{video_title}_translated.srt', 'w', encoding='utf-8') as file:
    for idx, entry in enumerate(translated_transcript):
        start = format_time(entry['start'])
        end = format_time(entry['start'] + entry['duration'])
        original_text = entry['original_text']
        translated_text = entry['translated_text']
        file.write(f'{idx + 1}\n')
        file.write(f'{start} --> {end}\n')
        file.write(f'{original_text}\n')
        file.write(f'{translated_text}\n\n')

print(f"翻譯後的字幕文件已保存為: {video_title}_translated.srt")
