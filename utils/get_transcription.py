import argparse
import os
from dotenv import load_dotenv
import requests
import json
from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    PrerecordedOptions,
    FileSource,
    ReadStreamSource
)
import asyncio
import logging

load_dotenv()
API_KEY = os.getenv("DG_API_KEY")
PARAMS = {'model':'nova-2','punctuate': True,'detect_language':True}

# async def deepgram_transcription(video_file, delete_audio):
#     audio_file, sr, nchannels = get_audio_from_video.extract_audio_from_video(video_file)
    
#     try:
#         # STEP 1 Create a Deepgram client using the API key in the environment variables
#         config = DeepgramClientOptions(
#             verbose=logging.SPAM,
#         )
#         deepgram = DeepgramClient("a9c63a2fc96d02c04290df1782e8987af77a172f", config)
#         # OR use defaults
#         # deepgram = DeepgramClient()

#         # STEP 2 Call the transcribe_file method on the prerecorded class
#         stream = open(audio_file, "rb")

#         payload: ReadStreamSource = {
#             "stream": stream,
#         }

#         options = PrerecordedOptions(
#             model="nova-2",
#             punctuate=True,
#             detect_language=True
#         )

#         response = deepgram.listen.prerecorded.v("1").transcribe_file(payload, options)
#         # print(response.to_json(indent=4))
#         stream.close()
#         json_data = response.to_json(indent=4)
        
#         with open("op.json", 'w', encoding='utf-8') as f:
#             f.write(json_data)
#         print("done")

#     except Exception as e:
#         print(e)

#     if delete_audio:
#         os.remove(audio_file)


def deepgram_transcription(audio_file, sr, nchannels, delete_audio):

    temp_dir = os.path.join(os.getcwd(), 'temp')
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    
    try:
        # STEP 1 Create a Deepgram client using the API key in the environment variables
        config = DeepgramClientOptions(
            verbose=logging.SPAM,
        )
        deepgram = DeepgramClient(API_KEY, config)
        # OR use defaults
        # deepgram = DeepgramClient()

        # STEP 2 Call the transcribe_file method on the prerecorded class
        stream = open(audio_file, "rb")

        payload: ReadStreamSource = {
            "stream": stream,
        }

        options = PrerecordedOptions(
            model="nova-2",
            punctuate=True,
            detect_language=True,
            sample_rate=sr,
            channels=nchannels
        )

        response = deepgram.listen.prerecorded.v("1").transcribe_file(payload, options)
        # print(response.to_json(indent=4))
        stream.close()
        json_data = response.to_json(indent=4)

        transcription_file_path = os.path.join(temp_dir,f"{os.path.split(audio_file)[-1].split('.')[0]}.json")
        with open(transcription_file_path, 'w', encoding='utf-8') as f:
            f.write(json_data)
        print("Completed Transcription........")

    except Exception as e:
        print(e)

    if delete_audio:
        os.remove(audio_file)

    return transcription_file_path



if __name__=="__main__":
    parser = argparse.ArgumentParser() 
    parser.add_argument('--video_path', help="Path to video file.", required=True)
    parser.add_argument('--sup_size', help="Number of words to display at one time. Default is 20.", default=20, required=False)
    parser.add_argument('--output_file_name', help="The name of srt/subtitle file.\n Dont write .srt in file name it will be created automatically.", default="output", required=False)
    parser.add_argument('--delete_audio', help="Delete audio file after job is done.", default=True, required=False)
    args = parser.parse_args()
    # asyncio.run(deepgram_transcription(args.video_path, args.delete_audio))