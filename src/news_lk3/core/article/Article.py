from news_lk3.core.article.ArticleBase import ArticleBase
from news_lk3.core.article.ArticleFileSystem import ArticleFileSystem
from news_lk3.core.article.ArticleRender import ArticleRender


class Article(ArticleBase, ArticleFileSystem, ArticleRender):
    pass
