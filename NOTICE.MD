##### 项目删除
项目中dc_project_status_info表带删除标志位delete_flag，删除时为逻辑删除
delete_flag == 1,即为无用数据,需要管理员手动清楚无用数据。
注意：dc_project_status_info的时候需要把dc_project与之关联的数据删除

##### 新闻删除
dc_new_ext中带删除标志位
删除dc_new_ext的时候需要把dc_new对应的数据删除

##### 文件删除
表dc_files也带有表带删除标志位delete_flag。
delete_flag == 1,即为无用数据。
注意点1：删除每条记录的时候，需要删除与之对应的文件。文件位于项目的resources文件夹下。
dc_files中source的含义如下
- 1.代表封面图片
- 2:代表资料下载文件
- 3:获奖证书图片
- 4:代表新闻附件
1,3位于resources/pics下
2,4位于resources/files下
注：如果source = 1,name = default.png为默认封面图片。无需删除对应文件。



