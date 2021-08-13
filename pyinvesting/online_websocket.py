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

from threading import Thread, Event, Lock
import random
import websocket
import json
import re

import pandas as pd
import numpy as np

class OnlineWebsocket:
    
    def __init__(self, on_open=None, on_quotes=None, on_heartbeat=None, 
        on_error=None, on_close=None, proxy_url=None):
        """
        Class constructor 
        
        Parameters
        ----------
        on_open : function(), optional
            Callable object which is called at opening websocket.
            This function has no argument.
        on_quotes: function(quotes), optional
            Callable object which is called when received data.
            This function has 1 argument. The argument is the dataframe with the quotes.
        on_heartbeat : function(), optional
            Callable object which is called when a heartbeat response is received.
            This function has no argument.            
        on_error: function(exception), optional
            Callable object which is called when we get error.
            This function has 1 arguments. The argument is the exception object.
        on_close: function(), optional
            Callable object which is called when closed the connection.
            This function has no argument.
        proxy_url : str, optional
            The proxy URL with one of the following formats:
                - scheme://user:pass@hostname:port 
                - scheme://user:pass@ip:port
                - scheme://hostname:port 
                - scheme://ip:port
            
            Ex. https://john:doe@10.10.1.10:3128
        """
        
        self._proxy_data = self._get_proxy_data(proxy_url)
            
        self._on_open = on_open
        self._on_quotes = on_quotes
        self._on_heartbeat = on_heartbeat
        self._on_error = on_error
        self._on_close = on_close
        
        self._ws = None
        self._ws_keep_alive_thread = None
        self._ws_keep_alive_thread_event = None

        self._connection_thread = None        
        self._connection_lock = Lock()
        
        global _rtws_instance
        _rtws_instance = self
        
########################
#### PUBLIC METHODS ####
########################
    def connect(self, stream_server):
        """
        Connects to websocket to receive quotes information.
        
        Parameters
        ----------
        stream_server : int
            The server id used by the websocket.
        """
        
        if stream_server is None:
            raise Exception("Stream Server is None")
            
        with self._connection_lock:
            if not self._ws:
                url = 'wss://{}/echo/{}/{}/websocket'.format(
                    stream_server, 
                    random.randrange(0, 1000), 
                    ''.join(random.choice('abcdefghijklmnopqrstuvwxyz0123456789') for _ in range(8)))
                                
                self._ws = websocket.WebSocketApp(url,
                    on_open = self._internal_on_open,
                    on_message = self._internal_on_message,
                    on_error = self._internal_on_error,
                    on_close = self._internal_on_close)
             
                self._connection_thread = Thread(target=self._ws_connect_async)
                self._connection_thread.daemon = True
                self._connection_thread.start()

    def disconnect(self):
        """
        Disconnects from websocket to stop receiving quotes information.
        """
        
        with self._connection_lock:       
            if self._ws and self._ws.keep_running:
                self._ws.close()
            
            if self._connection_thread and self._connection_thread.isAlive():
                self._connection_thread.join(1)
            
            self._ws = None
            self._connection_thread = None
            
    def subscribe_event(self, pair_id):
        """
        Subscribe to an event to receive its quote information.
        
        Parameters
        ----------
        pair_id : int
            The pair_id that identify the asset to be retrieved.
        """
        
        with self._connection_lock:
            if not self._ws or not self._ws.keep_running:
                raise Exception("Connection is not open.")
            
            event = {'_event': 'subscribe', 'tzID': 8, 'message': 'pid-{}:'.format(pair_id)}
            self._ws.send('\"{}\"'.format(json.dumps(event).replace('\"','\\\"')))

    def unsubscribe_event(self, pair_id):
        """
        Unsubscribe from an event to stop receiving its quote information.
        
        Parameters
        ----------
        pair_id : int
            The pair_id that identify the asset to be retrieved.
        """
        
        with self._connection_lock:
            if not self._ws or not self._ws.keep_running:
                raise Exception("Connection is not open.")

            event = {'_event': 'unsubscribe', 'tzID': 8, 'message': 'pid-{}:'.format(pair_id)}
            self._ws.send('\"{}\"'.format(json.dumps(event).replace('\"','\\\"')))
            
#########################
#### PRIVATE METHODS ####
#########################
    def _get_proxy_data(self, proxy_url):
        
        result = {'host': None, 'port': None, 'user': None, 'pass': None}
        
        if proxy_url:
            parts = re.search('((\w+):(\w+)?@)?([\d|\w|.|-]+):(\d{2,5})', proxy_url)    
            
            if parts:
                result['user'] = parts.group(2)
                result['pass'] = parts.group(3)
                result['host'] = parts.group(4)
                result['port'] = int(parts.group(5))
            
        return result            
        
    def _ws_connect_async(self):
        
        ws = self._ws # Keep secure reference
        
        try:
            ws.run_forever(
                http_proxy_host = self._proxy_data['host'], 
                http_proxy_port = self._proxy_data['port'],
                http_proxy_auth = (self._proxy_data['user'], self._proxy_data['pass']) if self._proxy_data['user'] else None)
        except:
            pass
            
    def _ws_keep_alive(self):
        
        # Send Heartbeat to server every 1 second to keep the connection alive
        while not self._ws_keep_alive_thread_event.is_set():
            try:
                event = {'_event': 'heartbeat', 'message': 'h'}
                self._ws.send('\"{}\"'.format(json.dumps(event).replace('\"','\\\"')))
            except:
                pass
            
            self._ws_keep_alive_thread_event.wait(1)
            
    def _get_quotes_from_message(self, message):
        
        # Clean message (Remove backslashed, percentage, comma from numbers, and the non used suffix/prefix)
        message = message.replace('\\', '').replace('%','').replace(',"',';"').replace(",","").replace(';"',',"')
        message = message[message.index('::') + 2:len(message) - 4]
        quotes_df = pd.DataFrame(json.loads(message), index=[0])
        
        raw_cols = ['pid', 'bid', 'ask', 'last', 'high', 'low', 'pcp', 'turnover_numeric', 'pc', 'timestamp']
        for col in raw_cols:
            if not col in quotes_df.columns:
                quotes_df[col] = np.NAN
        quotes_df = quotes_df[raw_cols]
        
        cols = ['pair_id', 'bid', 'ask', 'last', 'high', 'low', 'change', 'turnover', 'previous_close', 'timestamp']
        quotes_df.columns = cols        
        quotes_df[cols] = quotes_df[cols].apply(pd.to_numeric) 
        quotes_df['previous_close'] = quotes_df['last'] - quotes_df['previous_close']
        quotes_df['datetime'] = pd.to_datetime(quotes_df['timestamp'], unit='s')
        quotes_df = quotes_df[['pair_id', 'bid', 'ask', 'last', 'high', 'low', 'change', 'turnover', 'previous_close', 'datetime']]
              
        return quotes_df

#############################
#### WEBSOCKET CALLBACKS ####        
#############################
    def _internal_on_open(ws):
        
        self = _rtws_instance
        
        self._ws_keep_alive_thread_event = Event()
        self._ws_keep_alive_thread = Thread(target=self._ws_keep_alive)
        self._ws_keep_alive_thread.daemon = True
        self._ws_keep_alive_thread.start()
        
        if self._on_open:
            self._on_open()

    def _internal_on_close(ws):

        self = _rtws_instance
        
        if self._ws_keep_alive_thread_event:
            self._ws_keep_alive_thread_event.set()
            self._ws_keep_alive_thread.join()
        
        if self._on_close:
            self._on_close()

    def _internal_on_error(ws, error):

        self = _rtws_instance

        if self._on_error:
            self._on_error(error)

    def _internal_on_message(ws, message):

        self = _rtws_instance
        
        try:
            if message[0] == 'a':
                if message.find('pid') > 0:
                    if self._on_quotes:
                        data = self._get_quotes_from_message(message)
                        self._on_quotes(data)
                elif message.find('heartbeat') > 0:
                    if self._on_heartbeat:
                        self._on_heartbeat()
        except Exception as ex:
            if self._on_error:
                self._on_error(ex)
