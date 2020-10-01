## Investing.com® API - Market and historical data downloader

pyinvesting is an API to download online and historical data from Investing.com.

-----
## Quick Start

###Search Module

The search module is used to search all the information related to a specific ticker.

The information that can be retrieved is:
- Tickers: It will be used by the rest of the modules to get online or historical data
- News: They are all the news related to a specific search.
- Articles: They are all the articles related to a specific search.

The file **example_search.py** in the **example** folder shows a basic example of how to use the module.

###Online Module

The online module handles the connection and subscription with the server and allows a client to subscribe to investing.com and receive all the change events.

The file **example_online.py** in the **example** folder shows a basic example of how to use the module.

###History Module

The history module is used to download historical data.
This module allows downloading data from 2 different places (chart and advanced chart sources)

The file **example_history.py** in the **example** folder shows a basic example of how to use the module.
