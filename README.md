# Web Scraping

This application retrieves data from 4 Nasa sites to gather information about Mars .

scrape_mars.py :
  Beautiful soup is used to retrieve and filter html data.
  Pandas is used get/keep html data. 
  
app.py:
  Flask application, calls scrape_mars.py, stores data in local mongoDb and defines routes.

static / templates /index.html : web display

page1.png, page2.png : Images of application running. 



