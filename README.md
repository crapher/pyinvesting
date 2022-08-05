
# Investing.com® API - Market and historical data downloader

[![PyPI pyversions](https://img.shields.io/badge/python-3.6+-blue.svg?style=flat
)](https://pypi.org/project/pyinvesting) [![PyPI version shields.io](https://img.shields.io/pypi/v/pyinvesting.svg?maxAge=60)](https://pypi.org/project/pyinvesting) [![PyPI status](https://img.shields.io/pypi/status/pyinvesting.svg?maxAge=60)](https://pypi.org/project/pyinvesting) [![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)  [![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://paypal.me/ddegese) [![Tweeting](https://img.shields.io/twitter/follow/diegodegese.svg?style=social&label=Follow&maxAge=60)](https://twitter.com/diegodegese)

pyinvesting is an API to download online and historical data from investing.com.

-----
## Quick Start

### Search Module

The search module is used to search all the information related to a specific ticker.

The information that can be retrieved is:
- Tickers: It will be used by the rest of the modules to get online or historical data
- News: They are all the news related to a specific search.
- Articles: They are all the articles related to a specific search.

The file **[example_search.py](https://github.com/crapher/pyinvesting/blob/master/examples/example_search.py)** shows a basic example of how to use the module.

### Online Module

The online module handles the connection and subscription with the server and allows a client to subscribe to investing.com and receive all the change events.

The file **[example_online.py](https://github.com/crapher/pyinvesting/blob/master/examples/example_online.py)** shows a basic example of how to use the module.

### History Module

The history module is used to download historical data.
This module allows downloading data from 2 different places (chart and advanced chart sources)

The file **[example_history.py](https://github.com/crapher/pyinvesting/blob/master/examples/example_history.py)** shows a basic example of how to use the module.

## Requirements

* [Python](https://www.python.org) >= 3.6+
* [Pandas](https://github.com/pydata/pandas) >= 1.0.0
* [Numpy](http://www.numpy.org) >= 1.18.1
* [Requests](http://docs.python-requests.org/en/master) >= 2.21.0
* [Websocket-client](https://github.com/websocket-client/websocket-client) >= 1.0.0
* [PyQuery](https://pythonhosted.org/pyquery) >= 1.2

## Legal

See the file [LICENSE](https://github.com/crapher/pyinvesting/blob/master/LICENSE) for our legal disclaimers of responsibility, fitness or merchantability of this library as well as your rights with regards to use of this library.  **pyinvesting** is licensed under **Apache Software License**.

## Attributions and Trademarks

investing.com is trademark of Fusion Media Limited.