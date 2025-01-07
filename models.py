from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Article(Base):
    __tablename__ = 'article'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    content = Column(Text)
    created_at = Column(Date)
    updated_at = Column(Date)
    
    comments = relationship('Comment', back_populates='article')

class Comment(Base):
    __tablename__ = 'comment'
    
    id = Column(Integer, primary_key=True)
    article_id = Column(Integer, ForeignKey('article.id'))
    content = Column(Text)
    created_at = Column(Date)
    updated_at = Column(Date)
    
    article = relationship('Article', back_populates='comments')