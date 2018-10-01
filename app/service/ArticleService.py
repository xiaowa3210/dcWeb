import traceback
from datetime import datetime
from  app.model.models import db

#添加文章
from app.model.models import Article

def getArticleByID(article_id):
    return db.session.query(Article).filter(Article.article_id == article_id).one()

def addArticle(article):
     try:
        db.session.add(article)
        db.session.commit()
     except:
         return False
     return True
def getArticlesByPage(page_index,per_page):
    # 这个地方要用到分页查询。带删除标志的不要展示出来了
    pagination = Article.query.filter(Article.delete_flag == 0).paginate(page_index, per_page, error_out=False)
    articles = pagination.items
    return articles,pagination

#逻辑删除文章,将删除标志位设为1
def deleteArticleByID(article_id):
    update_content = dict()
    update_content[Article.delete_flag] = 1
    update_content[Article.deleter_id] = "6489264936829"
    update_content[Article.delete_time] = datetime.now()
    try:
        db.session.query(Article).\
            filter(Article.article_id == article_id).update(update_content)
        db.session.commit()
    except Exception as e:
        traceback.print_exc()
        return False
    return True


#修改文章
def updateArticleByID(article):
    update_content = dict()
    update_content[Article.title] = article.title
    update_content[Article.sub_title] = article.sub_title
    update_content[Article.brief] = article.brief
    update_content[Article.key_words] = article.key_words
    update_content[Article.content] = article.content

    #TODO:这个先随便设置,这个后面要改
    update_content[Article.last_modified_id] = "43824893274983"
    update_content[Article.last_modified_time] = datetime.now()

    try:
        db.session.query(Article).\
            filter(Article.article_id == article.article_id).update(update_content)
        db.session.commit()
    except Exception as e:
        traceback.print_exc()
        return False
    return True

#修改文章
def updateArticleSelcettive(article_id,update_content):
    try:
        db.session.query(Article).\
            filter(Article.article_id == article_id).update(update_content)
        db.session.commit()
    except Exception as e:
        traceback.print_exc()
        return False
    return True
