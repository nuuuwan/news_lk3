from utils import TimeFormat

from news_lk3.core import AbstractNewsPaper

TIME_RAW_FORMAT = "%d %b, %Y | %I:%M %p"


class VirakesariLk(AbstractNewsPaper):
    @classmethod
    def get_original_lang(cls):
        return "ta"

    @classmethod
    def get_index_urls(cls):
        return [
            "https://www.virakesari.lk/category/local",
            "https://www.virakesari.lk/category/feature",
        ]

    @classmethod
    def parse_article_urls(cls, soup):
        article_urls = []
        for a in soup.find_all("a", {"class": "news-item"}):
            article_url = a.get("href")
            article_urls.append(article_url)
        return article_urls

    @classmethod
    def parse_time_ut(cls, soup):
        div = soup.find("div", {"class", "auth-date"})
        assert div, "[parse_time_ut] div not found"
        h5 = div.find("h5", {"class", "news-date"})
        assert h5, "[parse_time_ut] h5 not found"
        time_str = h5.text.replace("\n", " ").strip()
        return TimeFormat(TIME_RAW_FORMAT).parse(time_str).ut

    @classmethod
    def parse_title(cls, soup):
        title = soup.find("title")
        assert title, "[parse_title] title not found"
        return title.text.split("|")[0].strip()

    @classmethod
    def parse_body_lines(cls, soup):
        div = soup.find("div", {"class": "article-content"})
        assert div, "[parse_body_lines] div not found"
        return list(
            map(
                lambda line: line.strip(),
                div.text.strip().split("\n"),
            )
        )
