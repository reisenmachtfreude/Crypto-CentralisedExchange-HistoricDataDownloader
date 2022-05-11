import sys, os
import pandas as pd

# Paths and includes
current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)
workspace_root = os.path.dirname(project_dir)
sys.path.append(project_dir)
sys.path.append(workspace_root)

from src.bitfinexHistoricCandleConverter import BitfinexHistoricCandleConverter

# Convert Bitfinex downloaded data to ONE pickle binary file
download_data_folder = os.path.join(project_dir, 'data','downloads','bitfinex-BTC_USDT-1m')
pickle_data_folder = os.path.join(project_dir, 'data','pickle')
converter = BitfinexHistoricCandleConverter()
pickle_file = converter.convertToPickle('BTC_USDT',download_data_folder, pickle_data_folder)

# Convert Pickle to pandas dataframe
df = converter.getAsDataframe(pickle_file)
print(df)