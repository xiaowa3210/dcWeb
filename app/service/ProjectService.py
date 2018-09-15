from ..models import Project

def getProjectsByPage(page_index,per_page):

    # 这个地方要用到分页查询，每次查询12页
    pagination = Project.query.paginate(page_index, per_page, error_out=False)
    projects = pagination.items
    return pagination,projects

def getProjectById(pid):
    return Project.query.filter(Project.id == pid).one()