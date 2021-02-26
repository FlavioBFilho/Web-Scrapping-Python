#!pip install requests_html
import os
import time
from requests_html import HTMLSession
import pandas as pd
from bs4 import BeautifulSoup as bs
import re

courses = []

for i in range(1,3):
    url = "https://www.udemy.com/pt/courses/development/?p=%d"%(i)

    time.sleep(5)
    session = HTMLSession()
    r = session.get(url, headers={'Accept-Language':'pt-br '})
    r.html.render(timeout=45, wait=10, sleep=10)

    html_render = r.html.html

    r.close()
    session.close()

    soup = bs(html_render, 'html.parser')

    course_divs = soup.find_all('div', class_='list-view-course-card--course-card-wrapper--TJ6ET')
    #print(soup)

    for crs in course_divs:

        crs_name = crs.find('div', class_="list-view-course-card--title--2pfA0")
        crs_name = crs_name.h4.text

        crs_price = crs.find('div', class_="course-price-text price-text--base-price__discount--1J7vF price-text--black--1qJbH price-text--medium--2clK9 price-text--bold--ldWad")
        crs_price = crs_price.find_all('span')[2].text

        crs_rate = crs.find('div', class_="list-view-course-card--rating--za-yU").span.text

        crs_rtngs = crs.find('span', class_="ml5").text
        regex_syntax = r"\D"
        num = re.sub(regex_syntax, "", crs_rtngs)
        crs_rtngs = int(num)

        course = (crs_name,crs_price,crs_rate,crs_rtngs)
        courses.append(course)

df = pd.DataFrame(courses)

df = df.rename(columns={
    0: 'name',
    1: 'price',
    2: 'rate',
    3: 'ratings'
})

print(df)