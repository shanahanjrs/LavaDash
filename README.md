# DEPRECATED

> This project is being open sourced while we work on other projects.
> 
> Project owners:
> 
> @shanahanjrs
> 
> @tysongg
> 
> @aglovaile


### Dir structure

**analyzer/**
> Sentiment Analysis Engine

**scraper/**
> Scrapes Reddit, Twitter, and News for specific search terms

**analysis_utils/**
> Contains general-use util functionality for all internal microservices

**lavadash-ui/**
> Contains all the Django code for the Lavadash website

**ci/**
> Continuous Integration


### Build

> Build everything

`./build.sh`

> Build a single service

`docker-compose build <service name>`


### Run

`./run.sh`


### Helpful links

- Home page: http://localhost:8000/
- Chronograf: http://localhost:8888/sources/0/admin-influxdb/databases
- Grafana: http://localhost:3000/?orgId=1
- Add a search term if Redis is empty on start: http://127.0.0.1:5100/search/terms/military

### Data Flow

- Every N second we pull all the terms we want to scrape from Redis (Redis.Set.scraperTerms)
  and Publish them to a pub/sub queue *(toScrape)* for the *scraper* service.
- TODO: Add the SPAM FILTERING step here...
- When the *scraper* service picks up terms from the *toScrape* queue we will scrape Twitter,
  Reddit, and top news headlines then Publish the results in a pub/sub queue *(toAnalyze)*
  for the *analysis* service.
- When the *analysis* service picks up scrape-results from the *toAnalyze* queue it will perform
  the standard Sentiment Analysis + others (in the future) and store the results in a Time Series DB.

### TODO
- https://trello.com/b/mJoT74nQ/dev-board
