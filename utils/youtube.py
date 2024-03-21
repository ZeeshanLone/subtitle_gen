import os
import youtube_dl

def download_from_youtube(video_url, audio_only=True):
    videoinfo = youtube_dl.YoutubeDL().extract_info(url = video_url, download=False)
    filename = None
    options = None
    if audio_only:
        filename = os.path.join(os.getcwd(), 'audio', "%(id)s.%(ext)s")
        if not os.path.exists(os.path.join(os.getcwd(), 'audio')):
            os.makedirs(os.path.join(os.getcwd(), 'audio'))
        # options = {
        # # 'format': 'bestaudio/best',
        # 'format': 'worstaudio/worst',
        # 'keepvideo': False,
        # 'outtmpl': filename,
        # 'postprocessors': [{
        # 'key': 'FFmpegExtractAudio',
        # 'preferredcodec': 'mp3',
        # 'preferredquality': '192',
        # }],
        # 'quiet': False,
        # }
        options = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
                'preferredquality': '192'
            }],
            'postprocessor_args': [
                '-ar', '16000'
            ],
            'prefer_ffmpeg': True,
            'keepvideo': False,
            'outtmpl': filename,
        }
        
    else:
        filename = os.path.join(os.getcwd(), 'video', "%(id)s.%(ext)s")
        if not os.path.exists(os.path.join(os.getcwd(), 'video')):
            os.makedirs(os.path.join(os.getcwd(), 'video'))
        options = {
        'format': 'best',
        'keepvideo': True,
        'outtmpl': filename,
        }


    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([videoinfo['webpage_url']])
    return os.path.join(os.path.split(filename)[0], f"{videoinfo['id']}.{'wav' if audio_only else 'mp4'}"), audio_only
