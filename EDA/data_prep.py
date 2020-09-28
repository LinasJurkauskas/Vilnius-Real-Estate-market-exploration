import pandas as pd


def create_df_raw():
	'''
	Loads the raw data, makes the exclusion of unused data for analysis.
	1) extra large apartments > 120 sq. m excluded.
	2) only apartments (no houses) are included (type = 1)
	'''
	df_raw = pd.read_excel(r'C:\Users\tiesi\Class D\Vilnius-Real-Estate-market-exploration\Data.xlsx', index_col=0, sheet_name="posts") 
	#df_raw = df_raw[df_raw['year'] > 2018]
	df_raw = df_raw[df_raw['space_sq_m']< 120]
	#df_raw = df_raw[df_raw['type'] != 2]
	df_raw['log_date'] = pd.to_datetime(df_raw['log_date'])
	df_raw['week'] = df_raw['log_date'].dt.week
	#df_raw = df_raw[df_raw['state']==2]

	#select the columns for analysis
	df_raw_columns = [ 'log_date', 'district', 'street', 'year', 'total_price',
	       'price_sq_m', 'nr_rooms', 'space_sq_m', 'floor', 'nr_floors', 'week', 'state', 'type']

	df_raw = df_raw[df_raw_columns]

	return df_raw

def create_obj_raw():
	'''
	Loads the raw data, makes the exclusion of unused data for analysis.
	1) extra large apartments > 120 sq. m excluded.
	2) only apartments (no houses) are included (type = 1)
	'''
	df_raw = pd.read_excel(r'C:\Users\tiesi\Class D\Vilnius-Real-Estate-market-exploration\Data.xlsx', index_col=0, sheet_name="objects") 
	#df_raw = df_raw[df_raw['year'] > 2018]
	df_raw = df_raw[df_raw['space_sq_m']< 120]
	#df_raw = df_raw[df_raw['type'] != 2]
	df_raw['log_date'] = pd.to_datetime(df_raw['log_date'])
	df_raw['week'] = df_raw['log_date'].dt.week
	#df_raw = df_raw[df_raw['state']==2]

	#select the columns for analysis
	#df_raw_columns = [ 'log_date', 'district', 'street', 'year', 'total_price',
	#       'price_sq_m', 'nr_rooms', 'space_sq_m', 'floor', 'nr_floors', 'week', 'state', 'type']

	#df_raw = df_raw[df_raw_columns]

	return df_raw


def create_distinct_obj_raw():
	'''
	Loads the raw data, makes the exclusion of unused data for analysis.
	1) extra large apartments > 120 sq. m excluded.
	2) only apartments (no houses) are included (type = 1)
	'''
	df_raw = pd.read_excel(r'C:\Users\tiesi\Class D\Vilnius-Real-Estate-market-exploration\Data.xlsx', index_col=0, sheet_name="distinct_objects") 
	#df_raw = df_raw[df_raw['year'] > 2018]
	df_raw = df_raw[df_raw['space_sq_m']< 120]
	df_raw = df_raw[df_raw['type']==1]
	#df_raw = df_raw[df_raw['type'] != 2]
	df_raw['first_date'] = pd.to_datetime(df_raw['first_date'])
	df_raw['last_date'] = pd.to_datetime(df_raw['last_date'])

	#df_raw['week'] = df_raw['log_date'].dt.week
	#df_raw = df_raw[df_raw['state']==2]

	#select the columns for analysis
	#df_raw_columns = [ 'log_date', 'district', 'street', 'year', 'total_price',
	#       'price_sq_m', 'nr_rooms', 'space_sq_m', 'floor', 'nr_floors', 'week', 'state', 'type']

	#df_raw = df_raw[df_raw_columns]

	return df_raw



