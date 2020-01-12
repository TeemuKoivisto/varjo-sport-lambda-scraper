
# Haha. Häx
# https://stackoverflow.com/questions/44058239/sqlite3-error-on-aws-lambda-with-python-3
import imp
import sys
sys.modules["sqlite"] = imp.new_module("sqlite")
sys.modules["sqlite3.dbapi2"] = imp.new_module("sqlite.dbapi2")

import os
# import datetime
import logging
from multiprocessing import Process, Pipe

import boto3

from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

# TODO enable this
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.WARNING)

def crawl_unisport(event, context):
  # TODO this loggings don't work probably because of the Pipes & Processes below
  # start = datetime.datetime.utcnow()
  # logger.info('Crawling started: {}'.format(datetime.datetime.now().time()))

  configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})

# Well this is just insane. But oh well it works. (I hope)
# https://stackoverflow.com/questions/41495052/scrapy-reactor-not-restartable
# https://aws.amazon.com/blogs/compute/parallel-processing-in-python-with-aws-lambda/
  def f(q):
    try:
      runner = CrawlerRunner(get_project_settings())
      deferred = runner.crawl('unisport_spider')
      deferred.addBoth(lambda _: reactor.stop())
      reactor.run()
      input_p.send(None)
    except Exception as e:
      input_p.send(e)

  output_p, input_p = Pipe()
  p = Process(target=f, args=((output_p, input_p),))
  p.start()
  p.join()

  # end = datetime.datetime.utcnow()
  # logger.info('Crawling took {} h:m:s:ms'.format(str(end - start)))