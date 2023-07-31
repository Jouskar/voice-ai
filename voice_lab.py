from elevenlabs import clone, generate, play, set_api_key
import speech_recognition as sr
import sounddevice as sd
from scipy.io.wavfile import write
import time


class SpeechRecognizer:
    def __init__(self):
        self.r = sr.Recognizer()

    def speech_to_text(self):
        with sr.Microphone() as source2:
            self.r.adjust_for_ambient_noise(source2, duration=0.2)
            audio2 = self.r.listen(source2)
        try:
            text = self.r.recognize_google(audio2, language="tr-TR")
            return text.lower()

        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

        except sr.UnknownValueError:
            print("unknown error occurred")


class Recorder:
    def __init__(self, duration=55, samplerate=44100, channels=1):
        self.duration = duration
        self.fs = samplerate
        self.channels = channels
        self.end_record = False
        self.recording = None
        self.left_time = None
        self.samples = []
        self.deleted_samples = []

        sd.default.samplerate = samplerate
        sd.default.channels = channels

    def record(self):
        self.end_record = False
        self.recording = sd.rec(int(self.fs * self.duration))

        t = self.duration

        while t and not self.end_record:
            mins, secs = divmod(t, 60)
            self.left_time = '{:02d}:{:02d}'.format(mins, secs)
            time.sleep(1)
            t -= 1

        sd.stop()
        print(self.recording)
        self.left_time = None
        self.save_recording()

    def stop_recording(self):
        sd.stop()
        self.left_time = None
        self.end_record = True

    def save_recording(self):
        name: str
        if self.deleted_samples:
            name = f"recording{self.deleted_samples.pop(0)}.wav"
        else:
            name = f"recording{self.samples.__len__()}.wav"
        write(name, self.fs, self.recording)
        self.samples.append(name)

    def delete_sample(self, index: int):
        self.deleted_samples.append(self.samples.pop(index))

    def add_sample(self, sample: str):
        self.samples.append(sample)


recorder = Recorder()


class VoiceLab:
    __API_KEY = "941962e3f12d41d7c4ac09294dc20b35"
    __headers = {
        "Accept": "application/json",
        "xi-api-key": __API_KEY
    }
    __samples: [str] = []
    __voice_sample = None

    def __init__(self):
        self.__headers = {
            "Accept": "application/json",
            "xi-api-key": self.__API_KEY
        }

        self.recorder = recorder
        self.voice = "Arnold"
        self.cloned_voice = None
        self.model = "eleven_multilingual_v1"

        set_api_key(self.__API_KEY)

    def clone_voice(self):
        self.cloned_voice = \
            clone(
                name="Users Voice",
                description="Cloned voice of the user",
                files=self.recorder.samples,
            )

        self.voice = self.cloned_voice

    def generate_audio(self, text: str):
        print(self.voice)
        audio = generate(text=text, voice=self.voice, model=self.model)
        play(audio)


voice_lab = VoiceLab()
speech_recognizer = SpeechRecognizer()
