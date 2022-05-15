import time
import os
import datetime
import json
import time

from src.candleDownloadException import CandleDownloadException


class HistoricDataExporter:
	
	
	def __init__(self, storage_folder, ccxt_obj, max_number_of_candles):
		self.storage_folder = storage_folder
		self.exchange = ccxt_obj
		self.exchange_name = ccxt_obj.__class__.__name__.split('.')[-1] # Example <class 'ccxt.binance.binance'>
		self.max_number_of_candles = max_number_of_candles


	def downloadData(self, pair, start_date, end_date, candle_size_str):
		print("Downloading data: symbol=%s, start_date=%s, end_date=%s" %(pair, start_date, end_date))
		first_round = True
		
		folder_ident = self._getFolderIdent(pair=pair, candle_size=candle_size_str, start_date=start_date, end_date=end_date)
		folder_full_path = os.path.join(self.storage_folder, folder_ident)
		if os.path.exists(folder_full_path):
			raise CandleDownloadException("Skipping download because data folder exists: Downloading data: symbol=%s, start_date=%s, end_date=%s" %(pair, start_date, end_date))
		
		# Iterate over time range
		end_date_mts = end_date.timestamp() * 1000
		start_date_mts = self.exchange.parse8601(start_date.isoformat())
		candle_size_ms = None
		request_window_start_time = start_date_mts
		while request_window_start_time < end_date_mts:
			candles = self.exchange.fetch_ohlcv(pair, timeframe=candle_size_str, since=request_window_start_time, limit=self.max_number_of_candles)
			if len(candles) == 0:
				raise CandleDownloadException("Exchange does not return any candle data: symbol=%s, start_date=%s, end_date=%s" %(pair, start_date, end_date))
			print("Number of downloaded candles: %i " % len(candles))

			# Create destination folder after first successful download
			if first_round: 
				os.mkdir(folder_full_path)
				first_round = False
				
			self._storeCandles(folder_full_path, request_window_start_time, candles)
			most_recent_received_candle_time = candles[-1][0]
			print(most_recent_received_candle_time)
			
			# calc the size of one received candle
			if candle_size_ms is None:
				candle_size_ms = candles[1][0] - candles[0][0]
			# print("DEBUG: candle size is %i" % candle_size_ms)

			# Prepare next window start time
			request_window_start_time = most_recent_received_candle_time + candle_size_ms # plus 1 candle_size_ms


	# Generate a folder name which contains information about the contained data
	def _getFolderIdent(self, pair, candle_size, start_date, end_date):
		pair_str = pair.replace('/','_')
		start_str = start_date.replace(microsecond=0).isoformat().replace(':','-')
		end_str = end_date.replace(microsecond=0).isoformat().replace(':','-')
		folder_ident = "%s-%s-%s-%s-TO-%s" % (self.exchange_name, pair_str, candle_size, start_str, end_str)
		return folder_ident


	def _storeCandles(self, folder_full_path, request_window_start_time, candles):
		dt_start_time = datetime.datetime.utcfromtimestamp(request_window_start_time / 1000)
	
		request_ident = "%s" % ( dt_start_time.isoformat())
		cache_file = os.path.join(folder_full_path, request_ident + '.json')
		with open(cache_file, "w") as f:
			json.dump(candles, f)