from pyannote.audio import Pipeline
pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization")


class Speaker_Diarize:
    def __init__(self,audio_filepath):
        self.audio_filepath = audio_filepath
        
    def create_diarize_(self):
        diarization_dict = {'Speaker':[],'Start':[],'Stop':[]}
        diarization = pipeline(self.audio_filepath)
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            diarization_dict['Speaker'].append(speaker)
            diarization_dict['Start'].append(turn.start - 0.05)
            diarization_dict['Stop'].append(turn.end + 0.05)
        return diarization_dict

    def refactor_transcription(transcription_dict:dict)-> dict:  
        diarization_dict_refactor = {'Speaker':[],'Start':[],'Stop':[],'Transcription':[]}
        for i in range(0,len(transcription_dict['Speaker'])):
            if i == 0:
                diarization_dict_refactor['Speaker'].append(transcription_dict['Speaker'][i])
                diarization_dict_refactor['Start'].append(transcription_dict['Start'][i])
                diarization_dict_refactor['Transcription'].append(transcription_dict['Transcription'][i][0])
            else:
                if transcription_dict['Speaker'][i-1] != transcription_dict['Speaker'][i]:
                    diarization_dict_refactor['Start'].append(transcription_dict['Start'][i])
                    diarization_dict_refactor['Stop'].append(transcription_dict['Stop'][i-1])
                    diarization_dict_refactor['Speaker'].append(transcription_dict['Speaker'][i])
                    diarization_dict_refactor['Transcription'][-1] = self.punctuate(diarization_dict_refactor['Transcription'][-1])
                    diarization_dict_refactor['Transcription'].append(transcription_dict['Transcription'][i][0])
                else:
                    added_utterance = diarization_dict_refactor['Transcription'][-1] + ' ' + transcription_dict['Transcription'][i][0]
                    #print(added_utterance)
                    diarization_dict_refactor['Transcription'][-1] = added_utterance
        diarization_dict_refactor['Stop'].append(transcription_dict['Stop'][-1])
        return diarization_dict_refactor