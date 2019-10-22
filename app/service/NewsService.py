from datetime import datetime

from sqlalchemy import desc

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
    def selectByPage(self,page_index,per_page,status):
        if int(status) < 0:
            pagination = newExt.query.filter(newExt.deleteFlag == 0).order_by(desc(newExt.isTop)).order_by(desc(newExt.publisherTime)).paginate(
                page_index, per_page)
        else:
            pagination = newExt.query.filter(newExt.deleteFlag == 0,newExt.status==status).order_by(desc(newExt.isTop)).order_by(desc(newExt.publisherTime)).paginate(page_index, per_page)
        return pagination,pagination.items

    """
        分页查询新闻
        """

    def selectByUsername(self, page_index, per_page,status,username):
        if status is None or int(status) < 0:
            pagination = newExt.query.filter(newExt.deleteFlag == 0,newExt.creater == username).order_by(
                desc(newExt.publisherTime)).paginate(
                page_index, per_page)
        else:
            pagination = newExt.query.filter(newExt.deleteFlag == 0, newExt.status == status).order_by(
                desc(newExt.publisherTime)).paginate(page_index, per_page)
        return pagination, pagination.items
    """ 
    根据id查询新闻具体内容
    """
    def selectByNid(self,nid):
        return db2.session.query(New).filter(New.nid == nid).one()

    """ 
    修改新闻
    """
    def updatenew(self,new,status):
        result = db2.session.query(New).filter(New.nid == new.nid).one()
        result.title = new.title
        result.content = new.content
        result.src_content = new.src_content
        result.extInfo.status = int(status)+1
        result.extInfo.title = new.title
        result.extInfo.modifier = commonService.getCurrentUsername(0)
        result.extInfo.modifiedTime = datetime.now()
        if status == '1':
            result.extInfo.status = int(status)+1
            result.extInfo.publisher = commonService.getCurrentUsername(0)
            result.extInfo.publisherTime = datetime.now()
        db2.session.commit()

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
        if type == 1:  # 1代表发布
            updateContent = {
                'status': type,
                'publisher': commonService.getCurrentUsername(0),
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

