# Martian Updates Twitter Bot
Twitter Bot posting updates on Mars Curiosity Mission (data pulled from NASA APIs and scraped from NASAs partner agencies using Selenium headless browser).

## https://twitter.com/MartianUpdates

![alt text](https://raw.githubusercontent.com/jakubtober/MartianUpdatesTwitterBot/master/%40MartianUpdates_screenshot.jpg "@MartianUpdates")

### Functionality:

* pulls data from the MARS REMS (Rover Environmental Monitoring Station) instrument (data source CAB: https://cab.inta-csic.es/rems/) and saves it

* pulls last day images from NASA open API (there are 7 cameras on board to use)

* creates (and test if needed) 3 different type of twitter messages, posts one depending on history of what has been already posted during last days and what data is available

* posts twitter messages with or without pictures
