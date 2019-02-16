from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
from urllib.parse import urlencode 

executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
browser = Browser("chrome", **executable_path, headless=True)
mars_data={}
hemisphere_image_urls=[]

def getSoup(url_to_get):
    url=url_to_get
    try:
        browser.visit(url)
        html = browser.html
        soup = bs(html, "html.parser")
        print("Scraping "+url)
        #print(len(html))
        return soup
    except:
        return ""

def getNews():
    #collect the latest News Title and Paragraph Text
    thisSoup=getSoup("https://mars.nasa.gov/news/")
    if thisSoup is None:
        mars_data["news_title"]="unavailable"
        mars_data["news_paragraph"]="unavailable"
    else:
        news_title = thisSoup.find('li', class_='slide').find('a').find('h3').text
        news_paragraph=thisSoup.find('li', class_='slide').find('div', class_="article_teaser_body").text
        mars_data["news_title"]=news_title
        mars_data["news_paragraph"]=news_paragraph


def getFeaturedImg():
    thisUrl="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    thisSoup=getSoup(thisUrl)
    if thisSoup is None:
        mars_data["featured_img_url"]="unavailable"
    else:
        featured_img=thisSoup.find('section',class_='centered_text clearfix main_feature primary_media_feature single').find('article',class_="carousel_item")
        featured_img_url=featured_img.get('style')
        featured_img_url=thisUrl[:24]+featured_img_url[23:-3]
        mars_data["featured_img_url"]=featured_img_url


def getWeather():
    thisSoup=getSoup("https://twitter.com/marswxreport?lang=en")
    if thisSoup is None:
        mars_data["mars_weather"]="unavailable"
    else:
        for div in thisSoup.find_all('div',attrs={'data-name':'Mars Weather'}):
            tweet= div.find('p', class_='tweet-text')
            if tweet and tweet.text.find('Sol ')!= -1:
                mars_weather= tweet.text.strip().replace('\n',' ')            
                mars_weather=mars_weather[:mars_weather.find("pic")]
                break
        mars_data["mars_weather"]=mars_weather

def getFacts():
    table_df=pd.read_html("http://space-facts.com/mars/")
    df=table_df[0]
    df.columns=["Fact","Value"]
    df.columns.index=["Fact"]
    htmlStr=df.to_html()
    if htmlStr:
        mars_data["facts"]=htmlStr
    else:
        mars_data["facts"]="unavailable"

def gethemispheres():
    hemispheresUrls=[]
    base_url="https://astrogeology.usgs.gov"
    thisSoup=getSoup("https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars")
    if thisSoup is None:
        mars_hemis_data["hemispheres"]="unavailable"
    else:
        items=thisSoup.find_all('div', class_='item')
        for i in items: 
            alls=i.find_all('a', class_='itemLink product-item') 
            for a in alls:
                hemispheresUrls.append(a.get('href'))
        unurls=set(hemispheresUrls)    # get unique list of urls, one for each hemisphere
        for u in unurls: 
            #hemispheresUrls.append(base_url+u)
            htitle= str.title(u[25:].replace('_',' '))
            hemisurl=base_url+u
            hemisSoup=getSoup(hemisurl)
            hemislink=hemisSoup.find('div', class_="wide-image-wrapper ").find_all('a')[1].get('href')
            mars_data[htitle]=hemislink



def scrape():
    getNews()
    getFeaturedImg()
    getWeather()
    getFacts()
    gethemispheres()
    return mars_data
    



#EOF  ###