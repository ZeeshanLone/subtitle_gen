import argparse
import json
import pysrt

from utils.get_translation import google_translate
import os

def ms_to_time(milliseconds):
  """Converts milliseconds to hh:mm:ss.ms format, handling milliseconds below 1 second."""
  
  # Ensure milliseconds are positive (handles negative values from Deepgram)
  milliseconds = abs(milliseconds) * 1000  # Convert to milliseconds (integer)

  # Separate milliseconds from seconds
  seconds, milliseconds = divmod(int(milliseconds), 1000)

  # Handle cases where milliseconds are less than 1 second
  if seconds == 0:
    return f"00:00:00,{milliseconds:03d}"
  else:
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"


def non_overlapping_sliding_window(input_list, window_size):
    """
    Generate non-overlapping sliding windows of a predefined size over a list.

    Parameters:
    - input_list: The input list to create sliding windows from.
    - window_size: The size of each sliding window.

    Returns:
    A generator yielding each non-overlapping sliding window.
    """
    if window_size <= 0:
        raise ValueError("Window size must be a positive integer.")

    for i in range(0, len(input_list), window_size):
        yield input_list[i:i + window_size]


def merge_text(words_window, translate, from_lang, to_lang):
    words = []
    for word_data in words_window:
        words.append(word_data['punctuated_word'])

    text = ' '.join(words)
    if translate:
        text = google_translate(text, from_lang, to_lang)
    return text


def gen_subs(file_name, sup_size, output_file_name, translate, from_lang, to_lang):
    with open(file_name, 'r', encoding='utf-8') as f:
        transcription_data = f.read()
    try:
        transcription_data = json.loads(transcription_data)
    except Exception as e:
        print("Error in json file")

    words = transcription_data['results']['channels'][0]['alternatives'][0]['words']

    subs = pysrt.SubRipFile()
    for word_window in non_overlapping_sliding_window(words, int(sup_size)):
        start_time = ms_to_time(word_window[0]['start'])
        end_time  = ms_to_time(word_window[-1]['end'])
        sub_text = merge_text(word_window, translate, from_lang, to_lang)
        subs.append(pysrt.SubRipItem(start=start_time, end=end_time, text=sub_text))

    output_dir = os.path.join(os.getcwd(), 'output')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_file = os.path.join(output_dir, f"{output_file_name}.srt")
    subs.save(output_file, encoding='utf-8')
    print(f"Subtitles ready At......\n{output_file}")



if __name__=="__main__":

    # process arguments "transcriptionfilename" 
    # open transcription file
    parser = argparse.ArgumentParser() 
    parser.add_argument('--file_name', help="transcription file name should be json file.")
    parser.add_argument('--sup_size', help="Number of words to display at one time. Default is 20.", default=10, required=False)
    parser.add_argument('--output_file_name', help="The name of srt/subtitle file.\n Dont write .srt in file name it will be created automatically.", default="output", required=False)
    args = parser.parse_args()
    gen_subs(args.file_name, args.sup_size, args.output_file_name, translate=False)
