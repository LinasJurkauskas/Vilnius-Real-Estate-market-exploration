import pandas as pd


def create_df_raw():
	'''
	Loads the raw data, makes the exclusion of unused data for analysis.
	1) extra large apartments > 120 sq. m excluded.
	2) only apartments (no houses) are included (type = 1)
	'''
	df_raw = pd.read_excel(r'C:\Users\tiesi\Class D\Vilnius-Real-Estate-market-exploration\Data.xlsx', index_col=0) 
	#df_raw = df_raw[df_raw['year'] > 2018]
	df_raw = df_raw[df_raw['space_sq_m']< 120]
	df_raw = df_raw[df_raw['type'] == 1]
	df_raw['log_date'] = pd.to_datetime(df_raw['log_date'])
	df_raw['week'] = df_raw['log_date'].dt.week
	#df_raw = df_raw[df_raw['state']==2]

	#select the columns for analysis
	df_raw_columns = [ 'log_date', 'district', 'street', 'year', 'total_price',
	       'price_sq_m', 'nr_rooms', 'space_sq_m', 'floor', 'nr_floors', 'week', 'state']

	df_raw = df_raw[df_raw_columns]

	return df_raw




def create_df(df_raw):
	log_dates = set(df_raw['week'])

	#creating an analysis table where data without outlyers will be put
	df = df_raw[0:1].copy()
	df = df.reset_index()
	df = df.drop(df.index[0])
	df = df.drop(['ID'], axis=1)

	#preparing the quantiles range dataframe
	column_names = ['Q1','Q2','Q3','Q4','IQR', 
					'Skewness_w_outlyers','Skewness', 
					'Mean_w_outlyers', 'Mean',
					'Median_w_outlyers', 'Median',
					'nr_objects_w_outlyers', 'nr_objects']
	quantiles_range = pd.DataFrame(columns = column_names)

	for week in sorted(log_dates):
		Q1 = df_raw['price_sq_m'][df_raw['week'] == week].quantile(.01) 
		Q2 = df_raw['price_sq_m'][df_raw['week'] == week].quantile(.25) 
		Q3 = df_raw['price_sq_m'][df_raw['week'] == week].quantile(.75) 
		Q4 = df_raw['price_sq_m'][df_raw['week'] == week].quantile(.99)
		Skewness1 = df_raw['price_sq_m'][df_raw['week'] == week].skew()
		Mean1 = df_raw['price_sq_m'][df_raw['week'] == week].mean()
		Median1 = df_raw['price_sq_m'][df_raw['week'] == week].median()
		IQR = Q3 - Q2
		df_temp = df_raw[df_raw['week'] == week]
		#df_temp = df_temp[(df_temp['price_sq_m'] > Q1 - 1.25 * IQR)]
		#df_temp = df_temp[(df_temp['price_sq_m'] < Q3 + 1.25 * IQR)]
		df_temp = df_temp[(df_temp['price_sq_m'] > Q1)]
		df_temp = df_temp[(df_temp['price_sq_m'] < Q3)]
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
	Creates 3 data segmentations:
	1) size segment
	2) district segment
	3) street segment
	'''		

	df['size_segment'] = pd.qcut(df['space_sq_m'], q=3, labels=["small", "medium", "large"])	

	streets = df.groupby('street')['price_sq_m'].agg(['mean'])
	streets['street_rank'] = pd.qcut(streets['mean'], q=5,  labels=[5, 4, 3,2,1])
	df = pd.merge(df, streets['street_rank'], on='street', how='outer')	

	districts = df.groupby('district')['price_sq_m'].agg(['mean'])
	districts['district_rank'] = pd.qcut(districts['mean'], q=5,  labels=[5, 4, 3,2,1])
	df = pd.merge(df, districts['district_rank'], on='district', how='outer')

	#df['size_segment'] = df.size_segment.astype('category').cat.codes
	#df['street_rank'] = df.street_rank.astype('category').cat.codes
	#df['district_rank'] = df.district_rank.astype('category').cat.codes							

	return df




