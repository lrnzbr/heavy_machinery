import pandas as pd
import numpy as np
import scipy.stats as scs
from dateutil import parser

def drop_columns(df, names):
	df.drop(names, axis =1, inplace=True)

def stanardize_YearMade(df):
	df['YearMade'] = df['YearMade'].apply(lambda x: 0 if x < 1970 else x - 1970)

def strip_saledate(df):
	df['saledate'] = df['saledate'].apply(parser.parse).map(lambda x: x.year)

def normalize(df, col_name):
	columns = df.columns.values

	year_mean = df['YearMade'].mean()
	year_std = df['YearMade'].std()
	df['YearMade_Normalized'] = df['YearMade'].apply(lambda x: (x - year_mean) / year_std)

def make_dummies(df):
	col_names = df.columns
	col_dummies = col_names[:-37]   # from "Product Size"
	for names in col_dummies:
	   dummies_i = pd.get_dummies(df[names])
	   df = pd.concat([df, dummies_i], axis=1)


if __name__ == '__main__':

	## Correctly assigned mixed types and import.
	dtype_dict = {	'fiModelSeries': np.object, 
					'Coupler_System': np.object, 
					'Grouser_Tracks': np.object, 
					'Hydraulics_Flow': np.object}
	df = pd.read_csv('data/Train.csv', dtype=dtype_dict)

	## Get our X and y
	first_drop = ['SalesID', 'MachineID', 'ProductGroupDesc',
					'fiModelDesc', 'fiSecondaryDesc', 'fiModelSeries', 
					'fiModelDescriptor', 'fiProductClassDesc']
	drop_columns(df, first_drop)

	## Data munging
	stanardize_YearMade(df)
	strip_saledate(df)
	normalize_df(df):
	make_dummies(df)



