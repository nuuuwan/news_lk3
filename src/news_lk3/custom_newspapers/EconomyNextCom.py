from utils import TimeFormat

from news_lk3.core import AbstractNewsPaper

TIME_RAW_FORMAT = '%A %B %d, %Y %I:%M %p'


class EconomyNextCom(AbstractNewsPaper):
    @classmethod
    def get_index_urls(cls):
        return [
            'https://economynext.com/more-news/',
            'https://economynext.com/economy/',
        ]

    @classmethod
    def parse_article_urls(cls, soup):
        article_urls = []
        for div in soup.find_all('div', {'class': 'story-grid-single-story'}):
            article_url = div.find('a').get('href')
            article_urls.append(article_url)
        return article_urls

    @classmethod
    def parse_time_ut(cls, soup):
        span_time = soup.find('div', {'class': 'story-page-pulish-datetime'})
        return TimeFormat(TIME_RAW_FORMAT).parse(span_time.text.strip()).ut

    @classmethod
    def parse_title(cls, soup):
        h1 = soup.find('h1', {'class': 'story-page-header'})
        return h1.text

    @classmethod
    def parse_author(cls, soup):
        div_author = soup.find('div', {'class': 'single-author'})
        return div_author.text.replace('By', '')

    @classmethod
    def parse_body_lines(cls, soup):
        header_inner = soup.find('div', {'class': 'story-page-text-main'})
        return list(
            map(
                lambda line: line.strip(),
                header_inner.text.strip().split('\n'),
            )
        )
