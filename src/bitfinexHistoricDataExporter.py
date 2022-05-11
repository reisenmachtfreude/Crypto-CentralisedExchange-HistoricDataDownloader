import time
import os
import datetime
import json
import time



class BitfinexHistoricDataExporter:
	
	def __init__(self, storage_folder, ccxt_obj):
		self.storage_folder = storage_folder
		self.exchange = ccxt_obj
		self.exchange_name = ccxt_obj.__class__.__name__.split('.')[-1] # Example <class 'ccxt.binance.binance'>


	def _storeCandles(self, pair, candle_size, request_window_start_time, candles):
		dt_start_time = datetime.datetime.utcfromtimestamp(request_window_start_time / 1000)
		request_ident = "%s-%s-%s" % (pair.replace('/','_'), candle_size, dt_start_time.isoformat())
		cache_file = os.path.join(self.storage_folder, request_ident + '.json')
		with open(cache_file, "w") as f:
			json.dump(candles, f)


	def downloadData(self, pair, start_date, end_date, candle_size_str):
		print("Downloading data: symbol=%s, start_date=%s, end_date=%s" %(pair, start_date, end_date))

		candle_size_ms = None
		request_window_start_time = start_date
		while request_window_start_time < end_date:
			print(request_window_start_time)
			candles = self.exchange.fetch_ohlcv(pair, timeframe=candle_size_str, since=request_window_start_time, limit=10000)
			print("Number of downloaded candles: %i " % len(candles))
			self._storeCandles(pair, candle_size_str, request_window_start_time, candles)
			most_recent_received_candle_time = candles[-1][0]
			print(most_recent_received_candle_time)
			
			# calc the size of one received candle
			if candle_size_ms is None:
				candle_size_ms = candles[1][0] - candles[0][0]
			print("candle size is %i" % candle_size_ms)

			# Prepare next window start time
			request_window_start_time = most_recent_received_candle_time + candle_size_ms # plus 1 candle_size_ms