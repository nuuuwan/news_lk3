import os

from googletrans import Translator
from utils import JSONFile, Log

from news_lk3.core.article.Article import Article

log = Log('ExtArticle')


class ExtArticle(Article):
    DIR_REPO_ARTICLES_EXT = os.path.join(Article.DIR_REPO, 'articles_ext')

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

            def translate(text):
                result = translator.translate(
                    text,
                    src=article.original_lang,
                    dest=target_lang,
                )
                result_text = result.text if result else None
                log.debug(f'{text} -> {result_text}')
                return result_text

            if article.original_lang == target_lang:
                continue
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

    @staticmethod
    def from_article(article: Article):
        return ExtArticle(
            newspaper_id=article.newspaper_id,
            url=article.url,
            time_ut=article.time_ut,
            original_lang=article.original_lang,
            original_title=article.original_title,
            original_body_lines=article.original_body_lines,
            translated_text=ExtArticle.get_translated_text(article),
        )

    @property
    def to_dict(self) -> dict:
        return dict(
            translated_text=self.translated_text,
        )

    @staticmethod
    def get_article_file_only(url):
        h = Article.get_hash(url)
        return f'{h}.ext.json'

    @staticmethod
    def get_article_file(url):
        file_name_only = ExtArticle.get_article_file_only(url)
        return os.path.join(ExtArticle.DIR_REPO_ARTICLES_EXT, file_name_only)

    @property
    def file_name(self):
        return ExtArticle.get_article_file(self.url)

    def store(self):
        JSONFile(self.file_name).write(self.to_dict)
        log.info(f'Stored {self.file_name}.')
