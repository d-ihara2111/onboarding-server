# -*- encoding: utf-8 -*-
import sys
import models
import databases

def select_articles():
    # DBからユーザ情報を取得
    result = databases.session.query(models.Article).all()
    return result