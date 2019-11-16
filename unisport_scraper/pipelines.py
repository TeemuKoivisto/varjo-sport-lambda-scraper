# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json
import os
import scrapy
from scrapy.exporters import JsonItemExporter
from unisport_scraper.items import UnisportGymItem

SERVERLESS_STAGE = os.environ.get('SERVERLESS_STAGE')

class UnisportJsonPipeline(object):
    def open_spider(self, spider):
        if SERVERLESS_STAGE == 'local':
            os.makedirs('output', exist_ok=True)
            self.file_unisport = open("output/unisport.json", 'wb')
        else:
            self.file_unisport = open("tmp/unisport.json", 'wb')
        self.exporter = JsonItemExporter(self.file_unisport, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()
 
    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file_unisport.close()
 
    def process_item(self, item, spider):
        if isinstance(item, UnisportGymItem):
            self.exporter.export_item(item)
        return item
