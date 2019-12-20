#coding UTF-8

import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
import pandas as pd
from html_table_parser import parser_functions as parser

driver =webdriver.Chrome()
i=1001

font_path = 'c:/Windows/Fonts/H2HDRM.ttf'
font_name = font_manager.FontProperties(fname=font_path).get_name()
rc('font',family=font_name)
while True:
    url = 'http://kosis.kr/conts/nsportalStats/nsportalStats_0102Body.jsp?menuId=10&NUM=%d&searchKeyword=&freq=' %i
    driver.get(url)
    driver.switch_to.frame(driver.find_element_by_tag_name('iframe'))
    html = driver.page_source
    result = BeautifulSoup(html, 'html.parser')
    
    try:
        tag = result.find_all("table", class_="Tb")[0]
        
    except IndexError:
        driver.close()
        break
        
    html_table = parser.make2d(tag)
    df = pd.DataFrame(html_table[2:], columns=html_table[0])
    df_2=df.drop(df.columns[0], axis=1)
    for a in df_2.columns:
        df_2[a]=df_2[a].str.replace(',','')
    df_2=df_2.set_index(df.iloc[:,0])
    df_2=df_2.apply(pd.to_numeric)
    print(df_2)
    print(df_2.describe())
    print(df_2.dtypes)
    df_2.T.plot.bar()
    plt.show()
    i=i+df.shape[0]
