import os

from news_lk3._utils import log
from news_lk3.core import Article, ExtArticle


def init_dir():
    for dir in [
        Article.DIR_REPO,
        Article.DIR_REPO_ARTICLES,
        ExtArticle.DIR_REPO_ARTICLES_EXT,
    ]:
        if not os.path.exists(dir):
            os.makedirs(dir)
            log.info(f'Created {dir}.')
        else:
            log.debug(f'{dir} exists. Not creating.')
