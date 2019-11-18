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

deploy_front() {
  # Copy the build into bucket and delete all existing files
  aws s3 sync ./frontend s3://varjosport.net \
    --region eu-central-1 \
    --acl public-read \
    --cache-control max-age=120 \ # Or 0? Kinda useless to cache it for 2 minutes anyway..
    --delete \
    --exclude unisport.json
}
