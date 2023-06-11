import numpy as np
import soundfile as sf
import noisereduce as nr
from scipy.io import wavfile
from pydub import AudioSegment
import ffmpy
import wave


class Audio_Setup:
    def __init__(self,audio_filepath:str):
        self.audio_filepath = audio_filepath
        
    def denoise(self,start_time:float,stop_time:float,):
        data,srate = sf.read(self.audio_filepath)
        time_delta = stop_time - start_time
        if time_delta > 0.30:
            start_time = start_time + (time_delta*0.20)
            stop_time = stop_time - (time_delta*0.20)
        beginning_of_noise = int(np.round(start_time*srate))
        end_of_noise = int(np.round(stop_time*srate))
        noise_sample = data[beginning_of_noise:end_of_noise]
        reduced_noise = nr.reduce_noise(y =data, sr=srate, y_noise = noise_sample, n_std_thresh_stationary=1.5,stationary=True)
        write(self.audio_filepath,srate,reduced_noise)
        return reduced_noise
    
    def check_nchannels(self)-> None:
        w = wave.open(self.audio_filepath, 'r')
        nchannels = w.getnchannels()
        if nchannels != 1:
            fs, data = wavfile.read("test_convo_two.wav") 
            channel_one = audio_filepath.split('.wav')[0] + 'channel_1.wav'
            channel_two = audio_filepath.split('.wav')[0] + 'channel_2.wav'
            wavfile.write(channel_one, fs, data[:, 0])   # saving first column which corresponds to channel 1
            wavfile.write(channel_two, fs, data[:, 1])
        else:
            print('Already single channel.')
    
    def check_srate(self)-> bool:
        w = wave.open(self.audio_filepath, 'r')
        rate = w.getframerate()
        if rate != 16000:
            sound = pyd.AudioSegment.from_file(self.audio_filepath)
            sound = sound.set_frame_rate(16000)
            sound.export(self.audio_filepath, format="wav")
            return False
        else:
            return True
    
    def transcode_to_wav(self):
        suffix = self.audio_filepath[-3:]
        if suffix in ['mp3','ogg','m4a']:
            transcode = ffmy.FFmpeg(inputs={self.audio_filepath:None},\
                        outputs={self.audio_filepath[-3:]+'.wav': None})
            transcode.run()
            
    def wav_to_flac(self):
        data = AudioSegment.from_wav(self.audio_filepath)
        flac_file_path = self.audio_filepath.split(".wav")[0] + ".flac"
        data.export(flac_file_path,format="flac")
