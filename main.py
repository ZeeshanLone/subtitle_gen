import argparse
import re
from utils.youtube import download_from_youtube
from utils import get_audio_from_video, get_transcription, generate_subtitles, audio_utils



def is_youtube_url(url):
    youtube_regex = r'^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube(-nocookie)?\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|live\/|v\/)?)([\w\-]+)(\S+)?$'
    return bool(re.match(youtube_regex, url))



    

if __name__=="__main__":
    parser = argparse.ArgumentParser() 
    parser.add_argument('--video_path', help="Path to video file or a youtube link of the video.", required=True)
    parser.add_argument('--download_audio', help="Set if you want to download .", required=False, action='store_true')
    parser.add_argument('--audio_only', help="Set if input is audio file.", required=False, action='store_true')
    parser.add_argument('--sup_size', help="Number of words to display at one time. Default is 10.", default=10, required=False)
    parser.add_argument('--output_file_name', help="The name of srt/subtitle file.", default="output", required=False)
    parser.add_argument('--translate', help="Set if tranlation is required.", required=False, action='store_true')
    parser.add_argument('--from_lang', help="Language to translate from.", default="auto", required=False)
    parser.add_argument('--to_lang', help="Language to translate to.", default="en", required=False)
    parser.add_argument('--use_stereo', help="Use all audio channels available.", required=False, action='store_true')
    parser.add_argument('--sample_rate', help="Define new sample rate for the audio.", required=False, default=0)
    args = parser.parse_args()
    
    # for now support only video files
    # generate subtitles directly from a given audio file
    video_path = args.video_path
    audio_path = ""
    transcription_file_path = ""


    if is_youtube_url(args.video_path):
        video_path, audio_only = download_from_youtube(video_url=args.video_path, audio_only=args.download_audio)

    # check if only audio was downloaded from youtube
    if args.download_audio or args.audio_only:
        audio_path = video_path
        sample_rate , nchannels = audio_utils.audio_info(audio_path)
    else:
        audio_path, sample_rate , nchannels = get_audio_from_video.extract_audio_from_video(video_path)

    if not args.use_stereo:
        audio_utils.convert_audio_to_mono(audio_path)
        sample_rate , nchannels = audio_utils.audio_info(audio_path)
    
    if args.sample_rate:
        audio_utils.change_sample_rate(audio_path, new_sample_rate=int(args.sample_rate))
        sample_rate , nchannels = audio_utils.audio_info(audio_path)
        
    transcription_file_path = get_transcription.deepgram_transcription(audio_path, sample_rate , nchannels, delete_audio=False)
    generate_subtitles.gen_subs(transcription_file_path, int(args.sup_size), args.output_file_name, args.translate, args.from_lang, args.to_lang)

    
