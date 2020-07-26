# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 18:11:29 2020

@author: Root
"""

from selenium import webdriver
from time import sleep
#import csv
import pandas as pd
#import itertools
class Smotri_i_uchis_parser(object):
    
    def __init__(self, browser):
        self.browser = browser
        
    
    def to_csv(self, arg1, arg2, arg3, arg4, arg5, arg6, arg7):
        
        df = pd.DataFrame({'course': arg1, 'link': arg2, 'coach': arg3, 'social': arg4, 'students': arg5, 'reviews': arg6, 'prices': arg7})
        
        df.to_excel(r'C:\Users\Root\Desktop\parser\parser\vse-kursy.xlsx', encoding='utf-8-sig')
        
    
    def parse(self):
        self.go_to_course() 
        
    
        
    def go_to_course(self):
        #self.browser.get('https://m.smotriuchis.ru/catalog/all/117')
        self.browser.get('https://smotriuchis.ru/vse-kursy')
        sleep(4)
        
        # titles = self.browser.find_elements_by_class_name('wdgtile_name')
        title_d = []
        hrefs_l = []
        coach_l = []
        social_l = []
        students_l = []
        reviews_l = []
        prices = []
        strings = list(range(1,98))
        
        cross = self.browser.find_element_by_xpath('/html/body/div[23]/div/div')
        
        try:
            cross.click()
        except Exception as e:
            pass
            
        for string in strings:
            hrefs = self.browser.find_elements_by_class_name('wdgtile_href')
             # for title in titles:
             #    title_d.append(title.text)
            
            for href in hrefs:
            
                hrefs_l.append(href.get_attribute('href'))
            
            # //*[@id="pager"]/div[2]/ul/li[102]/a
            
            
            # page = self.browser.find_element_by_xpath('//*[@id="pager"]/div[2]/ul')
            # button_find = page.find_element_by_class_name('active')
            # button = button_find.find_element_by_tag('a')
            # button.click()
            # //*[@id="pager"]/div[2]/ul/li[101]/a
            if string < 10 or string >= 89:
                arrow1 = self.browser.find_element_by_xpath('//*[@id="pager"]/div[2]/ul/li[101]/a')
                arrow1.click()
            else:
                arrow2 = self.browser.find_element_by_xpath('//*[@id="pager"]/div[2]/ul/li[102]/a')
                arrow2.click()
             # titles = self.browser.find_elements_by_class_name('wdgtile_name')
            
        new_hrefs_l = []
        for word in hrefs_l:
            if word not in new_hrefs_l:
                new_hrefs_l.append(word)

        
        bad_hrefs = []
        for i in new_hrefs_l:
                self.browser.get(i)
                try:
                    title = self.browser.find_element_by_class_name('main-title')
                    title_d.append(title.text)
                except:
                    bad_hrefs.append(i)
                    continue
                price = self.browser.find_element_by_xpath('//*[@id="crs-start"]/div[2]/div[1]/div/div[2]/div')
                prices.append(price.text)
                coach = self.browser.find_element_by_class_name('instr-name')
                coach_l.append(coach.text)
                students = self.browser.find_element_by_xpath('//*[@id="crs-infobox"]/div[2]/div[2]/div/div[3]/span')
                students_l.append(students.text)
                reviews = self.browser.find_element_by_xpath('//*[@id="crs-infobox"]/div[2]/div[2]/div/div[4]/span')
                reviews_l.append(reviews.text)
                coach_link_find = self.browser.find_element_by_xpath('//*[@id="crs-instr"]/div[2]/div[2]/a')
                coach_link = coach_link_find.get_attribute('href')
                self.browser.get(coach_link)
                social_local = []
                
                try:
                    social = self.browser.find_element_by_xpath('//*[@id="profile"]/div/div[1]/div/div[3]/div[3]/div')
                    social_tag = social.find_elements_by_tag_name('a')
                    for s in social_tag:
                        ab = s.get_attribute('href')
                        social_local.append(ab)
                    social_l.append(social_local)
                    social_local = []
                except:
                    social_l.append('-')
        
        for w in bad_hrefs:
            while w in new_hrefs_l:
                new_hrefs_l.remove(w)
        #data = list(zip(title_d, new_hrefs_l, coach_l, social_l))
        
        # data_1 = title_d
        # data_2 = new_hrefs_l
        # data_3 = coach_l
        # data_4 = social_l
        #datas = {'Title': title_d, 'Course_name': new_hrefs_l, 'Name': coach_l, 'Soc_net': social_l}
        #export_data = zip_longest(*datas, fillvalue = '')
        # print(title_d, new_hrefs_l, coach_l, social_l, students_l, reviews_l)
        # print(bad_hrefs)
        self.to_csv(title_d, new_hrefs_l, coach_l, social_l, students_l, reviews_l, prices)
        #self.to_csv(data)
        #data = dict(zip(title_d, new_hrefs_l, coach_l, social_l))  
            
        
        
        
                    

def main():
    #browser = webdriver.Chrome()
    
    chromebrowser = r"C:\Users\Root\Desktop\parser\chromedriver.exe"
    chrome_option = webdriver.ChromeOptions()
    chrome_option.add_argument("headless")
    chrome_option.add_argument('--no-sandbox')
    browser = webdriver.Chrome(executable_path=chromebrowser, chrome_options=chrome_option)
    browser.set_window_size(1920, 1080, browser.window_handles[0])
    parser = Smotri_i_uchis_parser(browser)
    parser.parse()
    
    browser.close()
    
    
if __name__ == "__main__":
    main()