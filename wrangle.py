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

def make_dummies(df, col_dummies):
	dummies_i = pd.get_dummies(df, columns = col_dummies)
	return dummies_i

if __name__ == '__main__':
	dtype_dict = {	'fiModelSeries': np.object, 
					'Coupler_System': np.object, 
					'Grouser_Tracks': np.object, 
					'Hydraulics_Flow': np.object
					}
	df = pd.read_csv('../data/Train.csv', dtype=dtype_dict)
	y = df['SalePrice'].values

	first_drop = [	'SalesID', 'MachineID', 'ProductGroupDesc', 'datasource',
					'fiModelDesc', 'fiSecondaryDesc', 'fiModelSeries', 'fiBaseModel',
					'fiModelDescriptor', 'fiProductClassDesc', 'ModelID', 'SalePrice'
					]
	drop_columns(df, first_drop)

	stanardize_YearMade(df)
	strip_saledate(df)
	col_dummies = ['ProductSize', 'state', 'ProductGroup', 'Drive_System', 'Enclosure',
				   'Forks', 'Pad_Type', 'Ride_Control', 'Stick', 'Transmission',
				   'Turbocharged', 'Blade_Extension', 'Blade_Width', 'Enclosure_Type',
				   'Engine_Horsepower', 'Hydraulics', 'Pushblock', 'Ripper',
				   'Scarifier', 'Tip_Control', 'Tire_Size', 'Coupler', 'UsageBand',
				   'Coupler_System', 'Grouser_Tracks', 'Hydraulics_Flow', 'Track_Type',
				   'Undercarriage_Pad_Width', 'Stick_Length', 'Thumb',
				   'Pattern_Changer', 'Grouser_Type', 'Backhoe_Mounting', 'Blade_Type',
				   'Travel_Controls', 'Differential_Type', 'Steering_Controls', 'auctioneerID'
				   ]
	clean_df = make_dummies(df, col_dummies)

	mean_hour_median = clean_df['MachineHoursCurrentMeter'].mean()
	clean_df['MachineHoursCurrentMeter'] = clean_df['MachineHoursCurrentMeter'].fillna(mean_hour_median)

	X = clean_df.values

