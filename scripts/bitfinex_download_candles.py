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
end_date = datetime.datetime.now()

pairs = ['BTCUSD']
for pair in pairs:
	downloader = HistoricDataExporter(data_folder, exchange_ccxt_obj, max_number_of_candles=10000)
	downloader.downloadData('BTC/USDT', start_date, end_date, candle_size_str='1d')