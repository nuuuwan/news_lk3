import os

from utils import TIME_FORMAT_TIME, File, Log, Time

from news_lk3.core import Article
from news_lk3.reports.ArticleSummary import ArticleSummary

log = Log('ReadMe')


class ReadMe(ArticleSummary):
    PATH = os.path.join(Article.DIR_REPO, 'README.md')
    N_DISPLAY = 100

    @staticmethod
    def render_article(article) -> list[str]:
        return [
            f'### {article.original_title}',
            f'*{TIME_FORMAT_TIME.stringify(Time(article.time_ut))}'
            + f' - [{article.newspaper_id}]({article.url})*',
        ] + article.original_body_lines
    
    @staticmethod
    def render_article_stats(article_list) -> list[str]:
        lines = []
        newspaper_to_n = {}
        for article in article_list:
            newspaper_to_n[article.newspaper_id] = (
                newspaper_to_n.get(article.newspaper_id, 0) + 1
            )
        
        lines.append('## Newspaper Stats')
        for newspaper_id, n in newspaper_to_n.items():
            lines.append(f'* {n:, }{newspaper_id}')
        lines.append(f'* Total: {len(article_list):, }')
        return lines

    def write(self):
        articles = self.articles
        sorted_articles = sorted(
            articles, key=lambda a: a.time_ut, reverse=True
        )

        lines = [
            f'# Newspaper Articles from Sri Lanka :lka:',
            f'As of **{TIME_FORMAT_TIME.stringify(Time.now())}**',
        ]
        lines.extend(ReadMe.render_article_stats(sorted_articles))

        lines.append(f'## Latest Articles ({ReadMe.N_DISPLAY})')
        for article in sorted_articles[: self.N_DISPLAY]:
            lines.extend(ReadMe.render_article(article))

        File(ReadMe.PATH).write('\n\n'.join(lines))
        log.debug(f'Wrote {ReadMe.PATH}')
