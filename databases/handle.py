from databases.models import Article, ArticleQueryParams
from databases.settings import session

def select_articles(params: ArticleQueryParams):
    query = session.query(Article)
    
    if params.title:
        query = query.filter(Article.title.contains(params.title))
    
    result = query.offset(params.offset).limit(params.limit).all()
    return result