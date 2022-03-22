'''
Author: lijunhong
Date: 2022-03-19 12:54:26
Email: lijunhong@fengmap.com
LastEditTime: 2022-03-20 14:07:02
LastEditors: lijunhong
LastEditorsEmail: lijunhong@fengmap.com
Description: 
 Copyright: Copyright 2014 - 2022, FengMap, Ltd. All rights reserved.
'''
from bs4 import BeautifulSoup
from bs4.element import Tag
import json
import os
import logging


path ='./html'
html_list = os.listdir(path)
# print(type(sorted(html_list)))

output = []
output_list = [['标题', '专利号', '发明人', '权利人','年份', '被引频次']]

for html_file in sorted(html_list):
    html_path = path + '/' + html_file
    if not html_path.endswith('html'):
        continue
    print('正在处理文件：',html_file)
    print('--------------------')
    soup = BeautifulSoup(open(html_path), 'lxml')
    soup_list = soup.find_all('div', class_='summary-record')
    index = 0
    if not len(soup_list) == 50:
        print(html_path, len(soup_list))
    
    for item in soup_list: 
        obj = {}
        for child in item.descendants:
            if isinstance(child, Tag) and child.has_attr('id') and child['id'] == 'Summary-pan' and child.name == 'span':
                obj['Summary-pan'] = child.string[:4]  
            if isinstance(child, Tag) and child.name == 'app-summary-authors':
                assignee_str = 'SumAuthTa-' + str(index) + '-MainDiv-assignee-en'
                author_str = 'SumAuthTa-' + str(index) + '-MainDiv-inventor-en'
                index += 1
                for child_son in child.descendants:               
                    if isinstance(child_son, Tag) and child_son.has_attr('data-ta') :
                        # 发明人
                        if child_son['data-ta'] == author_str:
                            author = []
                            for span in child_son.descendants:
                                if isinstance(span, Tag) and not span.has_attr('class') and span.name == 'span' :
                                    author.append(span.string)
                            obj['author'] = author
                        # 专利权人
                        if child_son['data-ta'] == assignee_str:
                            assignee = []
                            for span in child_son.descendants:
                                if isinstance(span, Tag) and not span.has_attr('class') and span.name == 'span' :
                                    assignee.append(span.string)
                            obj['assignee'] = assignee
            if isinstance(child, Tag) and child.has_attr('class'):
                # 施引专利
                if child['class'][0] == 'stat-number':
                    obj['statNumber'] = child.string.strip().replace(',', '')
                # title
                if child['class'][0] == 'title' and child.name == 'a':
                    obj['title'] = child.string
                # 专利家族
                if child['class'][0] == 'patent-info-top':
                    patent = []
                    for span in child.contents:
                        if isinstance(span, Tag) and span.has_attr('class') and span.name == 'span' and span['class'][0] == 'value-wrap':
                            patent.append(span.string)
                    obj['patent'] = patent            
                   
        output.append(obj)
        obj_list = []
        for key,value in obj.items():
            if isinstance(value, list):
                value = ' '.join(value)
            obj_list.append(value)
        output_list.append(obj_list)
        # print(output_list)
    print('处理完成：',html_file)
    print('--------------------')





json_str = json.dumps(output_list)
with open('test_data.json', 'w') as json_file:
    json_file.write(json_str)


# fileObject = open('jsonFile.json', 'w')
# fileObject.write(jsObj)
# fileObject.close()

# def data_write_csv(file_name, datas):#file_name为写入CSV文件的路径，datas为要写入数据列表
#     file_csv = codecs.open(file_name,'w+','utf-8')#追加
#     writer = csv.writer(file_csv, delimiter=' ', quotechar=' ', quoting=csv.QUOTE_MINIMAL)
#     for data in datas:
#         writer.writerow(data)
#     print("保存文件成功，处理结束")
# data_write_csv('out.xls', output)