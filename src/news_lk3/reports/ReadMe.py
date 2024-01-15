import os

from utils import TIME_FORMAT_TIME, File, Log, Time

from news_lk3.core import Article
from news_lk3.reports.ArticleSummary import ArticleSummary

log = Log('ReadMe')


class ReadMe(ArticleSummary):
    PATH = os.path.join(Article.DIR_REPO, 'README.md')
    N_DISPLAY = 100

    def write(self):
        articles = self.articles
        sorted_articles = sorted(
            articles, key=lambda a: a.time_ut, reverse=True
        )
        lines = [
            f'# Articles (Latest {ReadMe.N_DISPLAY})',
            f'* As of {TIME_FORMAT_TIME.stringify(Time.now())}',
            '',
        ]
        for article in sorted_articles[: self.N_DISPLAY]:
            lines.extend(
                [
                    f'## {article.original_title}',
                    f'* {TIME_FORMAT_TIME.stringify(Time(article.time_ut))} *',
                ]
                + article.original_body_lines
                + ['']
            )

        File(ReadMe.PATH).write_lines(lines)
        log.debug(f'Wrote {ReadMe.PATH}')
