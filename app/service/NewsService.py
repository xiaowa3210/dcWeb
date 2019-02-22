from datetime import datetime

from app import db2
from app.model.entity import New, newExt
from app.service.CommonService import CommonService

commonService = CommonService()
class NewsService:

    """
    添加新闻
    """
    def addNews(self,new):
        db2.session.add(new)
        db2.session.commit()

    """
    分页查询新闻
    """
    def selectByPage(self,page_index,per_page,type):
        if int(type) < 0:
            pagination = newExt.query.filter(newExt.deleteFlag == 0).order_by(newExt.createTime).paginate(
                page_index, per_page)
        else:
            pagination = newExt.query.filter(newExt.deleteFlag == 0,type).order_by(newExt.createTime).paginate(page_index, per_page)
        return pagination,pagination.items

    """ 
    根据id查询新闻具体内容
    """
    def selectByNid(self,nid):
        return db2.session.query(New).filter(New.nid == nid).one()

    """ 
    修改新闻
    """
    def updatenew(self,new):
        result = db2.session.query(New).filter(New.nid == new.nid).one()
        result.title = new.title
        result.content = new.content
        db2.commit()

    """ 
    @:param:
        updateContent:更新内容
        condition:查询条件
    @:return:
    @descrition:更新新闻状态信息
    """

    def updateNewsextraInfo(self, updateContent, condition):
        db2.session.query(newExt).filter(condition).update(updateContent)
        db2.session.commit()

    """ 
    @:param:
    @:return:
    @descrition:根据新闻ID更新新闻状态信息
    """

    def updateNewStatusByNid(self, updateContent,nid):
        db2.session.query(newExt).filter(newExt.nid == nid).update(updateContent)
        db2.session.commit()


    """ 
    发布或撤回新闻
    """
    def releaseOrUndoNew(self,nid,type):
        if type == 1:
            updateContent = {
                'status': type,
                'publisher': commonService.getCurrentUsername(),
                'publisherTime': datetime.now()
            }
        else:
            updateContent = {
                'status': type,
                'cancelTime': datetime.now()
            }
        self.updateNewStatusByNid(updateContent,nid)


    """ 
    删除新闻
    """
    def deleteNew(self,nid):
        updateContent = {
            'deleteFlag': 1
        }
        self.updateNewStatusByNid(updateContent, nid)

