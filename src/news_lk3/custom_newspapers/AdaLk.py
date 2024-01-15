from news_lk3.core import AbstractNewsPaper


class AdaLk(AbstractNewsPaper):
    @classmethod
    def get_original_lang(cls):
        return 'si'

    @classmethod
    def get_index_urls(cls):
        return [
            'https://www.ada.lk/latest-news/11',
            'https://www.ada.lk/technology/5',
            'https://www.ada.lk/business/7',
        ]

    @classmethod
    def parse_article_urls(cls, soup):
        article_urls = []
        for div in soup.find_all('div', {'class': 'cat-detail-1'}):
            article_url = div.find('a').get('href')
            article_urls.append(article_url)
        return article_urls

    @classmethod
    def parse_title(cls, soup):
        h1 = soup.find('h1', {'class': 'single-head'})
        return h1.text

    @classmethod
    def parse_body_lines(cls, soup):
        div_body = soup.find('div', {'class': 'single-body-wrap'})
        return list(
            map(
                lambda line: line.strip(),
                div_body.text.strip().split('\n'),
            )
        )
