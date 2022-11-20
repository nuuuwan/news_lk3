from news_lk3._utils import log
from news_lk3.core import Article
from news_lk3.core.articles_summary import build_articles_summary
from news_lk3.core.filesys import git_checkout
from news_lk3.core.news_wordcloud import (build_wordcloud,
                                          build_wordcloud_animation)
from news_lk3.core.readme import build_readme_summary
from news_lk3.core.trends import build_trending_summary
from news_lk3.core.upload_data import upload_data


def main(is_test_mode=False):
    log.debug(f'{is_test_mode=}')
    git_checkout(force=True)
    upload_data(is_test_mode)

    articles = Article.load_articles()

    ent_to_group, group_to_n = build_trending_summary(articles)
    build_wordcloud(group_to_n)
    build_wordcloud_animation(10, 1)
    build_wordcloud_animation(150, 0.16)

    build_articles_summary(articles, ent_to_group)

    build_readme_summary(articles)


if __name__ == '__main__':
    main(is_test_mode=False)
