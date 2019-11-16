import scrapy
import re

from unisport_scraper.items import UnisportGymItem

class UnisportSpider(scrapy.Spider):
  name = 'unisport_spider'
  start_urls = [
    'https://unisport.fi/paikat/unisport-kluuvi'
  ]
  start_names = ['kluuvi']

  def start_requests(self):
    for i, url in enumerate(self.start_urls):
      yield scrapy.Request(url, self.parse, meta={'name': self.start_names[i]})

  def parse(self, response):
    for div in response.css('.field--field_opening_hours > div'):
      gym_dict = {
        'name': response.meta['name'],
        'body': div.css('p ::text').extract_first().strip(),
      }
      yield UnisportGymItem(gym_dict)
    
