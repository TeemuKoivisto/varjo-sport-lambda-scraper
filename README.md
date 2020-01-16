# [Varjo Sport Lambda Scraper](https://varjosport.net)

Scrapes the basic info (mainly business hours) of all Unisport gyms.

Why you ask? Because as of now you can't view them all on one page and they are two clicks away from the frontpage. Who designed such retarded system, I don't know, but to me it's annoying since I have no interest in other stuff than seeing how long its open today.

# How to run the scraper locally

Requires Python >=3.6 with preferably virtualenv. I use `virtualenv-wrapper`, some have said `pyenv` is pretty good too.

1. Activate your virtualenv eg `workon varjos`
2. Install dependencies: `pip install -r requirements.txt` ([Scrapy](https://scrapy.org/) and Twisted)
3. Load the dev commands: `. cmds.sh`
4. Run the spider: `crawl`

You should get `./frontend/unisport_gyms.json` file with the data scraped.

Use `shell` to open [interactive Scrapy shell](https://docs.scrapy.org/en/latest/topics/shell.html) to test CSS selectors without having to run the spider.

# How to run the test server

Requires Node.js >=10.

1. Run: `node server.js`
2. The server should run at http://localhost:4040/

Reload the page after making changes to the files inside `frontend`-folder.

# How to deploy the fronted

Requires AWS account and one S3 bucket.

1. Set the bucket's permissions to allow public bucket access and enable static website hosting
2. Configure your local AWS user with access to that bucket
3. You should replace the bucket name in my `cmds.sh` script with your own
4. Then deploy the code with `AWS_PROFILE=varjosport.net-ci deploy_front` where AWS_PROFILE is your local AWS profile.

Go to the bucket's website URL to see the app running eg http://varjosport.net.s3-website.eu-north-1.amazonaws.com

If you want to deploy it to your own domain incase this one dies out for some reason, you have to configure Route 53, Certificate Manager, and CloudFront too. Pretty basic configuration, so I didn't bother writing it down as a template.

# How to run the serverless lambda

Requires Node.js >=10. Docker if you want to deploy it. AWS account with one local AWS user with admin privileges (I'm lazy) and one S3 bucket (the same bucket you use to host the frontend). 

1. Install dependencies: `npm i`
2. Run `npm run invoke` to execute the lambda. It will most probably fail because I hard-coded the profile and the bucket. Change them to your own
3. Similar to the previous command, `npm run deploy` will deploy the lambda but I've hard-coded the parameters

Once deployed, instead of waiting 24 hours for the lambda to run, you can trigger it manually by going to your AWS console's Lambda page for this function and creating & sending a test event.