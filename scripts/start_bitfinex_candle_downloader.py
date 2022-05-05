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

path_to_credentials = os.path.append(workspace_root, 'private', 'credentials_bf_acc1.json')
if not os.path.exists(path_to_credentials):
	raise Exception("ME: Please make sure that file containing Bitfinex API KEY and SECRET is stored at %s" %(path_to_credentials))

with open(path_to_credentials) as f:
	exchange = ccxt.bitfinex2(json.load(f))


pairs = ['BTCUSD']
startDate = datetime.date(2020, 1, 1)
endDate = datetime.date.today()

currentPath = os.path.dirname(os.path.abspath(__file__))