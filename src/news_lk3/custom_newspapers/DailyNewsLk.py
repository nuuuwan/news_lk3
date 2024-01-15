import os

from utils import TimeFormat

from news_lk3.core import AbstractNewsPaper

URL_BASE = 'http://dailynews.lk'
TIME_RAW_FORMAT = '%A, %B %d, %Y - %H:%M'


class DailyNewsLk(AbstractNewsPaper):
    @classmethod
    def get_index_urls(cls):
        return [os.path.join(URL_BASE, 'category/local')]

    @classmethod
    def parse_article_urls(cls, soup):
        article_urls = []
        for div in soup.find_all('li', {'class': 'views-row'}):
            article_url = os.path.join(
                URL_BASE,
                div.find('a').get('href')[1:],
            )
            article_urls.append(article_url)
        return article_urls

    @classmethod
    def parse_time_ut(cls, soup):
        span_time = soup.find('span', {'class': 'date-display-single'})
        return TimeFormat(TIME_RAW_FORMAT).parse(span_time.text.strip()).ut

    @classmethod
    def parse_title(cls, soup):
        h1 = soup.find('h1', {'class': 'title'})
        return h1.text

    @classmethod
    def parse_body_lines(cls, soup):
        divs = soup.find_all('div', {'class': 'field-item'})
        body_lines = []
        for div in divs:
            body_lines += list(
                map(
                    lambda line: line.strip(),
                    div.text.strip().split('\n'),
                )
            )
        return body_lines
