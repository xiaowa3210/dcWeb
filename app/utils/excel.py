import os

import xlwt


#获奖信息
class AwardInfo(object):
    def __init__(self, name, rank, time, project):
        self.name = name
        self.rank = rank
        self.time = time
        self.project = project  # 项目名
#获奖信息
class Member(object):
    def __init__(self, name, number, major):
        self.name = name
        self.number = number
        self.major = major
# 设置表格样式


def set_style(name, height, bold=False):
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = name
    font.bold = bold
    font.color_index = 4
    font.height = height
    style.font = font
    alignment = xlwt.Alignment() #创建居中
    alignment.vert = xlwt.Alignment.VERT_CENTER
    style.alignment = alignment
    return style


# 写Excel
def write_excel(awardInfos, filepath):
    f = xlwt.Workbook()
    sheet1 = f.add_sheet('学生', cell_overwrite_ok=True)
    row0 = ["获奖名称", "获奖级别", "获奖时间", "获奖项目", "成员"]
    sheet1.write_merge(0, 0, 4, 6)  # 合并成员单元格

    # 写表头
    for i in range(0, len(row0)):
        sheet1.write(0, i, row0[i], set_style('Times New Roman', 220, True))

    gs = 1
    # 写入具体信息
    for i in range(0, len(awardInfos)):
        s = gs
        e = 0
        award = awardInfos[i]
        name = award.name  # 获奖名称
        rank = award.rank  # 获奖级别
        time = award.time  # 获奖时间
        project = award.project  # 获奖项目

        item = (name, rank, time, project)
        for j in range(0, len(item)):
            sheet1.write(s, e, item[j], set_style('Times New Roman', 220, True))  # 第0列写入获奖名称
            e = e + 1

        members = award.members
        for p in range(0, len(members)):
            member = members[p]
            name = member.name  # 姓名
            number = member.number  # 学号
            major = member.major  # 专业

            e1 = e
            mem_item = (name, number, major)
            for n in range(0, len(mem_item)):
                sheet1.write(s, e1, mem_item[n], set_style('Times New Roman', 220, True))  # 第0列写入获奖名称
                e1 = e1 + 1
            s = s + 1

        # 合并单元格
        if(len(members) >= 2) :
            for j in range(0, len(item)):
                sheet1.write_merge(gs, s-1, j, j, item[j], set_style('Times New Roman', 220, True))
        gs = s
    f.save(filepath)


def createAward():
    award = AwardInfo("大创一等奖", "校内比赛", "2019-10", "VR虚拟与现实")
    members = []
    for i in range(3):
        member = Member()
        member.name = "小明"
        member.number = "2019123456"
        member.major = "通信专业"
        members.append(member)
    award.members = members
    return award

if __name__ == '__main__':
    awards = []
    loop = 6
    for i in range(loop):
        awards.append(createAward())

    write_excel(awards)
