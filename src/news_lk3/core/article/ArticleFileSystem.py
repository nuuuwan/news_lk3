import os
import tempfile
from functools import cache

from utils import Directory, Git, JSONFile, Log, hashx

log = Log('ArticleLoader')


class ArticleFileSystem:
    DIR_REPO = os.path.join(tempfile.gettempdir(), 'news_lk3_data')
    DIR_REPO_ARTICLES = os.path.join(DIR_REPO, 'articles')
    HASH_SALT = '123019839120398'
    HASH_LENGTH = 8

    @staticmethod
    def get_hash(url):
        return hashx.md5(url + ArticleFileSystem.HASH_SALT)[
            : ArticleFileSystem.HASH_LENGTH
        ]

    @staticmethod
    def get_article_file_only(url):
        h = ArticleFileSystem.get_hash(url)
        return f'{h}.json'

    @staticmethod
    def get_article_file(url):
        file_name_only = ArticleFileSystem.get_article_file_only(url)
        return os.path.join(
            ArticleFileSystem.DIR_REPO_ARTICLES, file_name_only
        )

    @staticmethod
    def load_d_from_file(article_file):
        return JSONFile(article_file).read()

    @classmethod
    def load_from_file(cls, article_file):
        d = cls.load_d_from_file(article_file)
        return cls.from_dict(d)

    @property
    def file_name(self):
        return ArticleFileSystem.get_article_file(self.url)

    def store(self):
        JSONFile(self.file_name).write(self.to_dict)
        log.info(f'Stored {self.file_name}.')

    @classmethod
    @cache
    def list_from_remote(cls) -> list:
        git = Git('https://github.com/nuuuwan/news_lk3_data.git')
        git.clone(cls.DIR_REPO, force=False)
        git.checkout('main')

        articles = []
        for child in Directory(cls.DIR_REPO_ARTICLES).children:
            if isinstance(child, Directory) or child.ext != 'json':
                continue
            article = cls.load_from_file(child.path)
            articles.append(article)
        n_articles = len(articles)
        log.debug(f'Loaded {n_articles} articles')
        return articles
