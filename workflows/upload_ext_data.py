import os
import time

from utils import SECONDS_IN, Log

from news_lk3.core import Article, ExtArticle

log = Log('upload_ext_data')

TEST_MODE = os.name == 'nt'
log.debug(f'{TEST_MODE=}')
MAX_RUNNING_TIME_M = 0.1 if TEST_MODE else 10
MAX_RUNNING_TIME_S = MAX_RUNNING_TIME_M * SECONDS_IN.MINUTE
log.debug(f'{MAX_RUNNING_TIME_S=}')


def main():
    t_start = time.time()
    articles = Article.list_from_remote()

    for article in articles:
        d_time = time.time() - t_start
        log.debug(f'{d_time=:.1f}s')
        if d_time > MAX_RUNNING_TIME_S:
            log.info(f'{d_time=:.1f}s > {MAX_RUNNING_TIME_S}s. Stopping.')
            break

        ext_article = ExtArticle.from_article(article, force_extend=True)
        if os.path.exists(ext_article.relative_ext_article_file_path):
            log.debug(
                f'{ext_article.relative_ext_article_file_path} exists. Skipping.')
            continue
        ext_article.store()


if __name__ == '__main__':
    main()
