# Final Project

## Overview:
+ Data Source: Home Sensor data [.txt files with lists in it]
+ Result of project:
  + ETL - Extracting data from .txt, tranforming those into serilized data and loading into CSV file.
  + Data cleaning - cleaning data and dividing it into different types. Also ignoreing data with unxexpected time occurence.
  + Data Sampling - Resample data and interpolate on montly, weekly and daily bases.
  + API application - created flask application:
    + getDataHour - Gives average data of the hour of a particular day.
    + getDataDay - Gives average data of a particular day.
    + compare temperature: uses above links to get api of homesensor data and api.worldweatheronline.com for historical weather data.
        + compareHour - compare average hour home temperature data with weather that day.
        + compareDay - compare average day home temperature data with weather that day.



## Purpose/Application:

## Execution and Explanation: