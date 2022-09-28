from email.policy import default
from tkinter.messagebox import RETRY
import uuid
from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, Float, Date
from sqlalchemy import insert, update, select, delete
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.attributes import InstrumentedAttribute
import pandas as pd

Base = declarative_base()
#Create the database
engine = create_engine('sqlite:///dhl_db.sqlite3')
#create the session
Session = sessionmaker(bind=engine)
sess = Session()

class UserInput(Base):
	__tablename__ = 'client_info'
	Unique_Lead_Assignment_Number = Column(String, primary_key=True, unique=True)
	Lead_Source_Name = Column(String)
	Lead_Source_Details_if_any = Column(String(255))
	Suspect_Creation_date_by_Lead_Originator = Column(Date)
	Suspect_Creation_by_Lead_Originator_Name = Column(String(100))
	Customer_name = Column(String(100), unique=True, nullable=False)
	Address_Line_1 = Column(String(100))
	Address_Line_2 = Column(String(100))
	City = Column(String(50))
	State = Column(String(20))
	Post_Code = Column(Integer)
	Main_Phone = Column(Integer)
	Contact_Person_Name = Column(Integer)
	Contact_Person_Email = Column(String(60))
	Contact_Person_Designation = Column(String(50))
	Contact_Person_Phone = Column(Integer)
	Website = Column(String(50))
	Physical_Channel = Column(String(3))
	SSM_Number_Business_Registration_Number = Column(String(12))
	Competitors = Column(String(20))
	Total_Potential_Revenue_per_Month = Column(Float)
	Industry = Column(String(20))
	Suspect_Accepted_By = Column(String(50))
	Prospect_Accepted_By = Column(String(50))
	Source_Type = Column(String(4))
	Lead_Score = Column(Integer())

	def __repr__(self):
		return super().__repr__()

	def __init__(self, id, src_name, src_detail, sus_crt, sus_name, cust_name,
				addr1, addr2, city, state, postcode, main_phone, cp_name, cp_email,
				cp_pos, cp_phone, website, phy_channel, biz_no, competitors, revenue,
				industry):
		self.Unique_Lead_Assignment_Number = id
		self.Lead_Source_Name = src_name
		self.Lead_Source_Details_if_any = src_detail
		self.Suspect_Creation_date_by_Lead_Originator = sus_crt
		self.Suspect_Creation_by_Lead_Originator_Name = sus_name
		self.Customer_name = cust_name
		self.Address_Line_1 = addr1
		self.Address_Line_2 = addr2
		self.City = city
		self.State = state
		self.Post_Code = postcode
		self.Main_Phone = main_phone
		self.Contact_Person_Name = cp_name
		self.Contact_Person_Email = cp_email
		self.Contact_Person_Designation =cp_pos
		self.Contact_Person_Phone = cp_phone
		self.Website = website
		self.Physical_Channel = phy_channel
		self.SSM_Number_Business_Registration_Number = biz_no
		self.Competitors = competitors
		self.Total_Potential_Revenue_per_Month = revenue
		self.Industry = industry

	def update(self):
		mapped_values = {}
		for item in Base.__dict__.iteritems():
			field_name = item[0]
			field_type = item[1]
			is_column = isinstance(field_type, InstrumentedAttribute)
			if is_column:
				mapped_values[field_name] = getattr(self, field_name)

		sess.query(Base).filter(Base.id == self.id).update(mapped_values)
		sess.commit()

if __name__ == "__main__":
	engine = create_engine('sqlite:///dhl_db.sqlite3')
	Base.metadata.create_all(engine)

def add_data(entry):
	try:
		sess.add(entry)
		sess.commit() #Attempt to commit all the records
	except:
		sess.rollback() #Rollback the changes on error
	finally:
		sess.close() #close the connection


