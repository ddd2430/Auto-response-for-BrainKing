#ecoding:utf-8
import xlwt,xlrd
from xlutils.copy import copy
import sys
import time
import os
import shutil

cwd=os.getcwd()
#先把文件a.xls复制一个副本，防止出现不可恢复的错误
Fuben=str(time.strftime('%Y-%m-%d %H_%M_%S',time.localtime(time.time())))+u'.xls'
shutil.copyfile(cwd+"\\BrainKingBank\\a.xls", cwd+"\\BrainKingBank\\"+Fuben+'.a')
#过滤出文件夹中的.xls文件
full2List=os.listdir(cwd+'\\BrainKingAnswer')
answerList=[]
for i in range(len(full2List)):
    if full2List[i][-4:]=='.xls':
        answerList.append(full2List[i])
        
question_arr=[[] for x in range(100)]
#把所有题目和答案读取到列表中,按typeID分类到三维数组中
for i in range(len(answerList)):
    table=xlrd.open_workbook(cwd+'\\BrainKingAnswer\\'+answerList[i])
    sheet=table.sheets()[0]
    nrows=sheet.nrows
    for j in range(nrows):
        temp_arr_q=sheet.row_values(j)
        temp_arr_q=[int(temp_arr_q[0]),temp_arr_q[1],temp_arr_q[2]]
        typeID=int(temp_arr_q[0])
        question_arr[typeID].append(temp_arr_q)
        
#打开题库的数据表
bank_arr=[[] for x in range(100)]
table_bank=xlrd.open_workbook(cwd+'\\BrainKingBank\\a.xls')
sheet_bank=table_bank.sheets()[0]
nrows=sheet_bank.nrows
for j in range(nrows):
    temp_arr=sheet_bank.row_values(j)
    temp_arr=[int(temp_arr[0]),temp_arr[1],temp_arr[2]]
    typeID=int(temp_arr[0])
    bank_arr[typeID].append(temp_arr)

#合并两个数组，去掉重复的
merge_arr=bank_arr
for i in range(len(question_arr)):
    for j in question_arr[i]:
        flag=False
        for m in bank_arr[i]:
            if m==j:
                flag=True
                print(str(i)+'-----'+str(j[1])+u'>>>>>'+str(j[2])+'------'+u'相同')
                break
        if flag==False:
            #添加到bank
            merge_arr[i].append(j)
        else:
            continue
             
#写入新的数据表
table_wt=xlwt.Workbook(encoding='utf-8')
sheet_wt=table_wt.add_sheet('Question and Answer')
iterator=0
for i in range(len(merge_arr)):
    if merge_arr[i]!=[]:
        for j in merge_arr[i]:
            sheet_wt.write(iterator,0,j[0])
            sheet_wt.write(iterator,1,j[1])
            sheet_wt.write(iterator,2,j[2])
            iterator+=1
    
table_wt.save(cwd+'\\BrainKingBank\\a.xls')
#删除文件
for i in answerList:
    pass
    os.remove(cwd+'\\BrainKingAnswer\\'+i)

