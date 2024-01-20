import os
import tempfile

from utils import JSONFile, Log, hashx

log = Log('ArticleLoader')


class ArticleLoader:
    DIR_REPO = os.path.join(tempfile.gettempdir(), 'news_lk3_data')
    DIR_REPO_ARTICLES = os.path.join(DIR_REPO, 'articles')
    HASH_SALT = '123019839120398'
    HASH_LENGTH = 8

    @staticmethod
    def get_hash(url):
        return hashx.md5(url + ArticleLoader.HASH_SALT)[
            : ArticleLoader.HASH_LENGTH
        ]

    @staticmethod
    def get_article_file_only(url):
        h = ArticleLoader.get_hash(url)
        return f'{h}.json'

    @staticmethod
    def get_article_file(url):
        file_name_only = ArticleLoader.get_article_file_only(url)
        return os.path.join(ArticleLoader.DIR_REPO_ARTICLES, file_name_only)

    @staticmethod
    def load_d_from_file(article_file):
        return JSONFile(article_file).read()

    @classmethod
    def load_from_file(cls, article_file):
        d = cls.load_d_from_file(article_file)
        return cls.from_dict(d)

    @property
    def file_name(self):
        return ArticleLoader.get_article_file(self.url)

    def store(self):
        JSONFile(self.file_name).write(self.to_dict)
        log.info(f'Stored {self.file_name}.')
