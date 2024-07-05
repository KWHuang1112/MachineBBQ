from pytube import YouTube
import whisper
import os

# 使用的統一變數
youtube_url = 'https://www.youtube.com/watch?v=fwn0U6yfrRA'
output_path = 'C:/Users/KW_Huang/Desktop/YT_subtitleGet/test'

def download_youtube_video(url, output_path):
    yt = YouTube(url)
    video_stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    video_stream.download(output_path)
    return video_stream.default_filename

def write_srt(segments, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        for i, segment in enumerate(segments):
            start = segment['start']
            end = segment['end']
            text = segment['text']
            file.write(f"{i + 1}\n")
            file.write(f"{format_timestamp(start)} --> {format_timestamp(end)}\n")
            file.write(f"{text}\n\n")

def format_timestamp(seconds):
    millisec = int((seconds % 1) * 1000)
    seconds = int(seconds)
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds:02},{millisec:03}"

def generate_subtitles(video_path, output_path):
    model = whisper.load_model("base")
    result = model.transcribe(video_path, language='ja')
    srt_path = os.path.join(output_path, os.path.basename(video_path).replace('.mp4', '.srt'))
    write_srt(result['segments'], srt_path)
    return srt_path


# 下載YouTube影片
video_filename = download_youtube_video(youtube_url, output_path)

# 生成日文字幕
srt_path = generate_subtitles(os.path.join(output_path, video_filename), output_path)

