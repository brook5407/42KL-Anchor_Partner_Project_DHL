import pandas as pd
import recordlinkage.compare
from recordlinkage.index import Block, SortedNeighbourhood
import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize.treebank import TreebankWordDetokenizer
from thefuzz import process
from project_orm import *
import re

# import requests
nltk.download('punkt')


def deduplicate_data(df):
	df = df.where(pd.notnull(df), None)
	name_stopword = ["SDN", "SB", "BHD", "LTD", 'LIMITED', "CO", "COMPANY"]
	df ['cust_name_token'] = df['Customer_name'].apply(word_tokenize)
	df['cust_name_clean'] = df['cust_name_token'].apply(lambda x: [word for word in x if word not in name_stopword])
	df ['cust_name_clean'] = df['cust_name_clean'].apply(TreebankWordDetokenizer().detokenize) 
	Block_Index_by_State = Block(on="State")
	Block_Index_by_State_Pairs = Block_Index_by_State.index(df)
	Neighbour_Index_by_Name = SortedNeighbourhood(on="Customer_name", window = 5)
	Neighbour_Index_by_Name_Pairs = Neighbour_Index_by_Name.index(df)
	All_Index_Pairs = Block_Index_by_State_Pairs.append(Neighbour_Index_by_Name_Pairs)
	All_Index_Pairs = All_Index_Pairs.drop_duplicates(keep='first')
	compare = recordlinkage.Compare()
	compare.string('cust_name_clean','cust_name_clean', label = 'name_score', threshold=0.8)
	compare.exact('Post_Code','Post_Code', label = 'postcode_score')
	comparison_vectors = compare.compute(All_Index_Pairs,df)
	matches = comparison_vectors[comparison_vectors.sum(axis=1) >= 2]
	keep_indices = matches.index.get_level_values(1)
	dup_indices = matches.index.get_level_values(0)
	keep = df[df.index.isin(keep_indices)].sort_values(by='Customer_name')
	dup = df[df.index.isin(dup_indices)].sort_values(by='Customer_name')
	del dup['cust_name_token']
	del keep['cust_name_token']
	del dup['cust_name_clean']
	del keep['cust_name_clean']
	keep_list= keep.values.tolist()
	dup_list = dup.values.tolist()
	for i in range(len(keep_list)):
		delete_data(dup_list[i][0])
		for j in range(len(keep_list[i])):
			if keep_list[i][j] is None or keep_list[i][j] == "":
				# column = keep.columns[j]
				edit_single_data(keep_list[i][0], keep.columns[j], dup_list[i][j])

def	cleanup_names(df, name):
	if name != "":
		df[name] = df[name].astype(str)
		df[name] = df[name].str.upper()
		df[name] = df[name].str.replace('[:-@]', '', regex=True)
		df[name] = df[name].str.replace('[!-/]', '', regex=True)
		df[name] = df[name].str.replace(' +', ' ', regex=True)
		df[name] = df[name].str.strip()

def cleanup_state(df,name):
	if name != "":
		df[name] = df[name].astype(str)
		df[name] = df[name].str.upper()
		df[name] = df[name].str.replace('[:-@]', '', regex=True)
		df[name] = df[name].str.replace('[!-/]', '', regex=True)
		df[name] = df[name].str.replace(' +', ' ', regex=True)
		df[name] = df[name].str.strip()

def cleanup_email(df,name):
	pattern = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
	if name != "":
		df[name] = df[name].astype(str)
		df[name] = df[name].str.strip()
		df[name] = df[name].apply(lambda x: x if pattern.match(x) else None)

def cleanup_website(df,name):
	pattern = re.compile(r"(^[a-zA-Z0-9_.+-]+\.[a-zA-Z0-9-.]+$)")
	if name != "":
		df[name] = df[name].astype(str)
		df[name] = df[name].str.strip()
		df[name] = df[name].apply(lambda x: x if pattern.match(x) else None)
		# df[name] = df[name].apply(lambda x: x if x != None and requests.get('http://'+x, verify=False, allow_redirects=True, timeout=None).status_code == 200 else None)

def	cleanup_revenue(df, name):
	if name != "":
		if df[name].dtype == object and isinstance(df.iloc[0][name], str):
			df[name] = df[name].str.replace('[a-z]','', regex=True)
			df[name] = df[name].str.replace('[A-Z]','', regex=True)
			df[name] = df[name].str.replace('[:-@]','', regex=True)
			df[name] = df[name].str.replace('[!-,]','', regex=True)
			df[name] = df[name].str.replace('/','', regex=True)
			df[name] = df[name].str.replace(' +',' ', regex=True)
			df[name] = df[name].str.strip()
			df[name] = df[name].astype(int)

def cleanup_postcode(df,name):
	if name != "":
		df[name] = df[name].astype(str)
		df[name] = df[name].str.strip()
		df[name] = df[name].str.findall('[0-9]+')
		df[name] = df[name].str.join("")
		df[name] = df[name].fillna("")

def	cleanup_phone(df, name):
	if name != "":
		df[name] = df[name].astype(str)
		df[name] = df[name].str.strip()
		df[name] = df[name].str.findall('[0-9]+')
		df[name] = df[name].str.join("")
		df[name] = df[name].fillna("")

def	cleanup_competitor(df, name):
	if name != "":
		df[name] = df[name].astype(str)
		df[name] = df[name].str.replace('[:-@]', '', regex=True)
		df[name] = df[name].str.replace('[!-/]', '', regex=True)
		df[name] = df[name].str.replace(' +', ' ', regex=True)
		df[name] = df[name].str.strip()

def cleanup_additional_info(df, name):
	if name != "":
		df[name] = df[name].astype(str)
		df[name] = df[name].str.strip()
		df[name] = df[name].apply(lambda x: name + ': ' + x)

def	remapping_competitors(df, name):
	cleanup_competitor(df,name)
	if name != "":
		competitors = ["FedEx","J&T", "Ninjavan", "GDEX", "Skynet", "PosLaju", "CityLink",'GD Express', 'Janio', 'J&T express']
		for competitor in competitors:
			matches = process.extract(competitor, df[name], limit=10)
			for match in matches:
				if match[1] >= 80:
					df.loc[df[name] == match[0], name] = competitor

def	remapping_state(df,name):
	cleanup_state(df,name)
	if name != "":
		all_state = ["JOHOR", "KEDAH", "KELANTAN", "KUALA LUMPUR", "LABUAN", "MALAKA","NEGERI SEMBILAN", "PAHANG", "PENANG",
				"PERAK","PERLIS","PUTRAJAYA","SABAH", "SARAWAK", "SELANGOR", "TERENGGANU"]
		for state in all_state:
			matches = process.extract(state, df[name], limit=16)
			for match in matches:
				if match[1] >= 80:
					df.loc[df[name] == match[0], name] = state

def create_indexlist(df):
	count_row = df.shape[0]
	index = list()
	for i in range(count_row):
		index.append(i)
	return index
