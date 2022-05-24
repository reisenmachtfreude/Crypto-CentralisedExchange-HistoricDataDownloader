import sys, os
import datetime
import json
import ccxt
import argparse

# Paths and includes
current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)
workspace_root = os.path.dirname(project_dir)
sys.path.append(project_dir)
sys.path.append(workspace_root)

from src.historicDataExporter import HistoricDataExporter
from src.candleDownloadException import CandleDownloadException

# Example call:
# python3 download_candles.py --exchange=bitfinex --pair=ETH/USD --start_date='2022-01-01 00:00:00' --end_date='2022-05-15 00:00:00' --candle_size=1m
parser = argparse.ArgumentParser(description='')
parser.add_argument('--exchange', dest='exchange_name', required=True)
parser.add_argument('--start_date', dest='start_date', required=True)
parser.add_argument('--end_date', dest='end_date', required=True)
parser.add_argument('--candle_size', dest='candle_size', required=True)
parser.add_argument('--pair', dest='pair', required=True)

args = parser.parse_args()

if not args.exchange_name.lower() in ['binance', 'bitfinex']:
	raise Exception("ME: unsupported exchange, so far only binance and bitfinex is supported")
else:
	exchange_name = args.exchange_name.lower()

path_to_credentials = os.path.join(workspace_root, 'private', 'credentials_%s.json' % exchange_name)
# Template of credentials_bitfinex.json:
# {
# 	"apiKey": "000000000000111111111111111100000000000000",
# 	"secret": "aaaaaaaaaaaabbbbbbbbbbbbbbbbcccccccccccccc",
# 	"password": ""
# }
if not os.path.exists(path_to_credentials):
	raise Exception("ME: Please make sure that file containing Bitfinex API KEY and SECRET is stored at %s" %(path_to_credentials))

with open(path_to_credentials) as f:
	ccxt_parameters = json.load(f)

# Handle exchange specific parameters
if exchange_name == 'binance':
		ccxt_parameters['options'] = { 'adjustForTimeDifference': True, 'enableRateLimit': True,'recvWindow': 60000}
		# API Docs show Binance allows max 1000 candle sticks per response
		# https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md#klinecandlestick-data
		amount_of_candles_per_request = 1000
elif exchange_name == 'bitfinex':
	amount_of_candles_per_request = 10000
else:
	raise Exception("ME: Unknown exchange")

	
method_to_call = getattr(ccxt, exchange_name)
exchange_ccxt_obj = method_to_call(ccxt_parameters)

data_folder = os.path.join(project_dir, 'data','downloads')
start_date = datetime.datetime.strptime(args.start_date, "%Y-%m-%d %H:%M:%S")
end_date =  datetime.datetime.strptime(args.end_date, "%Y-%m-%d %H:%M:%S")

# Download all candles using a list of specific pairs
if args.pair.upper()=='ALL':
	# Download candles for all currencies on the exchange
	pairs = exchange_ccxt_obj.loadMarkets()
else:
	#
	pairs = [args.pair.upper()] 

#Download selected data
for pair in pairs:
	try:
		downloader = HistoricDataExporter(data_folder, exchange_ccxt_obj, max_number_of_candles=amount_of_candles_per_request)
		downloader.downloadData(pair, start_date, end_date, candle_size_str=args.candle_size)
	except CandleDownloadException as e:
		print(e)