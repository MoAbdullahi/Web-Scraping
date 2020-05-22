import scrapy
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

class Stations(scrapy.Spider):
    name = "station"
    start_urls = [
        'https://www.brandstof-zoeker.nl/',
    ]

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)

    def parse(self, response):
        self.driver.get(response.url)
        while True:
            data = self.driver.find_elements_by_xpath('//li[starts-with(@id, "station")]/ul/li[1]')
            num_page_items = len(data)
            for i in range(num_page_items):
                address = data[i].text.split(",")[0]
                city    = data[i].text.split(",")[1]
                yield {"address": address, "city":city}
            try:
                response = response.replace(body=self.driver.page_source)
            except TimeoutException:break
