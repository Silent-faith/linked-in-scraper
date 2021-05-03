import pandas as pd 
import numpy as np 
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs


"""

logging into the linked in profile 


"""



username = "abhishekmahala28@gmail.com"
password = input()

driver = webdriver.Chrome('C:/Users/Abhishek Choudhary/.spyder-py3/chromedriver.exe')
driver.get("https://www.linkedin.com/")

username_input = driver.find_element_by_css_selector("input[name = 'session_key']")
password_input = driver.find_element_by_css_selector("input[name='session_password']")
            
username_input.send_keys(username)
password_input.send_keys(password)
            
login_button =  driver.find_element_by_xpath("//button[@type='submit']")
login_button.click()

"""

    reading the company data from the spreadsheet 

"""

Data = pd.read_csv("Vaccine_Data.csv")
Data = np.array(Data.iloc[:,:].values)



df = [] 
for i in range (1, len(Data), 2) :
    
    try : 
        Name_of_company = Data[i][1]
        
        Link_of_company = Data[i][3]
        
        
        """
            
            now going to the company page 
        
        """
        
        driver.get(Link_of_company)
        
        search_parameter1 =  "&origin=FACETED_SEARCH&title=manager"
        search_parameter2 = "&origin=FACETED_SEARCH&title=Chief"
        
        sleep(2)
        source = driver.page_source
        data=bs(source, 'html.parser')
        
        data = data.find('div', class_ = "display-flex mt2 mb1")
        data = data.find('a')
        
        link  = data.get('href')
        
        link = "https://www.linkedin.com" + link 
        
        link_of_people_data = link.split("&")
        
        link = link_of_people_data[0] + search_parameter1
        
        """
        
            now going to the companys people according to the searchrequirements 
        
        """
        
        try : 
        
            driver.get(link)
            
            sleep(2) 
            
            data  = bs(driver.page_source, 'html.parser') 
            
            data = data.find_all('li', class_ = "reusable-search__result-container")
            
            print(len(data))
            
            #print(data[1].prettify())
            for i in range (len(data)) : 
                
                item = data[i]
                
                try : 
                    
                    try : 
                        item_data = item.find('span', class_ = "visually-hidden").text.split()
                        name = ""
                        for i in range (1, len(item_data)-1) :
                            name += item_data[i] + " "
                        name = name[:-3]
                    except :
                        name = "out of network"
                    
                    #print("name : ", name)
                    link_of_person = item.find('a').get('href')
                    
                    job_destination = item.find('div', class_ = "entity-result__primary-subtitle t-14 t-black").text
                    
                    ans = [name, Name_of_company, job_destination, Link_of_company, link_of_person ]
                    df.append(ans)
                except :
                    print(i)
                    
            
            """
                for search parameter 2 
            """
            link = link_of_people_data[0] + search_parameter2
            
            """
            
                now going to the companys people according to the searchrequirements 
            
            """
            
            driver.get(link)
            
            sleep(2) 
            
            data  = bs(driver.page_source, 'html.parser') 
            
            data = data.find_all('li', class_ = "reusable-search__result-container")
            
            print(len(data))
            
            #print(data[1].prettify())
            for i in range (len(data)) : 
                
                item = data[i]
                
                try : 
                    
                    try : 
                        item_data = item.find('span', class_ = "visually-hidden").text.split()
                        name = ""
                        for i in range (1, len(item_data)-1) :
                            name += item_data[i] + " "
                        name = name[:-3]
                    except :
                        name = "out of network"
                    
                    link_of_person = item.find('a').get('href')
                    
                    job_destination = item.find('div', class_ = "entity-result__primary-subtitle t-14 t-black").text
                    
                    ans = [name, Name_of_company, job_destination, Link_of_company, link_of_person ]
                    df.append(ans)
                except :
                    print(i)
        except :
            pass
    except :
            pass
         
    #df_intial = pd.read_csv("result.csv")
df = pd.DataFrame(df, columns= ['name_of_person', 'name_of_company', 'job', 'link_of_company', 'linh_of_person']) 
df.to_csv("result.csv")
