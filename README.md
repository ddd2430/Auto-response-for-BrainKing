# Auto-response-for-BrainKing
This is an auto-response script for BrainKing miniprogram in WeChat. It's only used for studying and communication. Please don't use it to gain benefits or cheat.
There are three .py files. 'BK_auto' is used to auto-response for BrainKing. 'BK_collector' is used to collect questions in '.txt' files in BrainKing and BrainKingAnswer folders and finally produce a '.xls' file in BrainKingAnswer folder. And 'BK_merge' is used to merge the '.xls' files in last step and 'a.xls' in BrainKingBank folder. 'a.xls' is question bank in this program.
The compression package includes 'adb' and 'fiddler' to operate your android mobile phone and capture the data packege in your phone, respectively.

这是一个头脑王者的自动答题脚本，只用作学习交流使用，严禁用来获取利益或作弊，否自后果自负，如果有涉及侵权立即删除！

压缩包里包含用来抓包的fiddler，和用来操作安卓手机的adb 。可能需要自定义fiddler的custom rules，在onBeforeResponse函数中添加写入文件的功能。具体可查看源代码。

一共三个脚本，BK_auto是答题脚本，BK_collector用来从.txt文件中收集题目到Excel文件中，BK_merge文件用来将收集到的题目合并到题库中去。每次答题前会优先在BrainKingBank/a.xls中查找题目，为提高访问效率，在初始化时先将题库读到内存中，并按typeID分类，这样查找时就可以根据typeID在指定范围内查找，而不是搜索整个题库。

最后，喜欢的朋友请点个赞--，欢迎交流。
