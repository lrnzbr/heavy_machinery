import pandas as pd
import numpy as np
import scipy.stats as scs
from dateutil import parser
​
def drop_columns(df, names):
	df.drop(names, axis =1, inplace=True)
​
def stanardize_YearMade(df):
	df['YearMade'] = df['YearMade'].apply(lambda x: 0 if x < 1970 else x - 1970)
​
def strip_saledate(df):
	df['saledate'] = df['saledate'].apply(parser.parse).map(lambda x: x.year)
​
def my_get_dummies(series, name, values):
    # In: series - pandas Series
    #     name - the name of series in the Data Frame
    #     values - list of values for dummy variables
    # Out: the dummy columns
    index = series.index
    columns = [name + '_' + str(n) for n in values]
    df_ = pd.DataFrame(index=index, columns=columns)
    df_ = df_.fillna(0)
    for i, val in enumerate(values):
        df_.iloc[:,i] = list((series == val).astype(int))
    return df_

dtype_dict = {	'fiModelSeries': np.object,
				'Coupler_System': np.object,
				'Grouser_Tracks': np.object,
				'Hydraulics_Flow': np.object
				}
df = pd.read_csv('data/Train.csv', dtype=dtype_dict)
y = df.pop('SalePrice').values
​
first_drop = [	'SalesID', 'MachineID', 'ProductGroupDesc', 'datasource',
				'fiModelDesc', 'fiSecondaryDesc', 'fiModelSeries', 'fiBaseModel',
				'fiModelDescriptor', 'fiProductClassDesc', 'ModelID']

drop_columns(df, first_drop)
​
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
			   'Travel_Controls', 'Differential_Type', 'Steering_Controls', 'auctioneerID']

unique_value = []

for col in col_dummies:
	uniq = df[col].unique()		# get unique value for current column
	cleaned_uniq = [x for x in uniq if str(x) != 'nan']
	dummies_i = my_get_dummies(df[col], col, cleaned_uniq)	# create dummies using the provided values
	unique_value.append(cleaned_uniq)	# save the unique values in a list
	df = pd.concat([df, dummies_i], axis=1)		# add dummies to df

# convert unique list to series and add index, so it can be called by the column names
unique_value = pd.Series(unique_value, index = col_dummies)

drop_columns(df, col_dummies)	# columns can be dropped after the dummies are created
​
# use mean value for Nan's
mean_hour_median = df['MachineHoursCurrentMeter'].mean()
df['MachineHoursCurrentMeter'] = df['MachineHoursCurrentMeter'].fillna(mean_hour_median)
​
X = df.values
​
​####### now test datasets

df_test = pd.read_csv('data/Test.csv', dtype=dtype_dict)
drop_columns(df_test, first_drop)
​
stanardize_YearMade(df_test)
strip_saledate(df_test)

for col in col_dummies:
	dummies_i = my_get_dummies(df_test[col], col, unique_value[col])
	df_test = pd.concat([df_test, dummies_i], axis=1)

drop_columns(df_test, col_dummies)

mean_hour_median_test = df_test['MachineHoursCurrentMeter'].mean()
df_test['MachineHoursCurrentMeter'] = df_test['MachineHoursCurrentMeter'].fillna(mean_hour_median_test)
​
X_test = df_test.values
