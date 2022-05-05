import json
import glob
import pickle
import os
import pandas as pd


class BitfinexHistoricCandleConverter:	

	def convertToPickle(self, pair, download_data_folder, pickle_data_folder):
		all_elm = []
		path = download_data_folder + "/%s*.json" %(pair)
		for filename in glob.glob(path):
			with open(filename, 'r') as f:
				print("Processing file: %s" %(filename))
				content = json.loads(f.read())
				for elm in content:
					all_elm.append(elm)

		#Example  ETHUSD_20190101-20200523.p
		pickle_output_path = os.path.join(pickle_data_folder, 'data_%s.pickle' %(pair))
		pickle.dump(all_elm, open(pickle_output_path, "wb"))
		return pickle_output_path


	def getAsDataframe(self, pickle_file):
		all_json_object = pd.read_pickle(pickle_file)
		df = pd.DataFrame.from_records(all_json_object)
		df.columns = ['TimestampInMilliseconds','Open','High','Low','Close','Volume']
		return df