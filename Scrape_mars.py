#declare dependencies
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
import requests
from selenium import webdriver
from splinter import Browser


def init_browser():
    executable_path = {"executable_path':'C:/Webdrivers/chromedriver"}
    return Browser('chrome', **executable_path, headless=False)
    

def scrape():
    browser=init_browser()
    
    # NASA Mars News scraping:
    # Visit the NASA Mars news website and parse results HTML with BeautyfulSoup
    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)
    html = browser.html
    soup = bs(html, 'html.parser')

    #find articles
    article=soup.find_all('div', class_='list_text')
    #collect and save latest news title and paragraph 
    news_title = article[3].find('div', class_='content_title').text
    news_p=article[3].find('div', class_='article_teaser_body').text

    # JPL Mars Space Images-- Featured image url scraping
    #create a JPL url and have browser to visit it
    jpl_url='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(JPL_url)

    #use splinter click_link_by_partial_text method to click button
    browser.click_link_by_partial_text('FULL IMAGE')
    #wait time 10 to click once more tome with "more info" button
    time.sleep(10)
    browser.click_link_by_partial_text('more info')

    #parse results html with beautyfulSoup
    html1 = browser.html
    soup1 = bs(html1, 'html.parser')
    rel_img_path=soup1.find('img',class_='main_image').get('src')
    img_url="https://www.jpl.nasa.gov"+rel_img_path

    # Mars Weather
    #create a twitter weather url and have requests to get response from it,parse it to bs4
    mars_weather_url='https://twitter.com/marswxreport?lang=en'
    twitter_response=requests.get(mars_weather_url)
    soup2=bs(twitter_response.text,'html.parser')

    weather_twitter=soup2.find('div', class_="js-tweet-text-container")
    mars_weather=weather_twitter.find('p','tweet-text').text

    # Mars Facts
    #Visit the Mars Facts webpage and use Pandas to scrape the table containing facts
    facts_url='https://space-facts.com/mars/'
    mars_facts_df=pd.read_html(facts_url)[0]
    mars_facts_df.columns=['Description','Value']
    facts_df=mars_facts_df.set_index('Description')
    

    #Use Pandas to convert the data to a HTML table string.
    facts_html=facts_df.to_html()

    #  Mars Hemospheres
    #visit the USGS Astrogeology site to obtain high resolution images for each of Mar's hemispheres.
    Hemisph_url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(Hemisph_url)

    Hemisph_html=browser.html
    Hemisph_soup=bs(Hemisph_html,'html.parser')

    #seach for titles for all four hemisphares and store them in a list
    hemisph_names=[]
    results=Hemisph_soup.find('div',class_='collapsible results')
    hemisphs=results.find_all('h3')
    for title in hemisphs:
        hemisph_names.append(title.text)

    #Mac user: set Executable Path and InitialChrome Browser
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    image_urls=[]

    for name in hemisphere_names:
        #visit the USGS Astrogeology site to obtain high resolution images for each of Mar's hemispheres.
        hemisphere_url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(Hemisph_url)

        #search for each image url
        #use splinter click_link_by_partial_text method to click button
        browser.click_link_by_partial_text(name)
        #wait time 25 to click once more tome with "more info" button
        time.sleep(25)
        #visit the site to obtain high resolution images for each of Mar's hemispheres.
        html_1 = browser.html
        soup_1 = bs(html_1, 'html.parser')
        #seaerch for anchor tag and pull the image with "full" in the name
        image_url1=soup_1.find('div', class_='downloads').find('a')['href']
        image_urls.append({"title":name,"img_url":image_url1})


    #store data in a Python dictionary containing all of the scraped data
    mars_data={
    "news_title":news_title,
    "news_paragraph":news_p,
    "featured_image":img_url,
    "weather":mars_weather,
    "facts":facts_html,   
    "hemispheres":image_urls
    }
    
    # close the browser after scrape
    browser.quit()
    
    return mars_data
