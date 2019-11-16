import scrapy
import re

from unisport_scraper.items import UnisportGymItem

def strip(text):
  return text.strip() if text else ''

def strip_list(l):
  return [strip(x) for x in l]

class UnisportSpider(scrapy.Spider):
  name = 'unisport_spider'
  start_urls = [
    'https://unisport.fi/paikat/unisport-kluuvi',
    'https://unisport.fi/paikat/unisport-porthania',
    'https://unisport.fi/paikat/unisport-kumpula',
    'https://unisport.fi/paikat/unisport-meilahti',
    'https://unisport.fi/paikat/unisport-otaniemi',
    'https://unisport.fi/paikat/unisport-toolo',
    'https://unisport.fi/paikat/unisport-viikki',
  ]
  start_names = ['Kluuvi', 'Porthania', 'Kumpula', 'Meilahti', 'Otaniemi', 'Töölö', 'Viikki']

  def start_requests(self):
    for i, url in enumerate(self.start_urls):
      yield scrapy.Request(url, self.parse, meta={
        'name': self.start_names[i],
        'orig_url': url,
      })

  def parse(self, response):
    div = response.css('.field--field_opening_hours')
    if div:
      gym_dict = {
        'name': response.meta['name'],
        'orig_url': response.meta['orig_url'],
        'normal_hours_header': strip(div.css('div > h4 ::text').extract_first()),
        'normal_hours': strip_list(div.css('div > p:nth-child(2) ::text').extract()),
        'sauna_hours': strip_list(div.css('div > p:nth-child(5) ::text').extract()),
        'exception_hours': strip_list(div.css('div > p:nth-child(7) ::text').extract()),
      }
      yield UnisportGymItem(gym_dict)
    
