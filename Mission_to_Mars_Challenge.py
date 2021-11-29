#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import Splinter, Pandas and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt


# In[2]:


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[3]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[4]:


html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')


# In[5]:


slide_elem.find('div', class_='content_title')


# In[6]:


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[7]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### Featured Images

# In[8]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[9]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[10]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup


# In[11]:


# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[12]:


# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# In[13]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df


# In[14]:


df.to_html()


#  ### Hemishpheres

# In[15]:


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'
browser.visit(url)


# In[16]:


# 2. Create a list to hold the images and titles.
hemisphere_site = []
hemisphere_title= []
hemisphere_image_urls = []


# In[17]:


# 3. Write code to retrieve the image urls and titles for each hemisphere.
html_hem = browser.html
hems_soup = soup(html_hem, 'html.parser')


# In[18]:


for hem_links in hems_soup.find_all('a', class_='itemLink', href=True):
    hem_link=hem_links['href']
    hem_url = f'https://marshemispheres.com/{hem_link}'
    if hem_url not in hemisphere_site and hem_link is not "#":
        hemisphere_site.append(hem_url)
print (hemisphere_site)


# In[19]:


for link in hemisphere_site:
    browser.visit(link)
    html_hem_img = browser.html
    hem_img_soup = soup(html_hem_img, 'html.parser')
    img_url_rel =  hem_img_soup.find('a', text='Sample').get('href')
    hem_url= f'https://marshemispheres.com/{img_url_rel}'
    hemisphere_image_urls.append(hem_url)
    img_title =  hem_img_soup.find('h2',class_='title').string
    hemisphere_title.append(img_title)
    
print(hemisphere_image_urls)   
print(hemisphere_title)


# In[20]:


hemisph_dict = {}
for url in hemisphere_image_urls:
    for title in hemisphere_title:
        hemisph_dict[url] = title
        hemisphere_title.remove(title)
        break
        
print(hemisph_dict)


# In[ ]:




