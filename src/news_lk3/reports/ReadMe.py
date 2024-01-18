import math
import os

from utils import TIME_FORMAT_DATE, TIME_FORMAT_TIME, File, Log, Time

from news_lk3.core import Article
from news_lk3.reports.ArticleSummary import ArticleSummary

log = Log('ReadMe')


class ReadMe(ArticleSummary):
    PATH = os.path.join(Article.DIR_REPO, 'README.md')
    N_DISPLAY = 100
    BLOCK_EMOJI = '🟩'
    ARTICLE_BODY_MAX_CHARS = 480

    @staticmethod
    def render_article(article) -> list[str]:
        return [
            f'### {article.original_title}',
            '',
            f'*{TIME_FORMAT_TIME.stringify(Time(article.time_ut))}'
            + f' - [{article.newspaper_id}]({article.url})*',
            '',
            article.get_original_body(
                max_chars=ReadMe.ARTICLE_BODY_MAX_CHARS
            ),
            '',
        ]

    @staticmethod
    def render_stats_line(label: str, value: int, n_per_block: int):
        value_str = ReadMe.BLOCK_EMOJI * int(round(value / n_per_block))
        return f'* {value_str} ({value:,}) {label}'

    @staticmethod
    def round10(n: int) -> int:
        log_n = math.log10(n)
        n_rounded = 10 ** math.floor(log_n)
        return n_rounded

    @staticmethod
    def render_article_stats(article_list) -> list[str]:
        lines = []
        newspaper_to_n = {}
        for article in article_list:
            newspaper_to_n[article.newspaper_id] = (
                newspaper_to_n.get(article.newspaper_id, 0) + 1
            )
        n_per_block = ReadMe.round10(max(newspaper_to_n.values()) / 10)
        lines.extend(
            [
                '## Newspaper Stats',
                '',
                f'*Scraped **{len(article_list):,}** Articles*',
                '',
                f'{ReadMe.BLOCK_EMOJI} = {n_per_block}',
                '',
            ]
        )

        for newspaper_id, n in sorted(
            newspaper_to_n.items(), key=lambda x: x[1]
        ):
            lines.append(
                ReadMe.render_stats_line(newspaper_id, n, n_per_block)
            )

        lines.append('')

        return lines

    def write(self):
        articles = self.articles
        sorted_articles = sorted(
            articles, key=lambda a: a.time_ut, reverse=True
        )

        lines = [
            '# Newspaper Articles from Sri Lanka :sri_lanka:',
            '',
            f'As of **{TIME_FORMAT_TIME.stringify(Time.now())}**',
            '',
        ]
        lines.extend(ReadMe.render_article_stats(sorted_articles))

        lines.extend([f'## Latest {ReadMe.N_DISPLAY:,} Articles ', ''])
        prev_date_str = None
        for article in sorted_articles[: self.N_DISPLAY]:
            date_str = TIME_FORMAT_DATE.stringify(Time(article.time_ut))
            if date_str != prev_date_str:
                lines.extend([f'### {date_str}', ''])
                prev_date_str = date_str
            lines.extend(ReadMe.render_article(article))

        File(ReadMe.PATH).write('\n'.join(lines))
        log.debug(f'Wrote {ReadMe.PATH}')
