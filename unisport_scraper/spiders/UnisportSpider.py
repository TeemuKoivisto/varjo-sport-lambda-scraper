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
  info_texts_fi = {
    'Kluuvi': '',
    'Porthania': 'Pelkkä ryhmäliikunta',
    'Kumpula': '',
    'Meilahti': '',
    'Otaniemi': '',
    'Töölö': 'Itsepalvelu-sali, tarvitset kulkuoikeuspassin asiakaspalvelusta päästäksesi sisälle',
    'Viikki': 'Pelkkä ryhmäliikunta',
  }

  def start_requests(self):
    for i, url in enumerate(self.start_urls):
      yield scrapy.Request(url, self.parse, meta={
        'name': self.start_names[i],
        'orig_url': url,
        'info': self.info_texts_fi[self.start_names[i]],
      })

  def parse(self, response):
    """
    The logic for parsing the gym info from https://unisport.fi
    Because things would be too easy, some gyms have different layout than others.
    Mainly due to the fact some don't have saunas or are special gyms with only limited offerings (Viikki, Porthania).
    Or well, Meilahti is different because whoever made it put the exception hours before the sauna hours, for some reason.
    """
    div = response.css('.field--field_opening_hours')
    name = response.meta['name']
    if div:
      if name == 'Meilahti':
        gym_dict = self.parse_meilahti(div, response)
      elif name == 'Töölö':
        gym_dict = self.parse_toolo(div, response)
      elif name == 'Otaniemi':
        gym_dict = self.parse_otaniemi(div, response)
      elif name == 'Viikki':
        gym_dict = self.parse_viikki(div, response)
      else:
        gym_dict = self.parse_normal(div, response)
      yield UnisportGymItem(gym_dict)
  
  def parse_normal(self, div, response):
    return {
      'name': response.meta['name'],
      'orig_url': response.meta['orig_url'],
      'info': response.meta['info'],
      'normal_hours_header': strip(div.css('div > h4 ::text').extract_first()),
      'normal_hours': strip_list(div.css('div > p:nth-child(2) ::text').extract()),
      'sauna_hours': strip_list(div.css('div > p:nth-child(5) ::text').extract()),
      'exception_hours': strip_list(div.css('div > p:nth-child(7) ::text').extract()),
    }
  
  def parse_toolo(self, div, response):
    return {
      'name': response.meta['name'],
      'orig_url': response.meta['orig_url'],
      'info': response.meta['info'],
      'normal_hours_header': strip(div.css('div > h3 ::text').extract_first()),
      'normal_hours': strip_list(div.css('div > p:nth-child(1) ::text').extract())[1:],
      'sauna_hours': ['Ei saunaa'],
      'exception_hours': ['Aina auki'],
    }

  def parse_meilahti(self, div, response):
    return {
      'name': response.meta['name'],
      'orig_url': response.meta['orig_url'],
      'info': response.meta['info'],
      'normal_hours_header': strip(div.css('div > h4 ::text').extract_first()),
      'normal_hours': strip_list(div.css('div > p:nth-child(2) ::text').extract()),
      'sauna_hours': strip_list(div.css('div > p:nth-child(7) ::text').extract()),
      'exception_hours': strip_list(div.css('div > p:nth-child(5) ::text').extract()),
    }

  def parse_otaniemi(self, div, response):
    return {
      'name': response.meta['name'],
      'orig_url': response.meta['orig_url'],
      'info': response.meta['info'],
      'normal_hours_header': strip(div.css('div > h4 ::text').extract_first()),
      'normal_hours': strip_list(div.css('div > p:nth-child(2) ::text').extract()),
      'sauna_hours': ['Ei saunaa'],
      'exception_hours': strip_list(div.css('div > p:nth-child(5) ::text').extract()),
    }

  def parse_viikki(self, div, response):
    return {
      'name': response.meta['name'],
      'orig_url': response.meta['orig_url'],
      'info': response.meta['info'],
      'normal_hours_header': strip(div.css('div > h4 ::text').extract_first()),
      'normal_hours': strip_list(div.css('div > p:nth-child(2) ::text').extract()),
      'sauna_hours': ['Ei saunaa'],
      'exception_hours': ['Auki tuntien mukaan'],
    }