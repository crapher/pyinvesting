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
from .online_scrapping import OnlineScrapping
from .online_websocket import OnlineWebsocket

class Online:
    
    def __init__(self, on_open=None, on_quotes=None, on_heartbeat=None, 
        on_error=None, on_close=None, proxy_url=None):
        """
        Class constructor 
        
        Parameters
        ----------
        on_open : function(self), optional
            Callable object which is called at opening websocket.
            This function has one argument. The argument is the callable object.
        on_quotes: function(self, quotes), optional
            Callable object which is called when received data.
            This function has 2 arguments.
                The 1st argument is the callable object.
                The 2nd argument is the dataframe with the quotes.
        on_heartbeat : function(self), optional
            Callable object which is called when a heartbeat response is received.
            This function has one argument. The argument is the callable object.
        on_error: function(self, exception), optional
            Callable object which is called when we get error.
            This function has 2 arguments.
                The 1st argument is the callable object.
                The 2nd argument is the exception object.
        on_close: function(self), optional
            Callable object which is called when closed the connection.
            This function has one argument. The argument is the callable object.
        proxy_url : str, optional
            The proxy URL with one of the following formats:
                - scheme://user:pass@hostname:port 
                - scheme://user:pass@ip:port
                - scheme://hostname:port 
                - scheme://ip:port
            
            Ex. https://john:doe@10.10.1.10:3128
        """
                
        self._pid_map = {}
        
        self._scrapping = OnlineScrapping(proxy_url=proxy_url)
        self._websocket = OnlineWebsocket(
            on_open = self._internal_on_open, 
            on_quotes = self._internal_on_quotes,
            on_heartbeat = self._internal_on_heartbeat, 
            on_error = self._internal_on_error, 
            on_close = self._internal_on_close,
            proxy_url = proxy_url)
        
        self._on_open = on_open
        self._on_quotes = on_quotes
        self._on_heartbeat = on_heartbeat
        self._on_error = on_error
        self._on_close = on_close
        
########################
#### PUBLIC METHODS ####
########################
    def connect(self):       
        """
        Connects to websocket to receive quotes information.
        """
        
        try:
            stream_server = self._scrapping.get_stream_server()
            self._websocket.connect(stream_server)
        except Exception as ex:
            self._internal_on_error(ex)
        
    def disconnect(self):
        """
        Disconnects from websocket to stop receiving quotes information.
        """
        
        try:
            self._websocket.disconnect()
        except Exception as ex:
            self._internal_on_error(ex)

    def subscribe(self, pair_id, ticker=None, link=None):
        """
        Subscribe to an asset to receive its quote information.
        
        Parameters
        ----------
        pair_id : int
            The pair_id that identify the asset to be retrieved.
        ticker : str, option
            The name of the ticker to be retrieved.
            If it is not specified, the ticker is the dataframe will be the pair_id
        link : str, optional
            The link received in the search ticket query. 
            If it is specified, it will be used to get the data, previous to subscribe it to the websocket connection.
        """
        
        self._pid_map[pair_id] = ticker if ticker else pair_id

        if link:
            try:
                quotes = self._scrapping.get_quotes_from_link(pair_id, link)
                self._internal_on_quotes(quotes)
            except:
                pass
                
        self._websocket.subscribe_event(pair_id)
        
########################
#### RTWS CALLBACKS ####        
########################
    def _internal_on_open(self):
        
        if self._on_open:
            self._on_open(self)
            
    def _internal_on_quotes(self, quotes):
                
        if self._on_quotes:
            column = quotes['pair_id'].apply(lambda x: self._pid_map[x] if x in self._pid_map else x)
            quotes.insert(0, 'ticker', column)
            quotes.set_index('pair_id', inplace=True)
            self._on_quotes(self, quotes)

    def _internal_on_heartbeat(self):

        if self._on_heartbeat:
            self._on_heartbeat(self)
        
    def _internal_on_error(self, error):

        if self._on_error:
            self._on_error(self, error)
        
    def _internal_on_close(self):

        if self._on_close:
            self._on_close(self)
