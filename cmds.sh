#!/usr/bin/env bash

crawl() {
  scrapy crawl unisport_spider
}

shell() {
  scrapy shell https://unisport.fi/paikat/unisport-kluuvi
}

# Remember to use AWS_PROFILE=x with this command
deploy_front() {
  # Copy the build into bucket and delete all existing files excluding unisport.json
  aws s3 sync ./frontend s3://varjosport.net \
    --region eu-north-1 \
    --acl public-read \
    --cache-control max-age=0 \
    --delete \
    --exclude unisport_gyms.json \
    --exclude unisport_events.json
}
