import soundfile as sf

def audio_info(audio_path):
    data, sr = sf.read(audio_path)
    nchannels = 1
    if data.ndim > 1:
        nchannels = data.shape[-1]

    return sr, nchannels


def convert_audio_to_mono(audio_path):
    data, sr = sf.read(audio_path)
    sf.write(audio_path, data[::,0], sr)



def change_sample_rate(audio_path, new_sample_rate=0):
    data, sr = sf.read(audio_path)
    assert new_sample_rate < sr, f"New sample rate {new_sample_rate} must be less than sample rate {sr} of audio."
    if new_sample_rate == 0:
        new_sample_rate = sr
    factor = int(sr / new_sample_rate)
    sf.write(audio_path, data[::factor], new_sample_rate)