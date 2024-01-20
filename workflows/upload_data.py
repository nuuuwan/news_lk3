import os
import random
import time
from utils import SECONDS_IN
from news_lk3._utils import log
from news_lk3.core import Article
from news_lk3.custom_newspapers import newspaper_class_list

TEST_MODE = os.name == 'nt'
log.debug(f'{TEST_MODE=}')
MAX_RUNNING_TIME_M = 0.1 if TEST_MODE else 10
MAX_RUNNING_TIME_S = MAX_RUNNING_TIME_M * SECONDS_IN.MINUTE
log.debug(f'{MAX_RUNNING_TIME_S=}')


def init_dirs():
    for dir in [Article.DIR_REPO, Article.DIR_REPO_ARTICLES]:
        if not os.path.exists(dir):
            os.makedirs(dir)
            log.debug(f'Created directory {dir}')


def main():
    t_start = time.time()
    init_dirs()

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
        log.debug(f'{n_total=}')
        delta_t = time.time() - t_start
        log.debug(f'{delta_t=:.1f}s')
        if delta_t > MAX_RUNNING_TIME_S:
            log.info(
                f'{delta_t=:.1f}s > {MAX_RUNNING_TIME_S}s. Stopping.')
            break

    log.info(f'Scraped {n_total} articles in total.')


if __name__ == '__main__':
    main()
