from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import pandas as pd
import time

from selenium import webdriver

class Service:
    
    def getComment(self):       
        comment_list = []
        
        for page in range(1, 16):
            url = 'https://gall.dcinside.com/board/lists/?id=hit'
            url += '&page=' + str(page)
            print('>> page: ' + str(page))     
            
            try: 
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
                request = Request(url, headers=headers) 
                response = urlopen(request)
                html = response.read()
                soup = BeautifulSoup(html, 'lxml')
                links = soup.select('#container > section.left_content > article:nth-child(3) > div.gall_listwrap.list > table > tbody > tr')  
                
                for l in links:
                    a_link = l.select_one('td.gall_tit.ub-word > a:nth-child(1)').get('href')  
                    
                    if a_link != 'javascript:;':
                        baseurl = 'https://gall.dcinside.com'
                        url2 = baseurl + a_link
                        print('>> ' + url2)

                        options = webdriver.ChromeOptions() 
                        # options.add_argument('headless') 
                        options.add_argument('disable-gpu') 
                        options.add_experimental_option("excludeSwitches", ["enable-logging"])
                        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4692.99 Safari/537.36, Referrer-Policy=no-referrer, strict-origin-when-cross-origin')
                        driver = webdriver.Chrome('chromedriver', options=options)
                        driver.get(url2)
                        time.sleep(2)

                        soup2 = BeautifulSoup(driver.page_source, 'lxml')
                        comments = soup2.select('#focus_cmt > div.comment_wrap > div.comment_box > ul > li')
                        
                        for c in comments:
                            try: 
                                text = c.find('p', attrs={'class': 'usertxt'}).text
                                if 'dc App' in text:
                                    text = text.split('-')[0].strip('')
                                print(text)
                                comment_list.append(text) 
                            except Exception as e:
                                pass

                        driver.quit()

            except Exception as e:
                pass
        
        data = pd.DataFrame(comment_list, columns=['댓글'])
        data.to_csv('댓글.csv', index = False, encoding='utf-8-sig')


if __name__ == "__main__": 
    s = Service()
    res = s.getComment()