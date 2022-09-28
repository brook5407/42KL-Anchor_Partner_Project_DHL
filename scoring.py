'''
We go with addictive scoring. We don't want one factor to hugely affect the rest of the others.
scoring factors:
1. Physical channel - B2B will more prefer DHL
as it is more safe and more experienced in dealing with any problems happening
2. Total Potential Revenue/Month - higher the better
3. Contact person designation - higher the better
4. Rural/urban address(?) - if we can. Urban better.
5. Industry - the more fragile / high-cost / seasonal the better.
6. Source type - the warmer the better.
'''
# def	setscore_revenue(df):
# 	df.loc[df['Revenue per month'] > 24999, ['tmp']] = 10
# 	df.loc[df['Revenue per month'] < 25000, ['tmp']] = 8
# 	df.loc[df['Revenue per month'] < 14999, ['tmp']] = 6
# 	df.loc[df['Revenue per month'] < 9999, ['tmp']] = 4
# 	df.loc[df['Revenue per month'].isnull(), ['tmp']] = 2
# 	df.loc[df['Revenue per month'] < 4999, ['tmp']] = 2
# 	df['Rank'] = round(df['Rank'] + df['tmp'], 1)

# def	setscore_seasonality(df):
# 	df.loc[df['Seasonality'] == 'seasonal', ['tmp']] = 1.0
# 	df.loc[df['Seasonality'] == 'non-seasonal', ['tmp']] = 0.8
# 	df.loc[df['Seasonality'].isnull(), ['tmp']] = 0.8
# 	df['Rank'] = round(df['Rank'] * df['tmp'], 1)

def	setscore_weight(df):
	df.loc[df['Avg weight per package'] > 19.99, ['tmp']] = 1.0
	df.loc[df['Avg weight per package'] < 00.51, ['tmp']] = 0.2
	df.loc[df['Avg weight per package'].isnull(), ['tmp']] = 0.2

#+10 if phone intact.
#+2 if phone missing or incomplete
#def	setscore_phone(df):

#we start here
def	channel(df):
	data = 'Physical Channel'
	df.loc[df[data] == 'B2B', ['tmp']] = 10
	df.loc[df[data] == 'B2C', ['tmp']] = 8
	df['SCORE'] = df['SCORE'] + df['tmp']

def	revenue(df):
	data = 'Total Potential Revenue/Month'
	df[data] = df[data].astype(str).str.replace('[A-Z]', '', regex=True)
	df[data] = df[data].astype(str).str.replace(' ', '', regex=True)
	df[data] = df[data].astype(str).str.replace(',', '', regex=True)
	df.loc[df[data].astype(int) > 24999, ['tmp']] = 10
	df.loc[df[data].astype(int) < 25000, ['tmp']] = 8
	df.loc[df[data].astype(int) < 14999, ['tmp']] = 6
	df.loc[df[data].astype(int) < 9999, ['tmp']] = 4
	df.loc[df[data].astype(int).isnull(), ['tmp']] = 2
	df.loc[df[data].astype(int) < 4999, ['tmp']] = 2
	df['SCORE'] = df['SCORE'] + df['tmp']

# there must be a blank as well.
# default sample data given has no designation for competitors.
# for now no distinctions are made between which competitor is more significant for DHL.
# However, no competitor mean that DHL might have an easier time persuading these prospects to become leads.
def	competitors(df):
	data = 'Competitors'
	df.loc[df[data].isnull(), ['tmp']] = 5
	df.loc[df[data].astype(str).notnull(), ['tmp']] = 2
	df['SCORE'] = df['SCORE'] + df['tmp']

def	setscore(df):
	df['SCORE'] = 0
	#designation(df)// higher level better for DHL, SQ will fill and then we score
	channel(df)
	competitors(df)
	revenue(df)
	#industry(df) - should be a drop down menu for this to be scored
	#sourcetype(df)
	#leadpriority(df)
	del df['tmp']