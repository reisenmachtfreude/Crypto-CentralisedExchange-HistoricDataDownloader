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

from src.historicDataExporter import HistoricDataExporter
from src.candleDownloadException import CandleDownloadException


exchange_name = 'bitfinex'
path_to_credentials = os.path.join(workspace_root, 'private', 'credentials_%s.json' % exchange_name)
# path_to_credentials = os.path.join(project_dir, 'config', 'credentials_%s.json' % exchange_name)
if not os.path.exists(path_to_credentials):
	raise Exception("ME: Please make sure that file containing Bitfinex API KEY and SECRET is stored at %s" %(path_to_credentials))


with open(path_to_credentials) as f:
	method_to_call = getattr(ccxt, exchange_name)
	exchange_ccxt_obj = method_to_call(json.load(f))


data_folder = os.path.join(project_dir, 'data','downloads')
start_date = datetime.datetime.strptime('2017-01-10 00:00:00', "%Y-%m-%d %H:%M:%S")
end_date =  datetime.datetime.strptime('2022-05-15 00:00:00', "%Y-%m-%d %H:%M:%S")

# Download all candles using a list of specific pairs
# pairs = ['BTC/USDT'] 

# Download candles for all currencies on the exchange
pairs = exchange_ccxt_obj.loadMarkets()

for pair in pairs:
	try:
		downloader = HistoricDataExporter(data_folder, exchange_ccxt_obj, max_number_of_candles=10000)
		downloader.downloadData(pair, start_date, end_date, candle_size_str='1d')
	except CandleDownloadException as e:
		print(e)