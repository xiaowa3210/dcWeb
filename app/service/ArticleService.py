
from datetime import datetime
from  app.models import db

#添加文章
from app.models import Article


def addArticle(article):
     try:
        db.session.add(article)
        db.session.commit()
     except:
         return False
     return True


if __name__ == '__main__':

    article = Article()
    article.article_type = 1  # 代表图文
    article.title = "dadada"
    article.sub_title = "dadada"
    article.brief = "dadada"
    article.key_words = "dadada"
    article.content = "dadada"
    article.last_modifyer_time = datetime.now  # 最后修改时间设置为当前时间
    article.creator_id = "32578453825483"  # 先随便设一个字段
    if 1 == 1:
        article.publish_sign = 1  # 设置为已发布
        article.publish_id = article.creator_id  # 发布人id就是创建人id
        article.publish_time = datetime.now
        article.true_publish_time = datetime.now

    # 这些ID先随便设置，会设计到外键约束的问题。需额外建表
    article.creator_id = '64893264982'
    article.article_id = '64893264982'

    article.is_attachment = 0;

    addArticle(article)

    # admin = User(username='21', pwd='21211')
    # db.session.add(admin)
    # db.session.commit()