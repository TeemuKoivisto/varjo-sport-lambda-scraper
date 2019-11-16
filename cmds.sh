#!/usr/bin/env bash

init() {
  mkdir tmp
}

crawl() {
  scrapy crawl unisport_spider
}