def add_all_data(uploaded_df, load_sel_row,load_src_name,src_name,load_src_detail,src_extra,load_sus_crt,sus_date,load_sus_name,sus_name,
					load_cust_name,load_addr1,load_addr2,load_city,load_state,load_postcode,load_main_phone,load_cp_name,
					load_cp_email,load_cp_pos,load_cp_phone,load_website,load_phy_channel,load_biz_no,load_competitors,
					load_revenue,load_industry):
	for i in range(uploaded_df.shape[0]):
					new_id = uuid.uuid4().hex
					new_src_name = load_sel_row[i][load_src_name] if load_src_name != "" else src_name
					new_src_detail = load_sel_row[i][load_src_detail] if load_src_detail != "" else src_extra
					new_sus_crt = load_sel_row[i][load_sus_crt] if load_sus_crt != "" else sus_date
					new_sus_name = load_sel_row[i][load_sus_name] if load_sus_name != "" else sus_name
					new_cust_name = load_sel_row[i][load_cust_name] if load_cust_name != "" else None
					new_addr1 = load_sel_row[i][load_addr1] if load_addr1 != "" else None
					new_addr2 = load_sel_row[i][load_addr2] if load_addr2 != "" else None
					new_city = load_sel_row[i][load_city] if load_city != "" else None
					new_state = load_sel_row[i][load_state] if load_state != "" else None
					new_postcode = load_sel_row[i][load_postcode] if load_postcode != "" else None
					new_main_phone = load_sel_row[i][load_main_phone] if load_main_phone != "" else None
					new_cp_name = load_sel_row[i][load_cp_name] if load_cp_name != "" else None
					new_cp_email = load_sel_row[i][load_cp_email] if load_cp_email != "" else None
					new_cp_pos = load_sel_row[i][load_cp_pos] if load_cp_pos != "" else None
					new_cp_phone = load_sel_row[i][load_cp_phone] if load_cp_phone != "" else None
					new_website = load_sel_row[i][load_website] if load_website != "" else None
					new_phy_channel = load_sel_row[i][load_phy_channel] if load_phy_channel != "" else None
					new_biz_no = load_sel_row[i][load_biz_no] if load_biz_no != "" else None
					new_competitors = load_sel_row[i][load_competitors] if load_competitors != "" else None
					new_revenue = load_sel_row[i][load_revenue] if load_revenue != "" else None
					new_industry = load_sel_row[i][load_industry] if load_industry != "" else None
					new_entry = UserInput(new_id,new_src_name,new_src_detail,new_sus_crt,new_sus_name,new_cust_name,
								new_addr1,new_addr2,new_city,new_state,new_postcode,new_main_phone,new_cp_name,
								new_cp_email,new_cp_pos,new_cp_phone,new_website,new_phy_channel,new_biz_no,
								new_competitors,new_revenue,new_industry)
					add_data(new_entry)

def view_all_data():
	data = pd.read_sql('SELECT * FROM client_info', sess.bind)
	return data

def view_all_customer():
	data = pd.read_sql_query('SELECT DISTINCT Customer_name FROM client_info', sess.bind)
	return data

def get_customer_record(name):
	data = pd.read_sql_query('SELECT * FROM client_info where Customer_name="{}"'.format(name), sess.bind)
	return data

# def update_data(entry):
# 	sess.execute(update(entry).where(entry.Unique_Lead_Assignment_Number = id)
# 	sess.commit()

def edit_customer_data(id, src_name, src_detail, cust_name,
				addr1, addr2, city, state, postcode, main_phone, cp_name, cp_email,
				cp_pos, cp_phone, website, phy_channel, biz_no, competitors, revenue,
				industry):
	update_record = sess.execute(update(UserInput).
							where(UserInput.Unique_Lead_Assignment_Number == id).
							values(Lead_Source_Name = src_name,
							Lead_Source_Details_if_any = src_detail,
							# Suspect_Creation_date_by_Lead_Originator = sus_crt,
							# Suspect_Creation_by_Lead_Originator_Name = sus_name,
							Customer_name = cust_name,
							Address_Line_1 = addr1,
							Address_Line_2 = addr2,
							City = city,
							State = state,
							Post_Code = postcode,
							Main_Phone = main_phone,
							Contact_Person_Name = cp_name,
							Contact_Person_Email = cp_email,
							Contact_Person_Designation =cp_pos,
							Contact_Person_Phone = cp_phone,
							Website = website,
							Physical_Channel = phy_channel,
							SSM_Number_Business_Registration_Number = biz_no,
							Competitors = competitors,
							Total_Potential_Revenue_per_Month = revenue,
							Industry = industry))
	try:
		sess.commit()
	except:
		sess.rollback()
	finally:
		sess.close()

def delete_data(id):
	sess.execute(delete(UserInput).where(UserInput.Unique_Lead_Assignment_Number == id))
	try:
		sess.commit()
	except:
		sess.rollback()
	finally:
		sess.close()

def create_indexlist(df):
	count_row = df.shape[0]
	index = list()
	for i in range(count_row):
		index.append(i)
	return index

def    cleanup_names(df, name):
	if name != "":
		df[name] = df[name].str.replace('[a-z]', '', regex=True)
		df[name] = df[name].str.replace('[:-@]', '', regex=True)
		df[name] = df[name].str.replace('[!-/]', '', regex=True)
		df[name] = df[name].str.replace(' +', ' ', regex=True)
		df[name] = df[name].str.strip()

def    cleanup_revenue(df, name):
	if name != "":
		df[name] = df[name].str.replace('[a-z]', '', regex=True)
		df[name] = df[name].str.replace('[A-Z]', '', regex=True)
		df[name] = df[name].str.replace('[:-@]', '', regex=True)
		df[name] = df[name].str.replace('[!-/]', '', regex=True)
		df[name] = df[name].str.replace(' +', ' ', regex=True)
		df[name] = df[name].str.strip()

def    cleanup_phone(df, name):
	if name != "":
		df[name] = df[name].str.replace('[a-z]', '', regex=True)
		df[name] = df[name].str.replace('[A-Z]', '', regex=True)
		df[name] = df[name].str.replace('[:-@]', '', regex=True)
		df[name] = df[name].str.replace('[!-/]', '', regex=True)
		df[name] = df[name].str.replace(' +', ' ', regex=True)
		df[name] = df[name].str.strip()