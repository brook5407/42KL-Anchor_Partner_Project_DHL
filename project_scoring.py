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

def	channel(df,weight,max,min):
	data = 'Physical_Channel'
	score = 'Lead_Score'
	df.loc[df[data].isnull(), ['tmp']] = 0
	df.loc[df[data] == 'B2B', ['tmp']] = min
	df.loc[df[data] == 'B2C', ['tmp']] = max
	df.loc[df[score].isnull(), [score]] = 0
	df[score] = df[score] + (df['tmp'] * weight)

def	revenue(df,weight,max,average):
	data = 'Total_Potential_Revenue_per_Month'
	score = 'Lead_Score'
	df.loc[df[data].isnull(), ['tmp']] = 0
	df.loc[df[data] >= average, ['tmp']] = max
	df.loc[df[score].isnull(), [score]] = 0
	df[score] = df[score] + (df['tmp'] * weight)

def	competitors(df,weight,list,max,min):
	data = 'Competitors'
	score = 'Lead_Score'
	df[data] = df[data].fillna("")
	df.loc[df[data] == "", ['tmp']] = 0
	df.loc[df[data].notnull(), ['tmp']] = min
	df.loc[df[data].isin(list), ['tmp']] = max
	df.loc[df[score].isnull(), [score]] = 0
	df[score] = df[score] + (df['tmp'] * weight)

def	designation(df,weight,lv1,lv2,lv3,lv4):
	data = 'Contact_Person_Designation'
	score = 'Lead_Score'
	df[data] = df[data].fillna("")
	df['tmp'] = 0
	director_list = ["Director", "Chief", "President"]
	manager_list = ["Manager","Lead","Supervisor","Administrator"]
	entry_list = ["Intern","Trainee","Assistant","Apprentice","Associate"]

	df.loc[df[data].notnull(), ['tmp']] = lv3
	df['tmp'] = df.apply(lambda x: lv1 if any([item in x[data] for item in director_list]) else x['tmp'], axis=1)
	df['tmp'] = df.apply(lambda x: lv2 if any([item in x[data] for item in manager_list]) else x['tmp'], axis=1)
	df['tmp'] = df.apply(lambda x: lv4 if any([item in x[data] for item in entry_list]) else x['tmp'], axis=1)
	df.loc[df[score].isnull(), [score]] = 0
	df[score] = df[score] + (df['tmp'] * weight)

def contact_available(df, weight, name, phone, email):
	d_name = 'Contact_Person_Name'
	d_phone = 'Contact_Person_Phone'
	d_email = 'Contact_Person_Email'
	score = 'Lead_Score'
	df['tmp'] = 0
	df.loc[df[d_name].notnull(), ['tmp']] += name
	df.loc[df[d_phone].notnull(), ['tmp']] += phone
	df.loc[df[d_email].notnull(), ['tmp']] += email
	df.loc[df[score].isnull(), [score]] = 0
	df[score] = df[score] + (df['tmp'] * weight)

def cust_info_available(df, weight, name, address, postcode, phone):
	d_name = 'Customer_name'
	d_addr = 'Address_Line_1'
	d_postcode = 'Post_Code'
	d_phone = 'Main_Phone'
	score = 'Lead_Score'
	df['tmp'] = 0
	df.loc[df[d_name].notnull(), ['tmp']] += name
	df.loc[df[d_addr].notnull(), ['tmp']] += address
	df.loc[df[d_postcode].notnull(), ['tmp']] += postcode
	df.loc[df[d_phone].notnull(), ['tmp']] += phone
	df.loc[df[score].isnull(), [score]] = 0
	df[score] = df[score] + (df['tmp'] * weight)

def lead_source(df,weight,list,score):
	data = 'Lead_Source_Name'
	score = 'Lead_Score'
	df['tmp'] = 0
	df.loc[df[data].isin(list), ['tmp']] = score
	df.loc[df[score].isnull(), [score]] = 0
	df[score] = df[score] + (df['tmp'] * weight)

def source_type(df, hot, warm, check):
	score = 'Lead_Score'
	type = 'Source_Type'
	df[type] = 'Cold'
	if check == True:
		df.loc[(df['Customer_name'].notnull())&(df['Main_Phone'].notnull())&(df['Contact_Person_Name'].notnull())&(df['Contact_Person_Phone'].notnull())&(df[score]>=warm),[type]] = 'Warm'
		df.loc[(df['Customer_name'].notnull())&(df['Main_Phone'].notnull())&(df['Contact_Person_Name'].notnull())&(df['Contact_Person_Phone'].notnull())&(df[score]>=hot),[type]] = 'Hot'
	else:
		df.loc[df[score]>=warm, [type]] = 'Warm'
		df.loc[df[score]>=hot, [type]] = 'Hot'
	

