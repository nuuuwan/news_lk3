from news_lk3._utils import log
from news_lk3.core import Article
from news_lk3.core.filesys import git_checkout
from news_lk3.core.readme import build_readme_summary
from news_lk3.core.upload_data import upload_data


def main(is_test_mode=False):
    log.debug(f'{is_test_mode=}')
    git_checkout(force=True)
    upload_data(is_test_mode)

    articles = Article.load_articles()
    build_readme_summary(articles)


if __name__ == '__main__':
    main(is_test_mode=False)
