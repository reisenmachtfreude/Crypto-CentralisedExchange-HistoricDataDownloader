import sys, os
import datetime
import json
import ccxt

# Paths and includes
current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)
workspace_root = os.path.dirname(project_dir)
sys.path.append(project_dir)
sys.path.append(workspace_root)

from src.bitfinexHistoricDataExporter import BitfinexHistoricDataExporter

path_to_credentials = os.path.join(workspace_root, 'private', 'credentials_bitfinex.json')
# Template of credentials_bitfinex.json:
# {
# 	"apiKey": "000000000000111111111111111100000000000000",
# 	"secret": "aaaaaaaaaaaabbbbbbbbbbbbbbbbcccccccccccccc",
# 	"password": ""
# }
if not os.path.exists(path_to_credentials):
	raise Exception("ME: Please make sure that file containing Bitfinex API KEY and SECRET is stored at %s" %(path_to_credentials))

with open(path_to_credentials) as f:
	exchange_ccxt_obj = ccxt.bitfinex2(json.load(f))


data_folder = os.path.join(project_dir, 'data','downloads')
start_date = exchange_ccxt_obj.parse8601('2017-01-10 00:00:00')
end_date = datetime.datetime.now().timestamp() * 1000

pairs = ['BTCUSD']
for pair in pairs:

	downloader = BitfinexHistoricDataExporter(data_folder, exchange_ccxt_obj)
	downloader.downloadData('BTC/USDT', start_date, end_date, candle_size_str='1d')