from spleeter.audio.adapter import AudioAdapter
from spleeter.separator import Separator

def separate_audio(file, layers=5, sample_rate=44100):
    audio_loader = AudioAdapter.default()
    if layers not in [2, 4, 5]:
        raise Exception("layers must be 2, 4 or 5!")
    
    waveform, _ = audio_loader.load(file, sample_rate=sample_rate)
    separator = Separator('spleeter:{}stems'.format(layers))
    
    prediction = separator.separate(waveform)
    
    return prediction
    

if __name__ == "__main__":
    audio_loader = AudioAdapter.default()
    prediction = separate_audio("../../data/chitose.mp3", 4)
    for k, v in prediction.items():
        audio_loader.save("../../data/output/{}.mp3".format(k), v, 44100)
