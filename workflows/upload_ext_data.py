import os

from utils import Log

from news_lk3.core import Article, ExtArticle
from _upload_common import init_dir
log = Log('upload_ext_data')

MAX_N_STORED = 10


def main():
    init_dir()
    n_stored = 0
    articles = Article.list_from_remote()
    init_dir()
    for article in articles:
        ext_article = ExtArticle.from_article(article, force_extend=True)
        if os.path.exists(ext_article.file_name):
            log.debug(f'{ext_article.file_name} exists. Skipping.')
            continue
        ext_article.store()
        n_stored += 1
        if n_stored >= MAX_N_STORED:
            break


if __name__ == '__main__':
    main()
