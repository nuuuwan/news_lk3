import re

from utils import TimeFormat

from news_lk3.core import AbstractNewsPaper

TIME_RAW_FORMAT = '%B %d, %Y %I:%M %p'


class AdaDeranaLk(AbstractNewsPaper):
    @classmethod
    def use_selenium(cls):
        return True

    @classmethod
    def get_index_urls(cls):
        return [
            'http://www.adaderana.lk/hot-news/',
        ]

    @classmethod
    def parse_article_urls(cls, soup):
        article_urls = []
        for div in soup.find_all('div', {'class': 'news-story'}):
            article_url = div.find('a').get('href')
            article_urls.append(article_url)
        return article_urls

    @classmethod
    def parse_time_ut(cls, soup):
        span_time = soup.find('p', {'class': 'news-datestamp'})
        s = span_time.text.strip()
        s = re.sub(r'\s+', ' ', s)
        return TimeFormat(TIME_RAW_FORMAT).parse(s).ut

    @classmethod
    def parse_title(cls, soup):
        article = soup.find('article', {'class': "news"})
        h1 = article.find('h1')
        return h1.text

    @classmethod
    def parse_body_lines(cls, soup):
        header_inner = soup.find('div', {'class': 'news-content'})
        return list(
            map(
                lambda line: line.strip(),
                header_inner.text.strip().split('\n'),
            )
        )
