import os

from utils import Log

from news_lk3.core import Article, ExtArticle

log = Log('upload_ext_data')

MAX_N_STORED = 10


def init():
    for dir in [ExtArticle.DIR_REPO_ARTICLES_EXT]:
        if not os.path.exists(dir):
            os.makedirs(dir)
            log.info(f'Created {dir}.')
        else:
            log.debug(f'{dir} exists. Not creating.')


def main():
    n_stored = 0
    for article in Article.list_from_remote():
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
