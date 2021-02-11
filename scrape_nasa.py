from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    mars = {}

    # Mars News
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    story = soup.find("ul", class_="item_list")
    title = story.find("div", class_="content_title")
    mars["headline"] = title.find("a").get_text()
    mars["paragraph"] = story.find("div", class_="article_teaser_body").get_text()

    # JPL Image
    url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    image_url= soup.find('img', class_ ="headerimage")['src']

    featured_image_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/' + image_url

    mars['FeaturedImg'].append(featured_image_url)

    # Mars Facts
    url = "https://space-facts.com/mars/"

    tables = pd.read_html(url)
    marsfacts = tables[0]

    html_table = marsfacts.to_html()
    
    mars['MarsFacts'].append(html_table)

    # Mars Hemispheres

    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    item_link = soup.find_all('div', class_='item')

    for x in range(0, len(item_link)):
        print(item_link[x].a['href'])
    hemi_img =[]

    for x in range(0, len(item_link)):
        url = "https://astrogeology.usgs.gov" + item_link[x].a['href']
        browser.visit(url)
        
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        
        metadata = soup.find('section', class_='block metadata')
        img_dl = metadata.dl
        
        hemi_img.append({'img_url': img_dl.a["href"],'title': metadata.find('h2', class_='title').text})
    
    mars['hemispheres'].append(hemi_img)

    browser.quit()

    return mars
