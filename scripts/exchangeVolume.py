import sys, os
import pandas as pd
import datetime

# Paths and includes
current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)
workspace_root = os.path.dirname(project_dir)
sys.path.append(project_dir)
sys.path.append(workspace_root)

from src.bitfinexHistoricCandleConverter import BitfinexHistoricCandleConverter

# Convert Bitfinex downloaded data to ONE pickle binary file
converter = BitfinexHistoricCandleConverter()
pickle_file = os.path.join(project_dir,'data','pickle','data_BTC_USDT.pickle')

# Convert Pickle to pandas dataframe
df = converter.getAsDataframe(pickle_file)

# USD Trading volume
with open('data.csv', 'w') as f:
	df['VolumeUsd'] = df['Volume'] * df['High']
	for idx, row in df.iterrows():
		dt = datetime.datetime.utcfromtimestamp(row['TimestampInMilliseconds'] / 1000).date() 
		f.write("%s,%i\n" % (dt.isoformat(), row['VolumeUsd']))