#coding:utf-8
import subprocess
import requests
import os
import json
import urllib2
import time
import sys
import xlwt,xlrd
import random
import time
#from io import BytesIO
#from PyQt4.QtCore import *
from PyQt4.QtGui import *
from watchdog.observers import Observer
from watchdog.events import *
from xlutils.copy import copy
from pywinauto import application
from lxml import etree

class FileEventHandler(FileSystemEventHandler):
    
    def __init__(self):
        FileSystemEventHandler.__init__(self)
        process=subprocess.Popen('adb\\adb shell wm size',shell=True,stdout=subprocess.PIPE)
        sizeStr=process.stdout.read()
        self.w,self.h=int(sizeStr[sizeStr.index(':')+2:sizeStr.index('x')]),int(sizeStr[sizeStr.index('x')+1:])
        self.level=0
        self.cwd=os.getcwd()
        self.app = application.Application()
        self.app.start(self.cwd+"\\Fiddler\\Fiddler.exe")
        #初始化时将表格数据都读到一个列表中,一个三维数组,第一维指定了题目类型，在题库中题目越来越多时，可以有效减少查找时间
        self.questionTable=[[] for i in range(100)]
        table=xlrd.open_workbook(self.cwd+'\\BrainKingBank\\a.xls')
        sheet=table.sheets()[0]
        nrows=sheet.nrows
        for i in range(nrows):
            temp_arr=sheet.row_values(i)
            temp_arr=[int(temp_arr[0]),temp_arr[1],temp_arr[2]]
            typeID=int(temp_arr[0])
            self.questionTable[typeID].append(temp_arr)
            
    def searchInBaidu(self,question,answers):
        #w=win32gui.FindWindow(None,u'Progress Telerik Fiddler Web Debugger')
        #在百度搜索答案前将fiddler暂停（不然会很慢）
        self.app['Progress Telerik Fiddler Web Debugger'].MenuSelect('File->Capture Traffic')
        try:
            #百度知道整个网站编码为gbk编码，所以要转为utf8编码再查找
            zhidaoText=str(urllib2.urlopen(u'https://zhidao.baidu.com/search?word='+question,timeout=3).read()).decode('gbk').encode('utf-8')
            #三短一长
            for i in range(len(answers)):
                answers[i]=[zhidaoText.count(str(answers[i])),answers[i],i]
            answers.sort(reverse=True)
        except:
            print(u'访问百度知道出错')
            for i in range(len(answers)):
                answers[i]=[0,answers[i],i]
        #三长一短，且出现了‘不’，‘没’等否定词，这些否定词并没有出现在'「'和'「'之间
        flag=(answers[0][0]-answers[1][0])+(answers[0][0]-answers[2][0])-(answers[1][0]-answers[3][0])-(answers[2][0]-answers[3][0])
        indexBu,indexMei,indexCuo,indexZuo,indexYou,indexShuZuo,indexShuYou=question.find(u'不'),question.find(u'没'),question.find(u'错'),question.find(u'「'),question.find(u'」'),question.find(u'《'),question.find(u'》')
        if (indexBu!=-1 and not indexZuo<indexBu<indexYou and not indexShuZuo<indexBu<indexShuYou and not question[indexBu+1] in [u'起',u'幸']) or (indexMei!=-1 and not indexZuo<indexMei<indexYou and not indexShuZuo<indexMei<indexShuYou) or (indexCuo!=-1 and not indexZuo<indexCuo<indexYou and not indexShuZuo<indexCuo<indexShuYou):
            if (0 in [answers[0][0],answers[1][0],answers[2][0],answers[3][0]]) or (1 in [answers[0][0],answers[1][0],answers[2][0],answers[3][0]]) or flag<=0:
                print(u'discover No')
                answers.sort()
        #如果排名前2的答案频次相同
        if answers[0][0]==answers[1][0]:
            print(u'百度主页')
            try:
                #百度主页的默认编码方式是utf8
                baiduText=str(urllib2.urlopen(u'http://www.baidu.com/s?wd='+question,timeout=2).read())
                for i in range(len(answers)):
                    answers[i][0]=baiduText.count(str(answers[i][1]))
                answers.sort(reverse=True)
            except:
                print(u'访问百度主页出错')
            #三长一短，出现了‘不’，‘没’等否定词,这些否定词并没有出现在'「'和'「'之间
            flag=(answers[0][0]-answers[1][0])+(answers[0][0]-answers[2][0])-(answers[1][0]-answers[3][0])-(answers[2][0]-answers[3][0])
            if (indexBu!=-1 and not indexZuo<indexBu<indexYou and not indexShuZuo<indexBu<indexShuYou and not question[indexBu+1] in [u'起',u'幸']) or (indexMei!=-1 and not indexZuo<indexMei<indexYou and not indexShuZuo<indexMei<indexShuYou) or (indexCuo!=-1 and not indexZuo<indexCuo<indexYou and not indexShuZuo<indexCuo<indexShuYou):
                if (0 in [answers[0][0],answers[1][0],answers[2][0],answers[3][0]]) or (1 in [answers[0][0],answers[1][0],answers[2][0],answers[3][0]]) or flag<0:
                    print(u'题目中出现了否定词')
                    answers.sort()
            #如果排名前2的答案频次相同，打开百度知道前几个具体的问题查找答案
            for i in range(2):
                if answers[0][0]==answers[1][0]:
                    #xpath查找时会根据网页所指定的编码查找，所以此处转回gbk编码
                    try:
                        print(1)
                        tree=etree.HTML(zhidaoText.decode('utf-8').encode('gbk'))
                        print(2)
                        zhidaoUrl=tree.xpath('//div[@id="wgt-list"]/dl/dt/a')[i].get('href')
                        print(3)
                        zhidaoContent=str(urllib2.urlopen(zhidaoUrl,timeout=2).read()).decode('gbk').encode('utf-8')
                        print(4)
                        for j in range(len(answers)):
                            answers[j][0]=zhidaoContent.count(str(answers[j][1]))
                        answers.sort(reverse=True)
                        #三长一短，出现了‘不’，‘没’等否定词,这些否定词并没有出现在'「'和'「'之间
                        flag=(answers[0][0]-answers[1][0])+(answers[0][0]-answers[2][0])-(answers[1][0]-answers[3][0])-(answers[2][0]-answers[3][0])
                        if (indexBu!=-1 and not indexZuo<indexBu<indexYou and not indexShuZuo<indexBu<indexShuYou and not question[indexBu+1] in [u'起',u'幸']) or (indexMei!=-1 and not indexZuo<indexMei<indexYou and not indexShuZuo<indexMei<indexShuYou) or (indexCuo!=-1 and not indexZuo<indexCuo<indexYou and not indexShuZuo<indexCuo<indexShuYou):
                            if (0 in [answers[0][0],answers[1][0],answers[2][0],answers[3][0]]) or (1 in [answers[0][0],answers[1][0],answers[2][0],answers[3][0]]) or flag<0:
                                print(u'题目中出现了否定词')
                                answers.sort()
                        print(5)
                    except:
                        print(u'深入查找出错')
                else:
                    break
            
            #如果深入查找还是没有找到，则说明题目的选项比较长，可以将每个字分开查找
            if answers[0][0]==answers[1][0]:
                print(u'开始拆分选项查找')
                try:
                    for i in range(len(answers)):
                        for j in range(len(answers[i][1])):
                            answers[i][0]+=zhidaoText.count(str(answers[i][1][j]))
                except:
                    print(u'拆分查找出错')
                answers.sort(reverse=True)
                flag=(answers[0][0]-answers[1][0])+(answers[0][0]-answers[2][0])-(answers[1][0]-answers[3][0])-(answers[2][0]-answers[3][0])
                if (indexBu!=-1 and not indexZuo<indexBu<indexYou and not indexShuZuo<indexBu<indexShuYou and not question[indexBu+1] in [u'起',u'幸']) or (indexMei!=-1 and not indexZuo<indexMei<indexYou and not indexShuZuo<indexMei<indexShuYou) or (indexCuo!=-1 and not indexZuo<indexCuo<indexYou and not indexShuZuo<indexCuo<indexShuYou):
                    print(u'题目中出现了否定词')
                    answers.sort()
        print([answers[0][0],answers[1][0],answers[2][0],answers[3][0]])
        #搜索答案结束之后再开启fiddler
        self.app['Progress Telerik Fiddler Web Debugger'].MenuSelect('File->Capture Traffic')
        print(answers[0][2])
        return answers[0][2]
    
    def searchInTable(self,question,answers,typeID):
        for i in self.questionTable[typeID]:
            if question==i[1]:
                for j in range(len(answers)):
                    if i[2]==answers[j]:
                        print(u'在表中找到了答案：'+str(i[0])+u'-----'+str(i[1])+u'>>>>>'+str(i[2]))
                        return j
                print(u'在表中第'+str(i)+u'行找到了问题，但选项与答案不匹配')
                return -1
        return -1
        
    def click(self,correctNum):#swipe
        #print(int((0.47+0.11*correctNum)*self.h))
        cmd='adb\\adb shell input tap %s %s' % (
                int(0.5*self.w),
                int((0.47+0.11*correctNum)*self.h),
            )
        subprocess.Popen(cmd,shell=True)
        
    def on_modified(self,event):
        if not event.is_directory:
            path=os.path.realpath(event.src_path)
            #print(u"修改了文件>{0}".format(path))
            ext=os.path.splitext(path)[1]
            if ext=='.txt' or ext=='.log':
                try:
                    time.sleep(1)
                    #此处，由于fiddler保存的是utf16编码的文件，python读取的时候有时候只能读取到一部分，所以以二进制的方式读取，之后在用utf16解码
                    with open(path,'rb') as f:    
                        text=f.read().decode('utf-16')
                except:
                    print('read error****')
                    #接收到的是findQuzi数据包
                if text[0:8]==u'findQuiz':
                    try: 
                        indexQuiz=text.index(u'"quiz":')
                        indexOptions=text.index(u'"options":')
                        indexNum=text.index(u'"num":')
                        indexTypeID=text.index(u'"typeID":')
                        indexContri=text.index(u'"contributor":')
                        question=text[indexQuiz+8:indexOptions-2]
                        answers=text[indexOptions+12:indexNum-3].split('","')
                        answersIntable=text[indexOptions+12:indexNum-3].split('","')
                        typeID=int(text[indexTypeID+9:indexContri-1])
                        #print(u"typeID------"+str(typeID))
                        print(u'题目：'+question)
                    except:
                        print(u'*******read error****')
                        return
                    try:
                        indexMath=text.find('"type":')
                        questionType=text[indexMath+8:indexMath+10]
                    except:
                        questionType=u'未知'
                    #如果题目是数学题：
                    if questionType==u'数学':
                        print(u'********检测到一道数学题目********')
                        try:
                            calcAnswer=str(eval(question.replace(u'×',u'*').replace(u'÷',u'/').replace(u'＝','').replace(u'？','')))
                            print(calcAnswer)
                            for i in range(len(answers)):
                                if calcAnswer==answers[i]:
                                    self.click(i)
                                    time.sleep(2)
                                    self.click(i)
                                    time.sleep(2)
                                    self.click(i)
                                    return
                        except:
                             pass
                    correctAns=self.searchInTable(question,answersIntable,typeID)
                    print(correctAns)
                    if correctAns==-1:
                        correctAns=self.searchInBaidu(question,answers)
                        self.click(correctAns)
                        time.sleep(1)
                        self.click(correctAns)
                        time.sleep(1)
                        self.click(correctAns)
                        time.sleep(0.5)
                        self.click(correctAns)
                        time.sleep(0.5)
                        self.click(correctAns)
                        time.sleep(1)
                        self.click(correctAns)
                        #time.sleep(1)
                        
                    else:
                        #self.app['Progress Telerik Fiddler Web Debugger'].MenuSelect('File->Capture Traffic')
                        self.click(correctAns)
                        time.sleep(1)
                        self.click(correctAns)
                        time.sleep(1)
                        self.click(correctAns)
                        time.sleep(0.5)
                        self.click(correctAns)
                        time.sleep(0.5)
                        self.click(correctAns)
                        time.sleep(1)
                        self.click(correctAns)
                        #time.sleep(1)
                        #self.app['Progress Telerik Fiddler Web Debugger'].MenuSelect('File->Capture Traffic')
                #elif text[0:8]==u'chooseAn':
                    
                #这一部分是在挑战结束后自动点击继续挑战，如果要手动点击，请注释这一部分
                #接收到的是fightResult数据包
                elif text[0:8]==u'fightRes':
                    print(u'本轮挑战结束！')
                    #self.app['Progress Telerik Fiddler Web Debugger'].MenuSelect('File->Exit')
                    #升级了
                    try:
                        levelIndex=text.index('"level":')
                        isOutIndex=text.index('"isOut":')
                        level=int(text[levelIndex+8:isOutIndex-1])
                        if self.level!=0 and self.level<level:
                            cmd='adb\\adb shell input tap %s %s' % (
                                int(0.5*self.w),
                                int((0.67)*self.h),
                            )
                            time.sleep(8)
                            subprocess.Popen(cmd,shell=True)
                            time.sleep(3)
                        self.level=level
                        print(u'当前等级'+str(self.level))
                    except:
                        print(u'处理升级出错')
                    #点一下继续挑战
                    try:
                        print(1)
                        cmd='adb\\adb shell input tap %s %s' % (
                                int(0.5*self.w),
                                int(0.66*self.h),
                            )
                        print(2)
                        time.sleep(3)
                        print(3)
                        time.sleep(4)
                        subprocess.Popen(cmd,shell=True)
                        print(4)
                        #time.sleep(5)
                        time.sleep(2)
                        print(5)
                        time.sleep(1)
                        #选择难度
                        cmd='adb\\adb shell input tap %s %s' % (
                                int(0.5*self.w),
                                int(0.89*self.h),
                            )
                        subprocess.Popen(cmd,shell=True)
                        time.sleep(1)
                        cmd='adb shell input tap %s %s' % (
                                int(0.5*self.w),
                                int(0.79*self.h),
                            )
                        subprocess.Popen(cmd,shell=True)
                        time.sleep(1)
                        cmd='adb shell input tap %s %s' % (
                                int(0.5*self.w),
                                int(0.67*self.h),
                            )
                        subprocess.Popen(cmd,shell=True)
                    except:
                        print(u'继续挑战失败')
                    
             
def main():
    print(u'开始!')
    observer=Observer()
    event_handler=FileEventHandler()
    observer.schedule(event_handler,event_handler.cwd+'\\BrainKing',True)
    observer.start()
    app = QApplication([])
    sys.exit(app.exec_())
    
if __name__=='__main__':
    main()
