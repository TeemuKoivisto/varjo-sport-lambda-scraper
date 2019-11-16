#!/usr/bin/env bash

init() {
  mkdir tmp
}

crawl() {
  scrapy crawl unisport_spider
}

shell() {
  scrapy shell https://unisport.fi/paikat/unisport-kluuvi
}