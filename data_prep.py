import pandas as pd


def df_creation():
	df_raw = pd.read_excel(r'C:\Users\tiesi\Class D\Vilnius-Real-Estate-market-exploration\Data.xlsx', index_col=0) 
	#remove data from new apartments:
	df_raw = df_raw[df_raw['year']< 2019]
	#remove data from exceptionally big apartments(projects):
	df_raw = df_raw[df_raw['space_sq_m']< 120]
	#keep only selling apartments (type = 1)  data:
	df_raw = df_raw[df_raw['type'] == 1]
	#update column types:
	df_raw['log_date'] = pd.to_datetime(df_raw['log_date'])

	#create week column
	df_raw['week'] = df_raw['log_date'].dt.week

	#select the columns for analysis
	df_raw_columns = [ 'log_date', 'district', 'street', 'year', 'total_price',
	       'price_sq_m', 'nr_rooms', 'space_sq_m', 'floor', 'nr_floors', 'state', 'type', 'week']

	df_raw = df_raw[df_raw_columns]

	return df_raw
