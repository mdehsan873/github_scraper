from bs4 import BeautifulSoup
import urllib
import csv
import constant
import time
def getDetails(user):
    user_name=user.find('div',{'class','f4 text-normal'}).em.text.strip()
    name=user.find('div',{'class','f4 text-normal'}).a.text.strip()
    desctription=user.find('p',class_='mb-1')
    dict_service = {}
    dict_service['Name']=name
    dict_service['UserName']=user_name
    if desctription:
        dict_service['Des']=desctription.text.strip()
    else:
        dict_service['Des']='No Description'
    print(dict_service)
    return dict_service
def scraper():
    fields = ['Name', 'UserName', 'Des']
    out_file = open('scraped_data.csv','w')
    csvwriter = csv.DictWriter(out_file, delimiter=',', fieldnames=fields)    
    pageno=1
    while True:
        if pageno>10:
            break
        url=constant.BASE_URL+str(pageno)+constant.ATTRIBUTE1+constant.NAME+constant.SEARCH_TYPE
        req=urllib.request.Request(url, headers={'User-Agent' : "Magic Browser"})
        page = urllib.request.urlopen( req )
        soup=BeautifulSoup(page.read(),"html.parser")
        users=soup.find_all('div',{'class','d-flex hx_hit-user px-0 Box-row'})
        for user in users:
            csvwriter.writerow(getDetails(user))
        pageno+=1
        time.sleep(10)
    out_file.close()