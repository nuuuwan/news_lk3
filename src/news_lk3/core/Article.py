import os
import tempfile

from utils import TIME_FORMAT_TIME, JSONFile, Time, hashx

from news_lk3._utils import log


class Article:
    DIR_REPO = os.path.join(tempfile.gettempdir(), 'news_lk3_data')
    DIR_REPO_ARTICLES = os.path.join(DIR_REPO, 'articles')
    HASH_SALT = '123019839120398'
    HASH_LENGTH = 8
    DEFAULT_ORIGINAL_LANG = 'en'

    def __init__(
        self,
        newspaper_id,
        url,
        time_ut,
        original_lang,
        original_title,
        original_body_lines,
    ):
        self.newspaper_id = newspaper_id
        self.url = url
        self.time_ut = time_ut
        self.original_lang = original_lang
        self.original_title = original_title
        self.original_body_lines = original_body_lines

    @staticmethod
    def get_hash(url):
        return hashx.md5(url + Article.HASH_SALT)[: Article.HASH_LENGTH]

    @staticmethod
    def get_article_file_only(url):
        h = Article.get_hash(url)
        return f'{h}.json'

    @staticmethod
    def get_article_file(url):
        file_name_only = Article.get_article_file_only(url)
        return os.path.join(Article.DIR_REPO_ARTICLES, file_name_only)

    @staticmethod
    def load_d_from_file(article_file):
        return JSONFile(article_file).read()

    @staticmethod
    def load_from_file(article_file):
        d = Article.load_d_from_file(article_file)
        return Article.from_dict(d)

    @staticmethod
    def from_dict(d):
        return Article(
            newspaper_id=d['newspaper_id'],
            url=d['url'],
            time_ut=d['time_ut'],
            original_lang=d.get('original_lang'),
            original_title=d.get('original_title'),
            original_body_lines=d.get('original_body_lines'),
        )

    @property
    def to_dict(self):
        return dict(
            newspaper_id=self.newspaper_id,
            url=self.url,
            time_ut=self.time_ut,
            original_lang=self.original_lang,
            original_title=self.original_title,
            original_body_lines=self.original_body_lines,
        )

    def store(self):
        JSONFile(self.file_name).write(self.to_dict)
        log.debug(f'Wrote {self.file_name}')

    @property
    def file_name(self):
        return Article.get_article_file(self.url)

    def __lt__(self, other):
        return self.time_ut < other.time_ut

    def __str__(self):
        return '\n'.join(
            [
                self.newspaper_id,
                self.url,
                TIME_FORMAT_TIME.stringify(Time(self.time_ut)),
                self.original_lang,
                self.original_title,
                '\n'.join(
                    self.original_body_lines,
                ),
            ]
        )
