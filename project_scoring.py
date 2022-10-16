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

def	revenue(df,weight,max,min,average):
	data = 'Total_Potential_Revenue_per_Month'
	score = 'Lead_Score'
	df.loc[df[data].isnull(), ['tmp']] = 0
	df.loc[df[data] > average, ['tmp']] = max
	df.loc[df[data] <= average, ['tmp']] = min
	df.loc[df[score].isnull(), [score]] = 0
	df[score] = df[score] + (df['tmp'] * weight)

def	competitors(df,weight,list,max,min):
	data = 'Competitors'
	score = 'Lead_Score'
	df.loc[df[data].isnull(), ['tmp']] = 0
	df.loc[df[data].notnull(), ['tmp']] = min
	df.loc[df[data].isin(list), ['tmp']] = max
	df.loc[df[score].isnull(), [score]] = 0
	df[score] = df[score] + (df['tmp'] * weight)

def	designation(df,weight,lv1,lv2,lv3,lv4):
	data = 'Contact_Person_Designation'
	score = 'Lead_Score'
	df['tmp'] = 0
	director_above = ["Director", "Chief", "President"]
	manager = ["Manager","Lead","Supervisor","Administrator"]
	entry = ["Intern","Trainee","Assistant","Apprentice","Associate"]

	df.loc[df[data].notnull(), ['tmp']] = lv3
	for match in entry:
		df.loc[df[data].str.contains(match).any(),['tmp']] = lv4
	for match in manager:
		df.loc[df[data].str.contains(match).any(),['tmp']] = lv2
	for match in director_above:
		df.loc[df[data].str.contains(match).any(),['tmp']] = lv1
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
