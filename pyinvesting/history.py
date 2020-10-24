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
from . import __user_agent__

import requests as rq
import pandas as pd

class History:
    
    def __init__(self, proxy_url=None):
        """
        Class constructor 
        
        Parameters
        ----------
        proxy_url : str, optional
            The proxy URL with one of the following formats:
                - scheme://user:pass@hostname:port 
                - scheme://user:pass@ip:port
                - scheme://hostname:port 
                - scheme://ip:port
            
            Ex. https://john:doe@10.10.1.10:3128
        """
        
        if proxy_url:
            self._proxies = {'http': proxy_url, 'https': proxy_url}
        else:
            self._proxies = None

########################
#### PUBLIC METHODS ####
########################
    def get_chart_data(self, pair_id, interval=300, period=None, count=120):
        """
        Returns a dataframe with the historic quotes for the specified pair_id.
        
        Parameters
        ----------
        pair_id : int
            The pair_id value received in the search ticker query.
        interval : int
            The interval represented by each bar. 
            Valid values (all numeric values are seconds): 60, 300, 900, 1800, 3600, 18000, 86400, week, month
        period : int, optional
            The period to be retrieved.
            Valid values: 1-day, 1-week, 1-month, 3-months, 6-months, 12-months, 5-years, max
            The interval requried for each period is:
            - 1-day : 300
            - 1-week : 1800
            - 1-month : 3600
            - 3-months: 18000
            - 6-months: 18000
            - 12-months: week
            - 5-years: month
            - max: month
        count : int
            How many values will be retrieved.  
            Usually, if this value is over 500 the service will not return any information.
        """
        
        payload = {
            'pair_id': pair_id, 
            'pair_id_for_news': pair_id,
            'chart_type': 'candlestick',
            'pair_interval': interval,
            'candle_count': count if count else 120,
            'events': 'no',
            'volume_series': 'yes',
            'period': period if period else ''
        }
        
        url = 'https://www.investing.com/common/modules/js_instrument_chart/api/data.php?{}'.format(self._get_dict_to_query_string(payload))
        try:
            data = self._get_page_content(url)
        
            cols = ['datetime','open','high','low','close','volume','unknown']
            df = pd.DataFrame(data['candles'], columns = cols)
            df.drop(['unknown'], inplace=True, axis=1)
        
            df.datetime = pd.to_datetime(df.datetime / 1000, unit='s')
        except:
            df = pd.DataFrame()
            
        return df

    def get_adv_chart_data(self, pair_id, timeframe):
        """
        Returns a dataframe with the historic quotes for the specified pair_id.
        
        Parameters
        ----------
        pair_id : int
            The pair_id value received in the search ticker query.
        timeframe : str
            The interval represented by each bar. 
            Valid values: 1M, 5M, 15M, 30M, 60M, 5H, 1D, 1W, 1N
        """
        
        payload = {
            'strSymbol': pair_id, 
            'iTop': 1500,
            'strPriceType': 'bid',
            'strFieldsMode': 'allFields',
            'strExtraData': 'lang_ID=1',
            'strTimeFrame': timeframe
        }
    
        url = 'https://advcharts.investing.com/advinion2016/advanced-charts/1/1/8/GetRecentHistory?{}'.format(self._get_dict_to_query_string(payload))

        try:
            data = self._get_page_content(url)
            df = pd.DataFrame(data['data'])
            df['datetime'] = pd.to_datetime(df.date)
            df = df[['datetime','open','high','low','close','volume']]
        except:
            df = pd.DataFrame()
            
        return df
        
#########################
#### PRIVATE METHODS ####
#########################
    def _get_page_content(self, url):
        
        headers = {
            'User-Agent': __user_agent__, 
            'Referer': 'https://www.investing.com',
            'X-Requested-With': 'XMLHttpRequest',
            'Accept-Encoding': 'gzip, deflate'
        }
                
        response = rq.get(url = url, headers = headers, proxies = self._proxies)
        response.raise_for_status()
        
        return response.json()
        
    def _get_dict_to_query_string(self, dict):
        
        result = ''.join('{}={}&'.format(key, dict[key]) for key in dict)
        return result[0:-1] if len(result) > 0 else ''
            