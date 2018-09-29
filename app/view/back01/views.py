import json

from flask import render_template, request

from app.models import *
from app.service.ArticleService import addArticle
from app.view.MessageInfo import MessageInfo
from app.view.back01 import back01
from datetime import datetime
from app.models import db
@back01.route('/back01', methods=['GET'])

def index():
    return render_template('back01/index01.html')

@back01.route('/back01/doucment', methods=['GET'])
def doucmentEdit():
    return render_template('back01/document_edit.html')


@back01.route('/back01/doucment01', methods=['GET'])
def doucmentEdit01():
    return render_template('back01/form_component.html')



#保存文章
@back01.route('/back01/addArticle', methods=['POST'])
def saveArticle():

    #解析前端传过来的json数据s
    data = json.loads(request.get_data("utf-8"))
    title = data['title']
    subtitle = data['subtitle']
    brief = data['brief']

    keyword = data['keyword']
    content = data['content']
    type = data['type']             #0代表保存，1代表保存并且发布


    article = Article()
    article.article_type = 1            #代表图文
    article.title = title
    article.sub_title = subtitle
    article.brief = brief
    article.key_words = keyword
    article.content = content
    article.last_modifyer_time = datetime.now()       #最后修改时间设置为当前时间
    article.creator_id = "32578453825483"           #先随便设一个字段
    if type == 1:
        article.publish_sign = 1                    #设置为已发布
        article.publish_id = article.creator_id     #发布人id就是创建人id
        article.publish_time = datetime.now()
        article.true_publish_time = datetime.now()


    #这些ID先随便设置，会设计到外键约束的问题。需额外建表
    article.creator_id = '64893264982'
    article.article_id = '6438926555555555555555'

    article.is_attachment = 0;


    # db.session.add(article)
    # db.session.commit()
    if addArticle(article):
        return json.dumps(MessageInfo.success(data='添加成功').__dict__)
    else:
        return json.dumps(MessageInfo.fail(data="添加失败").__dict__)








