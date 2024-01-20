import os

from utils import JSONFile, Log

from news_lk3.core.article.Article import Article

log = Log('ExtArticleFileSystem')


class ExtArticleFileSystem:
    DIR_REPO_ARTICLES_EXT = os.path.join(Article.DIR_REPO, 'articles_ext')

    @staticmethod
    def get_extended_data(article: Article):
        file_name = Article.get_article_file(article.url)
        if not os.path.exists(file_name):
            return {}
        return JSONFile(file_name).read()

    @classmethod
    def from_article(cls, article: Article, force_extend: bool):
        extended_data = ExtArticleFileSystem.get_extended_data(article)
        translated_text = extended_data.get(
            'translated_text',
            None,
        )
        if force_extend:
            if not translated_text:
                translated_text = cls.get_translated_text(article)

        return cls(
            newspaper_id=article.newspaper_id,
            url=article.url,
            time_ut=article.time_ut,
            original_lang=article.original_lang,
            original_title=article.original_title,
            original_body_lines=article.original_body_lines,
            translated_text=translated_text,
        )

    @staticmethod
    def get_article_file_only(url):
        h = Article.get_hash(url)
        return f'{h}.ext.json'

    @staticmethod
    def get_article_file(url):
        file_name_only = ExtArticleFileSystem.get_article_file_only(url)
        return os.path.join(
            ExtArticleFileSystem.DIR_REPO_ARTICLES_EXT, file_name_only
        )

    @property
    def file_name(self):
        return ExtArticleFileSystem.get_article_file(self.url)

    def store(self):
        JSONFile(self.file_name).write(self.to_dict)
        log.info(f'Stored {self.file_name}.')
