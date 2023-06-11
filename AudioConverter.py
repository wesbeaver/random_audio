from pydub import AudioSegment


class AudioConvert:

    def __init__(self, audio_file):
        self.audio_file = audio_file
        self.audio = AudioSegment.from_file(audio_file)

    def convertmp3ToWav(self, output_file):
        audio = self.audio.set_frame_rate(44100)
        audio = audio.set_channels(2)
        audio = self.audio.set_sample_width(2)

        # Export the audio to WAV
        audio.export(output_file, format='wav')
