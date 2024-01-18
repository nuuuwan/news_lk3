from news_lk3.core import AbstractNewsPaper


class DailyMirrorLk(AbstractNewsPaper):
    @classmethod
    def get_time_raw_format(cls):
        return '%Y-%m-%dT%H:%M:%S%z'
        # return '%d %B %Y %I:%M %p' # previous

    @classmethod
    def get_index_urls(cls):
        return [
            'https://www.dailymirror.lk/latest-news/342',
            'https://www.dailymirror.lk/top-storys/155',
            'https://www.dailymirror.lk/business',
            'https://www.dailymirror.lk/opinion/231',
        ]

    @classmethod
    def parse_article_urls(cls, soup):
        article_urls = []
        for div in soup.find_all('div', {'class': 'col-md-8'}):
            article_url = div.find('a').get('href')
            article_urls.append(article_url)
        return article_urls

    @classmethod
    def parse_title(cls, soup):
        h1 = soup.find('h1', {'class': 'innerheader'})
        return h1.text

    @classmethod
    def parse_body_lines(cls, soup):
        header_inner = soup.find('header', {'class': 'inner-content'})
        return list(
            map(
                lambda line: line.strip(),
                header_inner.text.strip().split('\n'),
            )
        )
