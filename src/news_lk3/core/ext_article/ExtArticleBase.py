import time

from googletrans import Translator
from utils import Log

from news_lk3.core.article.Article import Article

log = Log('ExtArticleBase')

COMMON_TRANSLATOR = Translator()


class ExtArticleBase(Article):
    def __init__(
        self,
        # Article attributes
        newspaper_id: str,
        url: str,
        time_ut: int,
        original_lang: str,
        original_title: str,
        original_body_lines: list[str],
        # (new) attributes
        translated_text: dict[str, dict[str, str]],
    ):
        super().__init__(
            newspaper_id=newspaper_id,
            url=url,
            time_ut=time_ut,
            original_lang=original_lang,
            original_title=original_title,
            original_body_lines=original_body_lines,
        )
        self.translated_text = translated_text

    @staticmethod
    def get_translated_text(article: Article):
        idx = {}
        src = article.original_lang

        for dest in ['si', 'ta', 'en']:
            if src == dest:
                continue

            def translate_single(text):
                TIME_SLEEP_S = 1
                try:
                    time.sleep(TIME_SLEEP_S)
                    result = COMMON_TRANSLATOR.translate(
                        text,
                        src=src,
                        dest=dest,
                    )
                    result_text = result.text if result else None
                except Exception as e:
                    log.error(
                        f'Could not translate "{text}" ({src}) to {dest}: "{e}"'
                    )
                    result_text = None

                log.debug(f'{text} -> {result_text}')
                return result_text

            def translate(text) -> str:
                DELIM = '. '
                sentences = text.split(DELIM)
                translated_sentences = []
                for sentence in sentences:
                    translated_sentence = (
                        translate_single(sentence) or sentence
                    )
                    translated_sentences.append(translated_sentence)
                return DELIM.join(translated_sentences)

            translated_title = translate(
                article.original_title,
            )
            translated_body_lines = []
            for line in article.original_body_lines:
                translated_line = translate(
                    line,
                )
                translated_body_lines.append(translated_line)
            idx[dest] = dict(
                title=translated_title,
                body_lines=translated_body_lines,
            )
        return idx

    @property
    def to_dict(self) -> dict:
        return dict(
            translated_text=self.translated_text,
        )

    @property
    def is_en(self):
        return self.original_lang == 'en'

    @property
    def has_en_translation(self):
        return self.translated_text and 'en' in self.translated_text

    @property
    def title_display(self):
        if self.is_en or not self.has_en_translation:
            return self.original_title
        return self.translated_text['en']['title']

    @property
    def body_lines_display(self):
        if self.is_en or not self.has_en_translation:
            return self.original_body_lines
        return self.translated_text['en']['body_lines']
