from news_lk3.core.article.ArticleBase import ArticleBase
from news_lk3.core.article.ArticleLoader import ArticleLoader
from news_lk3.core.article.ArticleRender import ArticleRender


class Article(ArticleBase, ArticleLoader, ArticleRender):
    pass
