from moviepy.editor import VideoFileClip
import argparse
import tempfile
import os


def extract_audio_from_video(video_file):
    audio_path = os.path.join(os.getcwd(), 'audio')
    audio_file = VideoFileClip(video_file).audio

    if not os.path.exists(audio_path):
        os.makedirs(audio_path)
        print(f"Directory Created {audio_path}....")

    # file_name = tempfile.NamedTemporaryFile(dir=audio_path, delete=True)
    # file_name = file_name.name+'.wav'
    file_name = os.path.split(video_file)[-1].split('.')[0]
    file_name = os.path.join(audio_path, file_name + '.wav')
    audio_file.write_audiofile(file_name)

    return file_name, audio_file.fps, audio_file.nchannels



if __name__=="__main__":
    parser = argparse.ArgumentParser() 
    parser.add_argument('--video_path', help="Path to video file.", required=True)
    parser.add_argument('--sup_size', help="Number of words to display at one time. Default is 20.", default=20, required=False)
    parser.add_argument('--output_file_name', help="The name of srt/subtitle file.\n Dont write .srt in file name it will be created automatically.", default="output", required=False)
    args = parser.parse_args()

    print(extract_audio_from_video(args.video_path))