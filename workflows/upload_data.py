import os
import random

from news_lk3._utils import log
from news_lk3.core import Article, ExtArticle
from news_lk3.custom_newspapers import newspaper_class_list

MAX_ARTICLES_TO_UPLOAD = 80


def init():
    for dir in [Article.DIR_REPO, Article.DIR_REPO_ARTICLES,
                ExtArticle.DIR_REPO_ARTICLES_EXT]:
        if not os.path.exists(dir):
            os.makedirs(dir)
            log.info(f'Created {dir}.')
        else:
            log.debug(f'{dir} exists. Not creating.')


def main(is_test_mode=False):
    init()

    random.shuffle(newspaper_class_list)
    n = len(newspaper_class_list)
    n_total = 0
    for i, newspaper_class in enumerate(newspaper_class_list):
        newspaper_name = newspaper_class.__name__
        log.info(f'{i + 1}/{n}) Scraping {newspaper_name}...')
        article_list = newspaper_class.scrape()
        n_paper = len(article_list)
        log.info(
            f'{i + 1}/{n}) Scraped {n_paper} articles from {newspaper_name}'
        )

        n_total += n_paper

        if is_test_mode:
            if n_total > 0:
                break

        if n_total > MAX_ARTICLES_TO_UPLOAD:
            break

    log.info(f'Scraped {n_total} articles in total.')


if __name__ == '__main__':
    TEST_MODE = os.name == 'nt'
    log.debug(f'{TEST_MODE=}')
    main(TEST_MODE)
