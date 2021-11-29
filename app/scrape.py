# Import Splinter, Pandas and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt


def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph=mars_news(browser)
    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": mars_hemispheres,
        "last_modified": dt.datetime.now()
    }
    # Stop webdriver and return data
    browser.quit()
    return data


# Creating function to obtain data from site
def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    
    # Add try/except for error handling
    try:

        slide_elem = news_soup.select_one('div.list_text')

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
    
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    
    except AttributeError:
        return None, None

    return news_title, news_p

# ## JPL Space Images Featured Image

#Defining function for image browser
def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url


# ## Mars Facts

# Defining function for obtaining dataframe for facts
def mars_facts():
    try:
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")


### Challenge Code
def mars_hemispheres(browser):
    # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # 2. Create a list to hold the images and titles.
    hemisphere_site = []
    hemisphere_title= []
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    html_hem = browser.html
    hems_soup = soup(html_hem, 'html.parser')

    # Finding url for the hemispheres images
    for hem_links in hems_soup.find_all('a', class_='itemLink', href=True):
        hem_link=hem_links['href']
        hem_url = f'https://marshemispheres.com/{hem_link}'
        if hem_url not in hemisphere_site and hem_link is not "#":
            hemisphere_site.append(hem_url)

    # Visiting sites and retrieving image link and title
    for link in hemisphere_site:
        browser.visit(link)
        html_hem_img = browser.html
        hem_img_soup = soup(html_hem_img, 'html.parser')
        img_url_rel =  hem_img_soup.find('a', text='Sample').get('href')
        hem_url= f'https://marshemispheres.com/{img_url_rel}'
        hemisphere_image_urls.append(hem_url)
        img_title =  hem_img_soup.find('h2',class_='title').string
        hemisphere_title.append(img_title)

    # Creating dictionary to hold images links and titles
    hemisph_dict = {}
    for url in hemisphere_image_urls:
        for title in hemisphere_title:
            hemisph_dict[url] = title
            hemisphere_title.remove(title)
            break
            
    return(hemisph_dict)

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())