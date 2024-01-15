from utils import TimeFormat

from news_lk3.core import AbstractNewsPaper

TIME_RAW_FORMAT = '%Y-%m-%d %I:%M %p'


class IslandLk(AbstractNewsPaper):
    @classmethod
    def get_index_urls(cls):
        return [
            'https://island.lk/category/news/'
            'https://island.lk/category/features/',
            'https://island.lk/category/business/',
            'https://island.lk/category/editorial/',
            'https://island.lk/category/politics/',
        ]

    @classmethod
    def parse_article_urls(cls, soup):
        article_urls = []
        for div in soup.find_all('li', {'class': 'mvp-blog-story-wrap'}):
            article_url = div.find('a').get('href')
            article_urls.append(article_url)

        return article_urls

    @classmethod
    def parse_time_ut(cls, soup):
        meta_time = soup.find('meta', {'itemprop': 'dateModified'})
        return (
            TimeFormat(TIME_RAW_FORMAT)
            .parse(meta_time.get('content').strip())
            .ut
        )

    @classmethod
    def parse_title(cls, soup):
        h1 = soup.find('h1', {'itemprop': 'headline'})
        return h1.text

    @classmethod
    def parse_author(cls, soup):
        a_author = soup.find('a', {'rel': 'author'})
        return a_author.text

    @classmethod
    def parse_body_lines(cls, soup):
        header_inner = soup.find('div', {'id': 'mvp-content-wrap'})
        return list(
            map(
                lambda line: line.strip(),
                header_inner.text.strip().split('\n'),
            )
        )
