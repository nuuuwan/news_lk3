import os
from news_lk3.core import Article, ExtArticle
from utils import Log

log = Log('upload_ext_data')

MAX_N_STORED = 10


def main():
    n_stored = 0
    for article in Article.list_from_remote():
        ext_article = ExtArticle.from_article(article)
        if os.path.exists(ext_article.file_name):
            log.debug(f'{ext_article.file_name} exists. Skipping.')
            continue
        ext_article.store()
        n_stored += 1
        if n_stored >= MAX_N_STORED:
            break


if __name__ == '__main__':
    main()
