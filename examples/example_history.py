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

history = ic.History()

print('MSFT history chart - Timeframe: 5 minutes - Period: 1 day')
print(history.get_chart_data(252, interval='300', period='1-day'))

print('QQQ history chart - Timeframe: 5 hours - Period: 3 months')
print(history.get_chart_data(651, interval='18000', period='3-months'))

print('AAPL history chart - Timeframe: 1 week')
print(history.get_chart_data(6408, interval='week'))

print('TSLA history advanced chart - Timeframe: 60 minutes')
print(history.get_adv_chart_data(13994, timeframe='60M'))

print('GOOG history advanced chart - Timeframe: 1 minute')
print(history.get_adv_chart_data(100160, timeframe='1M'))

print('VIX history advanced chart - Timeframe: 1 day')
print(history.get_adv_chart_data(44336, timeframe='1D'))