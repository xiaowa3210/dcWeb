from ..models import User, Role
from app import db

role_dict = {
    1:'学生',
    2:'老师',
    3:'管理员'
}

#添加用户
def addUser(username,password,role):
    user = User(username,password)
    role = Role(role_dict[role])
    user.roles = [role]
    User.add(user)

#根据ID删除用户
def deleteUserByUserId(userID):
    User.query().filter(User.id == userID).delete()
#根据用户名删除用户
def deleteUserByUserId(username):
    User.query().filter(User.username == username).delete()


def modifyPasswordByUserId(userId, newpwd):
    User.query().filter(User.id == userId).update({User.password:newpwd})

#根据id查询用户信息
def getUserById(userID):
    return User.query().filter(User.id == userID).one

#根据用户名查询用户信息
def getUserByUsername(username):
    return User.query().filter(User.username == username).one

