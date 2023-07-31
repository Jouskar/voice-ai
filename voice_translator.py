from google.cloud import translate_v2 as translate
from voice_lab import voice_lab
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = \
    ("ya29.a0AbVbY6MIlTp0Bres8giDy0rFv9hVhwTsfGejnQdVdcLUGa4_ggPGv3hEXO83PPGJ"
        "bhjsv2DC0MWGjkVEQ2BFFSbn85JQizISiHe_XTTf-RuBSCZ79-oSLMX3bWpHFMAccnOkp77"
        "wowiGl7R9p1Qq3oSp6Oaa0GVTwAvhvwaCgYKAaMSARISFQFWKvPlpV1ZdBSpGOEhGkbNLVLgOw0173")


class VoiceTranslator(translate.Client):
    def __init__(self):
        super().__init__()
        self.__dest = 'en'
        self.available_languages = translate.Client().get_languages()
        self.language_names = [language["name"] for language in self.available_languages]
        self.languages = [language["language"] for language in self.available_languages]

    def audio_translate(self, text):
        print(text, self.__dest)
        translated = self.translate(text, target_language="en")
        voice_lab.generate_audio(translated["translatedText"])

    def set_dest(self, dest):
        self.__dest = dest


voice_translator = VoiceTranslator()
