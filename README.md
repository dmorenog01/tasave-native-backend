# TasaVE Native Backend

This repository contains two directories: api and scrapers.

You can also access the repo for the React Native app [here](https://github.com/dmorenog01/tasave-native)

## api
The api directory contains an express api served as a google cloud function with two endpoints:
- /v1/rates: Gets the latest rates from each of the supported currency pairs
- /v1/ping: Returns a 200 response.

A live deployment of the API can be accessed [here](https://api-5uzosi7y6a-uk.a.run.app/v1/rates).

## scrapers
The scrapers directory contains two cloud functions written in Python that are executed on a schedule to scrape exchange rates from each of the supported currencies.

## TODO
- Create endpoint for historic rates
