from functools import cached_property

from utils import Directory, GitReadOnly, Log

from news_lk3.core import Article

DIR_REPO = '/tmp/news_lk3_data-reports'
log = Log('ArticleSummary')


class ArticleSummary:
    def __init__(self):
        self.git = GitReadOnly('https://github.com/nuuuwan/news_lk3_data.git')
        self.git.clone(DIR_REPO, force=True)

    @cached_property
    def articles(self):
        articles = []
        for file in Directory(DIR_REPO).children:
            if file.ext != 'json':
                continue
            article = Article.load_from_file(file.path)
            articles.append(article)
        n_articles = len(articles)
        log.debug(f'Loaded {n_articles} articles')
        return articles


if __name__ == '__main__':
    ArticleSummary().articles
