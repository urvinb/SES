from bs4 import BeautifulSoup
import urllib.request,sys,time
import requests
import pandas as pd
from googlesearch import search


url = 'https://timesofindia.indiatimes.com/'
books_url='https://www.flipkart.com/the-exam-store'
def news():
    try:
        page = requests.get(url)

    except Exception as e:    
        # get the exception information
        error_type, error_obj, error_info = sys.exc_info()      
        
        #print the link that cause the problem
        print ('ERROR FOR LINK:',url)
        
        #print error info and line that threw the exception                          
        print (error_type, 'Line:', error_info.tb_lineno)
        

    print(page.status_code)
    #print(page.text)

def books():
    try:
        page = requests.get(books_url)

    except Exception as e:    
        # get the exception information
        error_type, error_obj, error_info = sys.exc_info()      
        
        #print the link that cause the problem
        print ('ERROR FOR LINK:',url)
        
        #print error info and line that threw the exception                          
        print (error_type, 'Line:', error_info.tb_lineno)
    

    print(page.status_code)
    print(page.text)

def google():
    query = "jee main books"
    my_results_list = []
    for i in search(query,tld = 'com',lang = 'en',num = 10,start = 0,stop = None,pause = 2.0):
        my_results_list.append(i)
        print(i)

no_pages = 2

def get_data(pageNo):  
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}

    #r = requests.get('https://www.amazon.in/gp/bestsellers/books/ref=zg_bs_pg_'+str(pageNo)+'?ie=UTF8&pg='+str(pageNo), headers=headers)#, proxies=proxies)
    r = requests.get('https://www.google.com/search?sxsrf=ALeKk00o37Gz155SeYJ6uRxXgg4ZTedRXw%3A1614467731074&ei=k9I6YPOKBMCc4-EPsM6DiAY&q=books+for+jee+mains&oq=&gs_lcp=Cgdnd3Mtd2l6EAEYBzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzoHCAAQRxCwA1D56wNY-esDYK6HBGgEcAJ4AIAB4QGIAeEBkgEDMi0xmAEAoAEBqgEHZ3dzLXdperABCsgBCMABAQ&sclient=gws-wiz')
    content = r.content
    soup = BeautifulSoup(content,"html.parser")
    print(content)
    #print(soup)

    alls = []
    
    for d in soup.findAll('div', attrs={'class':'a-section a-spacing-none aok-relative'}):
        #print(d)
        #p13n-sc-truncate-desktop-type2 p13n-sc-truncated
        name = d.find('span', attrs={'class':'zg-text-center-align'})
        n = name.find_all('img', alt=True)
        #print(n[0]['alt'])
        author = d.find('a', attrs={'class':'a-size-small a-link-child'})
        rating = d.find('span', attrs={'class':'a-icon-alt'})
        users_rated = d.find('a', attrs={'class':'a-size-small a-link-normal'})
        price = d.find('span', attrs={'class':'p13n-sc-price'})

        all1=[]

        if name is not None:
            #print(n[0]['alt'])
            all1.append(n[0]['alt'])
        else:
            all1.append("unknown-product")

        if author is not None:
            #print(author.text)
            all1.append(author.text)
        elif author is None:
            author = d.find('span', attrs={'class':'a-size-small a-color-base'})
            if author is not None:
                all1.append(author.text)
            else:    
                all1.append('0')

        if rating is not None:
            #print(rating.text)
            all1.append(rating.text)
        else:
            all1.append('-1')

        if users_rated is not None:
            #print(price.text)
            all1.append(users_rated.text)
        else:
            all1.append('0')     

        if price is not None:
            #print(price.text)
            all1.append(price.text)
        else:
            all1.append('0')
        alls.append(all1)    
    return alls

    results = []
    for i in range(1, no_pages+1):
        results.append(get_data(i))
    flatten = lambda l: [item for sublist in l for item in sublist]
    df = pd.DataFrame(flatten(results),columns=['Book Name','Author','Rating','Customers_Rated', 'Price'])
    df.to_csv('amazon_products.csv', index=False, encoding='utf-8')
    df = pd.read_csv("amazon_products.csv")
    print(df.shape())

get_data(1)