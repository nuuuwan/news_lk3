from googletrans import Translator
from utils import Log
import time
from news_lk3.core.article.Article import Article

log = Log('ExtArticleBase')


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
        translator = Translator()
        idx = {}
        for target_lang in ['si', 'ta', 'en']:
            if article.original_lang == target_lang:
                continue

            def translate(text):
                try:
                    time.sleep(1)
                    result = translator.translate(
                        text,
                        src=article.original_lang,
                        dest=target_lang,
                    )
                    result_text = result.text if result else None
                except Exception as e:
                    log.debug(f'{text} -> {e}')
                    result_text = None

                log.debug(f'{text} -> {result_text}')
                return result_text

         
            translated_title = translate(
                article.original_title,
            )
            translated_body_lines = []
            for line in article.original_body_lines:
                translated_line = translate(
                    line,
                )
                translated_body_lines.append(translated_line)
            idx[target_lang] = dict(
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
