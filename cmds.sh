#!/usr/bin/env bash

crawl() {
  scrapy crawl unisport_spider
}

shell() {
  scrapy shell https://unisport.fi/paikat/unisport-kluuvi
}

# Use profile 
deploy_front() {
  # Copy the build into bucket and delete all existing files
  # Maybe set max-age to 0? Kinda useless to cache it for 2 minutes anyway..
  aws s3 sync ./frontend s3://varjosport.net \
    --region eu-north-1 \
    --acl public-read \
    --cache-control max-age=0 \
    --delete \
    --exclude unisport.json
}
