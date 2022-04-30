from spleeter.audio.adapter import AudioAdapter
from python_osu_parser import curve

audio_loader = AudioAdapter.default()
sample_rate = 44100
file = '../data/chitose.mp3'
waveform, _ = audio_loader.load(file, sample_rate=sample_rate)