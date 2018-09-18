INSERT INTO project (pname, introduction,create_time)
    VALUES
    ("古代诗歌文化的数字化传承与展示"
     ,"这是一款在ios系统上应用的交互绘本产品，以非物质文化遗传——《诗经》为主题，利用中国传统绘画和传统颜色色谱表进行上色绘制，不同信息层级表现其风俗特征，每一步都充满浓郁的中国风格，再与中国传统音乐搭配，传统却又不刻板。 在技术上，通过多点触控技术，手势识别，加速度传感器，ios动画等多媒体技术进行的创新应用，形成了具有交互体验的互动绘本模型，更好地加深了读者理解、使其积极参与、主动操控。"
     ,CURRENT_DATE);


数据库中新增一列
alter TABLE project add teaminfo TEXT;

--清空一个表--
DELETE FROM project;



