"""Twitter does not seem to work so well, unless we are really looking at the reaction
of the consumer regarding a product that we already had identified.
Need new methods for scraping:

- Instagram;

- From a magazine/website that shows new products or upcoming products, then make the program
automatically write out the materials (and match it with our portfolio??)
    
    https://mognavi.jp/soft-drink/newitem

    For each site, have a personal format for the dataframe dictionary.
    We want to prevent the scraper from constantly reading in the whole site. Set a type of cache and
    make the program first read whether something has been updated. If updated, only add the new one.
    Then paste this dataframe in a csv/excel sheet?

    Modules needed: requests, bs4, pandas, openpyxl, csv?

    We need a class that holds the url for scraping and also loads in the dataframe of existing data(?)
    Within this class, we have a method that starts scraping the page and grabs all the html.
    Then we also have a method that starts writing the data to a product class that has fixed attr
    depending on which site we are scraping.
    Also a method for writing data to the dataframe/excel sheet. Skips over already written products.

    TIPS:
    - Check the Coursera ABC example
    - What pattern designs could we implement?

    Classes:
        Scraper
        FoodNews
        MogNavi

    A scraper that scrapes on specified pages the products with all its details.
    Once scraped and compiled nicely, it has to be pasted in an excel sheet so that 
    it can be sent to the R&D team for judging what products we could try and make.

"""

import requests
import re
import bs4
import pandas as pd
from dataclasses import dataclass
from urllib.parse import urlsplit
from urllib.parse import unquote

class Scraper:
    def __init__(self, url, data):
        self.url = url
        self.current_data = data  # A dataframe from a pickle
        self.scraped_data = []  # List of Product dataclasses

    def scrape_url(self, url):
        res = requests.get(url)
        res.raise_for_status()
        return bs4.BeautifulSoup(res.text, "html.parser")
    
class FoodNews(Scraper):
    def _get_domain(self, url):
        split_url = urlsplit(url)
        return f"{split_url.scheme}://{split_url.hostname}"

    def __init__(self, url, data):
        super().__init__(url, data)
        self.domain = self._get_domain(self.url)

    def collect_data(self):
        """
        Attributes
        -----------
        page_count : int
            Page number that is part of the url.
        scrape_page : Soup of scraped url.
            Uses fstring to form a proper url with attr "page_count"
            Example: {http://www.foodnews.com/articles/category/24}/{1}"""
        while True:
            page_count = 1
            scrape_page = self.scrape_url(f"{self.url}/{page_count}")

            collected_links = self._collect_links(scrape_page)



            # TODO - make it grab the correct product info and set in dataclass
            # Create private method for this and add under here
            # So that means we are automatically grabbing for each page


            if not collected_links:
                break  # Empty page, end of pages reached

            page_count +=1

        
    def _collect_links(self, scraped_page):
        product_re = re.compile(r"^productList(-smallBox)?$")
        # REDESIGN - NOT READABLE!
        return [str(f"{self.domain}{link.find('a').get('href')}"
                ) for link in scraped_page.find_all(class_=product_re)]

    def _set_product_data(self, links):
        for link in links:
            scrape_page = self.scrape_url(link)
            name = self._format_item(scrape_page, "#clm-mainBody > h1")
            manufacturer = 
            sales_date = 
            category = 
            # etc...

            # unquote(kanji text).encode("latin1").decode("utf-8")
    
    def _format_item(self, scraped_page, item):
        scraped_item = scraped_page.select(item)
        encoded_item = scraped_item[0].text.strip()
        return unquote(encoded_item).encode("latin1").decode("utf-8")



        
        
    





    



    
    pass
    # init has url, data of already existing data, which could be a list of class 'Product'

@dataclass
class Product:
    product_name : str
    manufacturer : str
    sales_date : str
    category : str
    quantity : str
    price : str
    description : str
    image : str
    
    def __lt__(self, object):
        return self.sales_date < object.sales_date




# An ABC for 1 class that defines attributes??

if __name__ == '__main__':
    pass  # initiate the scraper