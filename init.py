import sqlite3
import re
cx=sqlite3.connect("./data.db")
cu=cx.cursor()
cu.execute('create table if not exists User (StudentID nvarchar(30) primary key,Name nvarchar(30),Drcom_Num nvarchar(30),IDcard nvarchar(30),TybPasswd nvarchar(30))')
fd=open('drcom','r')
for line in fd:
    if line.find('\'')>-1:
        print('SQL injection detected')
        continue
    sm=line.split('\t')
    try:
        cu.execute("insert into User values('"+sm[0]+"','"+sm[1]+"','','"+sm[3]+"','"+sm[4]+"')")
    except Exception as e:
        print (e)
        pass
fi=open('./drcom_num')
for line in fi:
    dr=line.split('\t')[6].split('\n')[0]
    stu=line.split('\t')[0]
    cu.execute('update User set Drcom_Num=\''+dr+'\' where StudentID=\''+stu+'\'')
cx.commit()
