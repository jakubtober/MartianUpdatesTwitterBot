# Martian Updates Twitter Bot
Twitter Bot posting updates on Mars Curiosity Mission (data pulled from NASA APIs and scraped from NASAs partner agencies using Selenium).

## https://twitter.com/MartianUpdates

### Functionality:

* pull data from the MARS REMS (Rover Environmental Monitoring Station) instrument (data source CAB: https://cab.inta-csic.es/rems/) and save it

* pull last day images from NASA open API (for different cameras - there are 7 cameras on board to use)

* create (and test if needed) twitter messages, 3 different types depending on history of what has been already posted during last days and what data is available

* post twitter messages with or without pictures
