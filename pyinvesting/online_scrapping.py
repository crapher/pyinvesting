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

from pyquery import PyQuery as pq

import re
import requests as rq
import pandas as pd
import numpy as np

import threading
import time
import json

class OnlineScrapping:
    
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
        
        self._stream_server = None
        self._stream_server_lock = threading.Lock()
    
########################
#### PUBLIC METHODS ####
########################
    def get_stream_server(self):
        """
        Returns a stream server to be used for the websocket to retrive quotes.        
        """
        with self._stream_server_lock:
            if not self._stream_server:
                content = self._get_page_content('https://api.investing.com/api/editions/streamer')
                servers = json.loads(content)
                self._stream_server = servers['stream_servers'][0]
                    
        return self._stream_server
            
    def get_quotes_from_link(self, pair_id, link):
        """
        Parses and returns a dataframe with the quotes for the specified pair_id.
        
        Parameters
        ----------
        pair_id : int
            The pair_id value received in the search ticker query.
        link : str
            The link value received in the search ticker query.        
        """
        
        content = self._get_page_content(link)
        
        with self._stream_server_lock:
            if not self._stream_server:
                self._stream_server = self._get_stream_server_from_page(content)
            
        return self._get_quotes_from_page(content, pair_id)

#########################
#### PRIVATE METHODS ####
#########################
    def _get_page_content(self, url):
        
        if url.startswith('/'): # relative URL
            url = 'https://www.investing.com{}'.format(url)
                        
        headers = {
            'User-Agent': __user_agent__,
            'Accept-Encoding': 'gzip, deflate'
        }
                
        response = rq.get(url = url, headers = headers, proxies = self._proxies)
        response.raise_for_status()
        
        return response.text

    def _get_quotes_from_page(self, text, pair_id):
        
        data = {'pair_id': pair_id, 'bid': np.NAN, 'ask': np.NAN, 'last': np.NAN, 'high': np.NAN, 'low': np.NAN, 'pcp': np.NAN, 'turnover': np.NAN, 'pc': np.NAN, 'timestamp': int(time.time())}        
        keys = list(data)
        
        doc = pq(text)
        spans = doc("span[class*='{}']".format(pair_id))
        for span in spans:
            classes = span.attrib['class']
            
            for key in keys:
                if '{}-{}'.format(pair_id, key) in classes:
                    try:
                        data[key] = float(span.text.replace(',','').replace('%','').strip())
                        keys.remove(key)
                    except:
                        pass

                    break
        
        if data['last'] and data['pc']:
            data['pc'] = data['last'] - data['pc']
        elif data['pc']: # There is no last value
            data['pc'] = np.NAN

        result = pd.DataFrame(data, index=[0])
        result.columns = ['pair_id', 'bid', 'ask', 'last', 'high', 'low', 'change', 'turnover', 'previous_close', 'timestamp']
        result['datetime'] = pd.to_datetime(result['timestamp'], unit='s')
        result = result[['pair_id', 'bid', 'ask', 'last', 'high', 'low', 'change', 'turnover', 'previous_close', 'datetime']]
        
        return result
