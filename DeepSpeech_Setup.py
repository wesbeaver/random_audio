import deepspeech
import wave
import numpy as np
import pandas as pd
from fastpunct import FastPunct
import os
from scipy.io.wavfile import write





class DeepSpeech_Setup:
    def __init__(self,model_file_path:str,scorer_file_path:str):
        self.model_file_path = model_file_path
        self.scorer_file_path = scorer_file_path
        
    def create_model(self)-> deepspeech.Model:
        model = deepspeech.Model(self.model_file_path)
        model.enableExternalScorer(self.scorer_file_path)
        lm_alpha = 0.75
        lm_beta = 1.85
        model.setScorerAlphaBeta(lm_alpha, lm_beta)
        beam_width = 500
        model.setBeamWidth(beam_width)
        return model
    
    def execute_model(self,model,audio_filepath:str,is_data=False)-> str:
        self.check_srate(audio_filepath)
        w = wave.open(filename, 'r')
        frames = w.getnframes()
        buffer = w.readframes(frames)
        data16 = np.frombuffer(buffer,dtype=np.int16)
        text = model.stt(data16)
        return text
    
    def create_audio_snippet(self,start:float,stop:float,audio_filepath:str)->int:
        with wave.open(audio_filepath, "rb") as w:
            nchannels = w.getnchannels()
            sampwidth = w.getsampwidth()
            framerate = w.getframerate()
            # set position in wave to start of segment
            w.setpos(int(start * framerate))
            # extract data
            buffer = w.readframes(int((stop - start) * framerate))
            data = np.frombuffer(buffer,dtype=np.int16)
            return data
        
    def transcribe(self,model,data:list)->str:
        text = model.stt(data)
        return text
    
    def punctuate(self,text:str)-> str:
        fp = FastPunct()
        punctuated_text = fp.punct([text], correct=True)
        return punctuated_text
           
    def transcribe_diarized(self,model,diarize_dict:dict,audio_filepath:str)-> dict:
        self.check_srate(audio_filepath)
        diarize_dict['Transcription'] = []
        for i in range(0,len(diarize_dict['Start'])):
            start = diarize_dict['Start'][i]
            stop = diarize_dict['Stop'][i]
            data = self.create_audio_snippet(start,stop,audio_filepath)
            text = self.transcribe(model,data)
            #punctuated_text = self.punctuate(text)
            diarize_dict['Transcription'].append(punctuated_text)
        return diarize_dict
    
    def extract_pos(transcription_dict:dict) -> dict:
        pos_dict = {i:{}for i in set(transcription_dict['Speaker'])}
        for i in range(0,len(transcription_dict['Speaker'])):
            #print(transcription_dict['Transcription'][i][0])
            text = nltk.word_tokenize(transcription_dict['Transcription'][i][0])
            pos_list = nltk.pos_tag(text)
            #print(transcription_dict['Transcription'][i][0])
            #print('-----')
            for j in pos_list:
                if j[1] not in pos_dict[transcription_dict['Speaker'][i]].keys():
                    pos_dict[transcription_dict['Speaker'][i]][j[1]] = []
                    pos_dict[transcription_dict['Speaker'][i]][j[1]].append(j[0])
                else:
                    pos_dict[transcription_dict['Speaker'][i]][j[1]].append(j[0])
        return pos_dict
            
            