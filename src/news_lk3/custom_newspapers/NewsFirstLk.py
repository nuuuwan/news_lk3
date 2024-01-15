from utils import TimeFormat

from news_lk3.core import AbstractNewsPaper

TIME_RAW_FORMAT = '%d %b, %Y\t| %I:%M %p'
H1_CLASS = 'text-left w-600 text-foxblue hidden-xs hidden-sm artical-hd-out'


class NewsFirstLk(AbstractNewsPaper):
    @classmethod
    def use_selenium(cls):
        return True

    @classmethod
    def get_index_urls(cls):
        return [
            'https://www.newsfirst.lk/latest-news/',
        ]

    @classmethod
    def parse_article_urls(cls, soup):
        article_urls = []
        for div in soup.find_all('div', {'class': 'desktop-news-block-ppd'}):
            article_url = div.find('a').get('href')
            article_urls.append(article_url)
        return article_urls

    @classmethod
    def parse_time_ut(cls, soup):
        span_time = soup.find('p', {'class': 'artical-new-byline'})
        s = span_time.text.strip()
        lines = s.split('\n')
        return TimeFormat(TIME_RAW_FORMAT).parse(lines[2]).ut

    @classmethod
    def parse_title(cls, soup):
        h1 = soup.find('h1', {'class': H1_CLASS})
        return h1.text

    @classmethod
    def parse_body_lines(cls, soup):
        header_inner = soup.find('div', {'class': 'thumb-para'})
        return list(
            map(
                lambda line: line.strip(),
                header_inner.text.strip().split('\n'),
            )
        )
