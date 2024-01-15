import os

from utils import TIME_FORMAT_TIME, Directory, Git, Log, Time, TSVFile

from news_lk3.core import Article

log = Log('ArticleSummary')


class ArticleSummary:
    @property
    def articles(self):
        git = Git('https://github.com/nuuuwan/news_lk3_data.git')
        git.clone(Article.DIR_REPO, force=True)
        git.checkout('main')

        articles = []
        for child in Directory(Article.DIR_REPO_ARTICLES).children:
            if isinstance(child, Directory) or child.ext != 'json':
                continue
            article = Article.load_from_file(child.path)
            articles.append(article)
        n_articles = len(articles)
        log.debug(f'Loaded {n_articles} articles')
        return articles

    @property
    def summary(self):
        d_list = []
        for article in self.articles:
            d_list.append(
                dict(
                    # more useful
                    newspaper_id=article.newspaper_id,
                    time_str=TIME_FORMAT_TIME.stringify(
                        Time(article.time_ut)
                    ),
                    original_title=article.original_title,
                    n_original_body_lines=len(article.original_body_lines),
                    # less useful
                    hash=Article.get_hash(article.url),
                    time_ut=article.time_ut,
                    original_lang=article.original_lang,
                    url=article.url,
                )
            )
        d_list = sorted(d_list, key=lambda d: d['time_ut'], reverse=True)
        return d_list

    @property
    def summary_file_path(self):
        return os.path.join(Article.DIR_REPO, 'summary.tsv')

    def store_summary(self):
        summary = self.summary
        if not Directory(Article.DIR_REPO).exists:
            os.makedirs(Article.DIR_REPO)
            log.debug(f'Created directory {Article.DIR_REPO}')

        TSVFile(self.summary_file_path).write(summary)
        log.debug(f'Stored summary to {self.summary_file_path}')
