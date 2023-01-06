import scipy
import soundfile


class AudioProcessor:

    @staticmethod
    def save_as_wav(input_file_path, output_file_path):
        sound_data, samplerate = soundfile.read(input_file_path + '.ogg')
        soundfile.write(input_file_path + '.wav', sound_data, samplerate)
        scipy.io.wavfile.read(input_file_path + '.wav')
        scipy.io.wavfile.write(output_file_path, data=sound_data, rate=16000)
