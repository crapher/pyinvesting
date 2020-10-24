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
import urllib
import json

class Search():
    
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
    def tickers(self, search_term, limit=30):
        """
        Returns all the tickers found under the search_term.
        
        Parameters
        ----------
        search_term : str
            Term used to filter the tickers
        limit : int
            Maximum results count that will be retrieved
        """
                
        tickers = self._internal_search(search_term.lower(), 'quotes', limit)
        if not tickers.empty:
            tickers.link = tickers.link.apply(lambda x: 'https://www.investing.com{}'.format(x) if x != None and x[0] == '/' else x)
            tickers = tickers[['pairId', 'link', 'symbol', 'exchange', 'name', 'type']]
            tickers.columns = ['pair_id', 'link', 'symbol', 'exchange', 'name', 'type']
            return tickers

        return pd.DataFrame()

    def news(self, search_term, limit=30):
        """
        Returns all the news found under the search_term.
        
        Parameters
        ----------
        search_term : str
            Term used to filter the news
        limit : int
            Maximum results count that will be retrieved
        """
        
        news = self._internal_search(search_term.lower(), 'news', limit)
        if not news.empty:
            news.link = news.link.apply(lambda x: 'https://www.investing.com{}'.format(x) if x != None and x[0] == '/' else x)
            news.dateTimestamp = pd.to_datetime(news.dateTimestamp, unit='s')
            news = news[['dateTimestamp', 'name', 'link', 'providerName']]
            news.columns = ['datetime', 'name', 'link', 'provider']
            return news

        return pd.DataFrame()

    def articles(self, search_term, limit=30):
        """
        Returns all the articles found under the search_term.
        
        Parameters
        ----------
        search_term : str
            Term used to filter the articles
        limit : int
            Maximum results count that will be retrieved
        """
        
        articles = self._internal_search(search_term.lower(), 'articles', limit)
        if not articles.empty:
            articles.link = articles.link.apply(lambda x: 'https://www.investing.com{}'.format(x) if x != None and x[0] == '/' else x)
            articles.dateTimestamp = pd.to_datetime(articles.dateTimestamp, unit='s')
            articles = articles[['dateTimestamp', 'name', 'link', 'authorName', 'isEditorPick']]
            articles.columns = ['datetime', 'name', 'link', 'author', 'is_editor_pick']
            return articles
            
        return pd.DataFrame()
        
#########################
#### PRIVATE METHODS ####
#########################
    def _internal_search(self, search_term, search_type, limit):
        
        headers = {
            'User-Agent': __user_agent__, 
            'X-Requested-With': 'XMLHttpRequest', 
            'Content-Type':'application/x-www-form-urlencoded'}
        
        url = 'https://www.investing.com/search/service/searchTopBar'    
        payload = urllib.parse.urlencode(
            {'search_text': search_term, 'type': search_type, 'limit': limit})
        
        response = rq.post(url=url, data=payload, headers=headers, proxies=self._proxies)
        response.raise_for_status()
        
        json = response.json()
        return pd.json_normalize(json[search_type])
