import sys, os
import glob

# Paths and includes
current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)
workspace_root = os.path.dirname(project_dir)
sys.path.append(project_dir)
sys.path.append(workspace_root)

from src.historicCandleConverter import HistoricCandleConverter

converter = HistoricCandleConverter()
pickle_data_folder = os.path.join(project_dir, 'data','pickle')


# Convert specifc downloaded data to ONE pickle binary file
# download_data_folder = os.path.join(project_dir, 'data','downloads','bitfinex-BTC_USDT-1m')
# pickle_file = converter.convertToPickle('BTC_USDT',download_data_folder, pickle_data_folder)

# # Convert Pickle to pandas dataframe
# df = converter.getAsDataframe(pickle_file)
# print(df)

# Convert all downloadeds data to ONE pickle binary file
download_basefolder = os.path.join(project_dir, 'data','downloads')
for download_folder in glob.glob(download_basefolder + '/*'):
	print("Processing download folder %s" % download_folder)
	ident_str = os.path.basename(download_folder)
	pickle_file = converter.convertToPickle(ident_str, download_folder, pickle_data_folder)
	df = converter.getAsDataframe(pickle_file)
	print(df)