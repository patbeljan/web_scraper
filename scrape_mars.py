from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
from selenium import webdriver
import time

def mars_weather():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome('/Users/PatBeljan/Downloads/chromedriver', chrome_options=options)
    url = 'https://twitter.com/marswxreport?lang=en'

    driver.get(url)

    html = driver.page_source
    soup = bs(html, "html.parser")

    mars_weather = {}
    mars_weather['mars_weather'] = soup.find("p", {"class": "tweet-text"}).text[:168]

    return mars_weather

def mars_nasa_lastest_news():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome('/Users/PatBeljan/Downloads/chromedriver', chrome_options=options)
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

    driver.get(url)

    html = driver.page_source
    soup = bs(html, "html.parser")

    article_information = soup.findAll("div", {"class":["content_title", "article_teaser_body"]})

    articles = []
    for x in range(0,len(article_information),2):
        article_dict = {}
        article_dict['title'] = article_information[x].find('a').text.replace("\n", "")
        article_dict['description'] = article_information[x + 1].text.replace("\n", "")
        articles.append(article_dict)

    return articles[0]

def mars_images():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome('/Users/PatBeljan/Downloads/chromedriver', chrome_options=options)
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    driver.get(url)

    html = driver.page_source
    soup = bs(html, "html.parser")

    url_base = 'https://www.jpl.nasa.gov'

    link_start = str(soup.find("article", {"class": "carousel_item"})).index("url('") + 5
    link_end = str(soup.find("article", {"class": "carousel_item"})).index('jpg') + 3
    image_url_end = str(soup.find("article", {"class": "carousel_item"}))[link_start:link_end]
    final_url = url_base + image_url_end

    mars_image_dict = {}
    mars_image_dict['mars_image_link'] = final_url
    return mars_image_dict


def mars_hemisphere():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome('/Users/PatBeljan/Downloads/chromedriver', chrome_options=options)
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    driver.get(url)

    html = driver.page_source
    soup = bs(html, "html.parser")
    hemisphere_count = len(soup.findAll("div", {"class":"item"}))

    hemisphere_images = []
    for i in range(hemisphere_count):
        xpath = f'/html/body/div[1]/div[1]/div[2]/section/div/div[2]/div[{i+1}]/div/a'
        driver.find_element_by_xpath(xpath).click()
        #time.sleep(2)
        image_link_end = driver.find_element_by_class_name("wide-image").get_attribute("src")
        image_link = image_link_end
        title = driver.find_element_by_class_name("title").text.replace("Enhanced", "").strip()
        mydict = {}
        mydict['title'] = title
        mydict['image_link'] = image_link
        hemisphere_images.append(mydict)
        driver.back()

    return hemisphere_images

def mars_facts_table():
    tables = pd.read_html('https://space-facts.com/mars/')
    mydict = {}
    for x in range(len(tables[0])):
        name = tables[0].iloc[x,0].replace(" ", "_")
        name = name.replace(":", "")
        mydict[name] = tables[0].iloc[x,1]
    return mydict

def main():
    table_data = mars_facts_table()
    weather_data = mars_weather()
    hemisphere_data = mars_hemisphere()
    news_data = mars_nasa_lastest_news()
    images_data = mars_images()
    print(table_data)
    print(weather_data)
    print(hemisphere_data)
    print(news_data)
    print(images_data)

if __name__ == "__main__":
    main()
