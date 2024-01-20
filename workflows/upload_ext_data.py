import os

from _upload_common import init_dir
from utils import Log, SECONDS_IN
import time
from news_lk3.core import Article, ExtArticle

log = Log('upload_ext_data')

MAX_RUNNING_TIME_S = 1 * SECONDS_IN.MINUTE

def main():
    t_start = time.time()
    init_dir()
    articles = Article.list_from_remote()
    init_dir()
    for article in articles:
        
        d_time = time.time() - t_start
        log.debug(f'{d_time=:.1f}s')
        if d_time > MAX_RUNNING_TIME_S:
            log.info(f'{d_time=:.1f}s > {MAX_RUNNING_TIME_S}s. Stopping.')
            break

            
        ext_article = ExtArticle.from_article(article, force_extend=True)
        if os.path.exists(ext_article.file_name):
            log.debug(f'{ext_article.file_name} exists. Skipping.')
            continue
        ext_article.store()
        
if __name__ == '__main__':
    main()
