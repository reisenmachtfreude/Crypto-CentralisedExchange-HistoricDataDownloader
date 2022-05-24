import json
import glob
import pickle
import os
import pandas as pd


class HistoricCandleConverter:	

	def convertToPickle(self, pair, download_data_folder, pickle_data_folder):
		all_elm = []
		path = download_data_folder + "/*.json"
		for filename in glob.glob(path):
			with open(filename, 'r') as f:
				print("Processing file: %s" %(filename))
				content = json.loads(f.read())
				for elm in content:
					all_elm.append(elm)

		if len(all_elm) == 0:
			raise Exception("No candle data found in folder %s" % download_data_folder)

		#Example  ETHUSD_20190101-20200523.p
		pickle_output_path = os.path.join(pickle_data_folder, 'data_%s.pickle' %(pair))
		pickle.dump(all_elm, open(pickle_output_path, "wb"))
		element_count = len(all_elm)
		print("%i candles written to %s" %(element_count, pickle_output_path))
		return pickle_output_path


	def getAsDataframe(self, pickle_file):
		if not os.path.exists(pickle_file):
			raise Exception("File not found: %s" % (pickle_file))

		# Create dataframe from pickle file
		all_json_object = pd.read_pickle(pickle_file)
		df = pd.DataFrame.from_records(all_json_object)

		# Add names for loaded columns
		df.columns = ['TimestampInMilliseconds','Open','High','Low','Close','Volume']

		# Add time-based index for dataframe
		df['Date'] = (df['TimestampInMilliseconds'] / 1000).astype('int').astype("datetime64[s]")
		df.set_index('Date',inplace = True)
		df = df.sort_index(axis = 0)

		return df