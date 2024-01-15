import os
import random

from news_lk3._utils import log
from news_lk3.core.Article import Article
from news_lk3.custom_newspapers import newspaper_class_list

DELIM_MD = '\n' * 2
MAX_ARTICLES_TO_UPLOAD = 80


def init():
    os.system(f'rm -rf {Article.DIR_REPO}')
    os.system(f'mkdir {Article.DIR_REPO}')

    os.system(f'rm -rf {Article.DIR_REPO_ARTICLES}')
    os.system(f'mkdir {Article.DIR_REPO_ARTICLES}')


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
            if n_total > 2:
                break

        if n_total > MAX_ARTICLES_TO_UPLOAD:
            break

    log.info(f'Scraped {n_total} articles in total.')
