#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Investing.com API - Market and historical data downloader
# https://github.com/crapher/pyinvesting.git
#
# Copyright 2020 Diego Degese
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import pyinvesting as ic

def example_online():
    
    online = ic.Online(
        on_open=on_open, on_close=on_close, on_quotes=on_quotes, 
        on_heartbeat=on_heartbeat, on_error=on_error)
    
    online.connect()
    input("Press Enter to Disconnect...\n")
    online.disconnect()
    
def on_open(online):
    
    print('Connection Opened')

    print('Subscribing to US 30 Contract (With first reading)')
    online.subscribe(pair_id = 8873, ticker = 'US 30 Contract', link = '/indices/us-30-futures')

    print('Subscribing to US 500 Contract (With first reading)')
    online.subscribe(pair_id = 8839, ticker = 'US 500 Contract', link = '/indices/us-spx-500-futures')

    print('Subscribing to US Tech 100 (Without first reading)')
    online.subscribe(pair_id = 8874, ticker = 'US Tech 100')

    print('Subscribing to Small Cap 2000 (Without first reading)')
    online.subscribe(pair_id = 8864, ticker = 'Small Cap 2000')
    
def on_quotes(online, data):
    print(data)
    
def on_close(online):
    print('Connection Closed')

def on_error(online, error):
    print('There was an error. ', error)

def on_heartbeat(online):
#    print('Heartbeat response received from server')
    pass
    
if __name__ == "__main__":
    example_online()