#coding:utf-8

import xlwt,xlrd
from xlutils.copy import copy
import sys
import time
import os
cwd=os.getcwd()
fullList=os.listdir(cwd+'\\BrainKing')
fileList=[]
for i in range(len(fullList)):
    if fullList[i][-4:]=='.txt':
        fileList.append(fullList[i])
    elif fullList[i][-4:]=='.log':
        os.remove(cwd+u'\\BrainKing\\'+fullList[i])
full2List=os.listdir(cwd+u'\\BrainKingAnswer')
answerList=[]
table_wt=xlwt.Workbook(encoding='utf-8')
sheet_wt=table_wt.add_sheet('Question and Answer')
for i in range(len(full2List)):
    if full2List[i][-4:]=='.txt':
        answerList.append(full2List[i])
if len(fileList)!=len(answerList):
    print(u'error')
else:
    for i in range(len(fileList)):
        try:
            if os.path.splitext(fileList[i])[1]=='.txt':
                with open(cwd+u'\\BrainKing\\'+fileList[i],'rb') as f:
                    textQuestion=f.read().decode('utf-16')
                with open(cwd+u'\\BrainKingAnswer\\'+answerList[i],'rb') as f:
                    textAnswer=f.read().decode('utf-16')
                indexQuiz=textQuestion.index(u'"quiz":')
                indexOptions=textQuestion.index(u'"options":')
                indexNum=textQuestion.index(u'"num":')
                indexTypeID=textQuestion.index(u'"typeID":')
                indexContri=textQuestion.index(u'"contributor":')
                question=textQuestion[indexQuiz+8:indexOptions-2]
                answers=textQuestion[indexOptions+12:indexNum-3].split('","')
                
                typeID=textQuestion[indexTypeID+9:indexContri-1]
                questionNum=textQuestion[indexNum+6:indexNum+7]
                indexAns=textAnswer.index(u'"answer":')
                indexAnsNum=textAnswer.index(u'"num":')
                corrAnswer=int(textAnswer[indexAns+9:indexAns+10])
                answerNum=textAnswer[indexAnsNum+6:indexAnsNum+7]
                if questionNum!=answerNum:
                    print(fileList[i])
                else:
                    sheet_wt.write(i,1,question)
                    sheet_wt.write(i,2,answers[corrAnswer-1])
                    sheet_wt.write(i,0,int(typeID))
                    os.remove(cwd+u'\\BrainKingAnswer\\'+answerList[i])
                    os.remove(cwd+u'\\BrainKing\\'+fileList[i])
        except:
            i-=1
            pass
              
    excelName=str(time.strftime('%Y-%m-%d %H_%M_%S',time.localtime(time.time())))+u'.xls'
    table_wt.save(cwd+'\\BrainKingAnswer\\'+excelName)
