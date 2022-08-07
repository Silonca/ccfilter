# ccfilter

CCF Filter

一个从DBLP的搜索结果中筛选CCF文章的Python脚本，筛选结果以csv文件导出

**使用方式**
```
usage: ccfilter.py [-h] [-f [FILE]] [-k KEYWORD [KEYWORD ...]]
                   [-r RANK [RANK ...]] [-s [STARTDATE]] [-e [ENDDATE]]
                   [-o [OUTFILE]]

optional arguments:
  -h, --help            show this help message and exit
  -f [FILE], --file [FILE]
                        从DBLP获取的搜索结果（JSON格式）
  -k KEYWORD [KEYWORD ...], --keyword KEYWORD [KEYWORD ...]
                        关键词（不能和目标文件同时指定）
  -r RANK [RANK ...], --rank RANK [RANK ...]
                        CCF级别: ('ca', 'cb', 'cc', 'ja', 'jb', 'jc')
  -s [STARTDATE], --startdate [STARTDATE]
                        发表时间限制（起点）
  -e [ENDDATE], --enddate [ENDDATE]
                        发表时间限制（终点）
  -o [OUTFILE], --outfile [OUTFILE]
                        指定输出文件的文件名
```



