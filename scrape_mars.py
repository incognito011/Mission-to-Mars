from splinter import Browser
from bs4 import BeautifulSoup

import pandas as pd
import time
import requests


# Initialize browser
def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver, below path is for MacOS
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser("chrome", **executable_path, headless=False)


def scrape_news():
    # Initialize browser
    browser = init_browser()
    
    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    
    # Create BeautifulSoup object; parse with 'html.parser'
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Close browser
    browser.quit()
    
    # Collect the latest Mars News Title and Paragraph Text and store into variables
    news_title = soup.find("div", class_="content_title").text
    news_p = soup.find("div", class_="article_teaser_body").text
    
    # Store in dictionary
    news = {
        "news_title": news_title,
        "news_p": news_p,
        
    }

    # Return results
    return news


def scrape_jpl():

    # Initialize browser
    browser = init_browser()
    
    # Setup URL to JPL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Move browser to featured image page
    time.sleep(5)
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(5)
    browser.click_link_by_partial_text('more info')
    time.sleep(5)
    
    # Create BeautifulSoup object; parse with 'html.parser'
    jpl_html = browser.html
    soup = BeautifulSoup(jpl_html, 'html.parser')

    # Get featured image
    img_url = soup.find('img', class_='main_image')['src']
    jpl_url = "https://www.jpl.nasa.gov"
    featured_image_url = jpl_url + img_url

    # Close browser
    # browser.quit()
    
    jpl = {
        "featured_image_url": featured_image_url,
        
    }
     # Return results
    return jpl


def scrape_weather():
    
    # Setup URL to Mars Weather Twitter Account
    url = 'https://twitter.com/marswxreport?lang=en'

    # Retrieve page with the requests module
    response = requests.get(url)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find latest tweet and save it
    mars_weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    
    weather = {
          "mars_weather": mars_weather,
        
        }
    
    return weather


def scrape_facts():
    
     # Setup URL to Mars Facts webpage
     url = 'https://space-facts.com/mars/'

     # Scrape any table data from a page
     tables = pd.read_html(url)
     
     # Create dataframe from scraped data
     df = df = tables[0]
     df.columns = ['Description', 'Value']
     
     # Set the index to the Description column
     df.set_index('Description', inplace=True)
     
     # Convert dataframe to html table
     html_table = df.to_html()
     
     # Clean up html table
     html_table_clean = html_table.replace('\n', '')
    
     facts = {
        "mars_facts": html_table_clean,
        
        }
     
     return facts

 
# Define function to collect data from all title links
def scrape_usgs(link):
    
        # Initialize browser
        browser = init_browser()
        # Setup URL to usgs
        url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(url)
        
        # Move browser to featured image page
        browser.click_link_by_partial_text(link)
        time.sleep(5)
        
        # Create BeautifulSoup object; parse with 'html.parser'
        usgs_html = browser.html
        soup = BeautifulSoup(usgs_html, 'html.parser')
        
        # Get usgs image
        img_url = soup.find('img', class_='wide-image')['src']
        usgs_url = "https://astrogeology.usgs.gov"
        usgs_image_url = usgs_url + img_url
        
        # Create a dictionary to return 
        d = dict();
        
        d['title'] = link
        d['img_url'] = usgs_image_url
       
        # Close browser
        browser.quit()
        
        # Return data dict to main program
        return d

    
def scrape_hemisphere():
    # URL of page to be scraped
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    # Retrieve page with the requests module
    response = requests.get(url)
    
    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all title links featured    
    results = soup.find_all("div", class_="description")
    
    # Empty list of image urls
    hemisphere_image_urls = []
 
    # Loop through all title links and collect data
    for result in results:
        temp = scrape_usgs(result.text)
        hemisphere_image_urls.append(temp)
        time.sleep(5)
        
    hemi = {
        "mars_hemisphere": hemisphere_image_urls,
        
        }
    return hemi
