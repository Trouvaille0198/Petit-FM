from pygtrans import Translate
from config import logger
import time


class Translator:
    def __init__(self):
        self.translator = Translate()

    def translate(self, text: str, target_lang: str = 'zh-CN') -> (str, bool):
        try:
            result = self.translator.translate(text, target=target_lang).translatedText
        except ConnectionError:
            logger.warning('翻译次数过多！')
            time.sleep(50)
            return text, False
        return result, True

    def detect(self, text: str):
        return self.translator.detect(text).language