def create_df(df_raw, type):
	log_dates = set(df_raw['week'])

	#creating an analysis table where data without outlyers will be put
	df = df_raw[0:1].copy()
	df = df.reset_index()
	df = df.drop(df.index[0])
	df = df.drop(['ID'], axis=1)
	df_raw = df_raw[df_raw['type']==type]

	#preparing the quantiles range dataframe
	column_names = ['Q1','Q2','Q3','Q4','IQR', 
					'Skewness_w_outlyers','Skewness', 
					'Mean_w_outlyers', 'Mean',
					'Median_w_outlyers', 'Median',
					'nr_objects_w_outlyers', 'nr_objects']
	quantiles_range = pd.DataFrame(columns = column_names)

	for week in sorted(log_dates):
		Q1 = df_raw['price_sq_m'][df_raw['week'] == week].quantile(.001) 
		Q2 = df_raw['price_sq_m'][df_raw['week'] == week].quantile(.25) 
		Q3 = df_raw['price_sq_m'][df_raw['week'] == week].quantile(.75) 
		Q4 = df_raw['price_sq_m'][df_raw['week'] == week].quantile(.99)
		Skewness1 = df_raw['price_sq_m'][df_raw['week'] == week].skew()
		Mean1 = df_raw['price_sq_m'][df_raw['week'] == week].mean()
		Median1 = df_raw['price_sq_m'][df_raw['week'] == week].median()
		IQR = Q3 - Q2
		df_temp = df_raw[df_raw['week'] == week]
		df_temp = df_temp[(df_temp['price_sq_m'] > Q1)]
		df_temp = df_temp[(df_temp['price_sq_m'] < Q4)]
		df = df.append(df_temp, sort=False)
		Skewness2 = df['price_sq_m'][df['week'] == week].skew()
		Mean2 = df['price_sq_m'][df['week'] == week].mean()
		Median2 = df['price_sq_m'][df['week'] == week].median()
		nr_objects_w_outlyers = df_raw['price_sq_m'][df_raw['week'] == week].count()
		nr_objects = df['price_sq_m'][df['week'] == week].count()
		quantiles_range = quantiles_range.append(pd.Series(data={'Q1': Q1,
																'Q2': Q2,
																'Q3' : Q3,
																'Q4': Q4,
																'IQR': IQR,
																'Skewness_w_outlyers': Skewness1,
																'Skewness': Skewness2,
																'Mean_w_outlyers': Mean1,
																'Mean': Mean2,
																'Median_w_outlyers':Median1,
																'Median':Median2,
																'nr_objects_w_outlyers': nr_objects_w_outlyers,
																'nr_objects': nr_objects
																}, name=(week)))

	return df, quantiles_range


def create_segments(df):
	'''
	Creates 4 data segmentations:
	1) age segment
	2) size segment
	3) street segment
	4) district by avg price segment
	5) district by pop segment
	'''	
	df['age_segment'] = df.apply(define_year, axis=1)		
	df['size_segment'] = pd.qcut(df['space_sq_m'], q=3, labels=["small", "medium", "large"])	

	streets = df.groupby('street')['price_sq_m'].agg(['mean'])
	streets['street_rank'] = pd.qcut(streets['mean'], q=3,  labels=[1,2,3])
	df = pd.merge(df, streets['street_rank'], on='street', how='outer')	

	districts = df.groupby('district')['price_sq_m'].agg(['mean','count'])
	districts['district_rank'] = pd.qcut(districts['mean'], q=3,  labels=[ 1,2,3])
	df = pd.merge(df, districts['district_rank'], on='district', how='outer')

	#df['size_segment'] = df.size_segment.astype('category').cat.codes
	#df['street_rank'] = df.street_rank.astype('category').cat.codes
	#df['district_rank'] = df.district_rank.astype('category').cat.codes

	districts['avg_count'] = districts['count']/df['week'].nunique()
	districts_top10 = districts.nlargest(5,'count')
	districts = pd.merge(districts, districts_top10['avg_count'], left_index=True, right_index=True, how='outer')
	districts = districts.reset_index()
	districts['District_pop_rank'] = districts.apply(rank_districts, axis=1)
	districts.rename(columns={'avg_count_x':'avg_count'}, inplace=True)  
	del districts['avg_count_y']

	return df, streets, districts

def define_year(df):
    if df['year'] >= 2019:
        return 'New (2019+)'
    elif df['year'] > 1999:
        return 'Moderate (1999+)'
    else:
        return 'Old'


def rank_districts(districts):
    if districts['avg_count_y'] > 0:
        return districts['district']
    else:
        return 'Others'