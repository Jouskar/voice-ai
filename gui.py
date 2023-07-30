from voice_translator import voice_translator
from voice_lab import voice_lab, recorder, speech_recognizer
import customtkinter
import threading
from time import sleep


class TkButton:
    def __init__(self, root, label: str, function):
        self.button = customtkinter.CTkButton(master=root, text=label, command=function)

    def pack(self, pad_x, pad_y):
        self.button.pack(padx=pad_x, pady=pad_y)


class TkLabel:
    def __init__(self, root):
        self.__string_var = customtkinter.StringVar()
        self.header_label = customtkinter.CTkLabel(master=root, textvariable=self.__string_var, font=(None, 24),
                                                   width=10)
        self.header_label.pack(padx=20, pady=20)

    def set_text(self, text: str):
        self.__string_var.set(text)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Voice AI")
        self.geometry("400x400")

        self.header_label = TkLabel(self)

        self.voice_record_btn = TkButton(self, "Voice Record", self.record_voice)
        self.voice_record_btn.pack(20, 20)

        self.stop_record_btn = TkButton(self, "Stop Record", recorder.stop_recording)
        self.stop_record_btn.pack(20, 1)

        self.clone_voice_btn = TkButton(self, "Clone Voice", voice_lab.clone_voice)
        self.clone_voice_btn.pack(20, 1)

        self.translate_btn = TkButton(self, "Translate", self.engage_translate)
        self.translate_btn.pack(20, 1)

        self.recording_name = customtkinter.CTkEntry(master=self, placeholder_text="Recording name...", width=200)
        self.recording_name.pack(padx=20, pady=1)

        self.recording_add_btn = TkButton(self, "Add recording", self.add_recording)
        self.recording_add_btn.pack(20, 1)

        self.language_list = customtkinter.CTkComboBox(master=self, values=voice_translator.language_names, width=200)
        self.language_list.pack(padx=20, pady=20)
        self.language_list.set('Choose language')

    def record_voice(self):
        x = threading.Thread(target=recorder.record)
        x.start()

        while not recorder.end_record:
            sleep(1)
            print("hehe")
            self.header_label.set_text(recorder.left_time)
            self.update()

        x.join()

    def engage_translate(self):
        voice_translator.set_dest(self.language_list.get())
        speech_text = speech_recognizer.speech_to_text()
        voice_translator.audio_translate(speech_text)

    def add_recording(self):
        record_name = self.recording_name.get()
        recorder.add_sample(record_name)
        self.recording_name.delete(0, record_name.__len__())


app = App()
app.mainloop()
