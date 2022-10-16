from uuid import uuid4
from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, Float, Date
from sqlalchemy import insert, update, select, delete
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.attributes import InstrumentedAttribute
import pandas as pd
import numpy as np
from datetime import date 

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
	Post_Code = Column(String(5))
	Main_Phone = Column(String(12))
	Contact_Person_Name = Column(String(60))
	Contact_Person_Email = Column(String(60))
	Contact_Person_Designation = Column(String(50))
	Contact_Person_Phone = Column(String(12))
	Website = Column(String(50))
	Physical_Channel = Column(String(3))
	SSM_Number_Business_Registration_Number = Column(String(12))
	Competitors = Column(String(20))
	Total_Potential_Revenue_per_Month = Column(Integer)
	Industry = Column(String(20))
	Suspect_Accepted_By = Column(String(50))
	Suspect_Accepted_At = Column(Date)
	Prospect_Accepted_By = Column(String(50))
	Prospect_Accepted_At = Column(Date)
	Source_Type = Column(String(4))
	Lead_Score = Column(Float)

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


def add_all_data(load_sel_row,src_name,src_extra,sus_date,sus_name,
					load_cust_name,load_addr1,load_addr2,load_city,load_state,load_postcode,load_main_phone,load_cp_name,
					load_cp_email,load_cp_pos,load_cp_phone,load_website,load_phy_channel,load_biz_no,load_competitors,
					load_revenue,load_industry):
	for i in load_sel_row:
					new_id = uuid4().hex
					new_cust_name = i[load_cust_name] if load_cust_name != "" else None
					new_addr1 = i[load_addr1] if load_addr1 != "" else None
					new_addr2 = i[load_addr2] if load_addr2 != "" else None
					new_city = i[load_city] if load_city != "" else None
					new_state = i[load_state] if load_state != "" else None
					new_postcode = i[load_postcode] if load_postcode != "" else None
					new_main_phone = i[load_main_phone] if load_main_phone != "" else None
					new_cp_name = i[load_cp_name] if load_cp_name != "" else None
					new_cp_email = i[load_cp_email] if load_cp_email != "" else None
					new_cp_pos = i[load_cp_pos] if load_cp_pos != "" else None
					new_cp_phone = i[load_cp_phone] if load_cp_phone != "" else None
					new_website = i[load_website] if load_website != "" else None
					new_phy_channel = i[load_phy_channel] if load_phy_channel != "" else None
					new_biz_no = i[load_biz_no] if load_biz_no != "" else None
					new_competitors = i[load_competitors] if load_competitors != "" else None
					new_revenue = i[load_revenue] if load_revenue != "" else None
					new_industry = i[load_industry] if load_industry != "" else None
					new_entry = UserInput(new_id,src_name,src_extra,sus_date,sus_name,new_cust_name,
								new_addr1,new_addr2,new_city,new_state,new_postcode,new_main_phone,new_cp_name,
								new_cp_email,new_cp_pos,new_cp_phone,new_website,new_phy_channel,new_biz_no,
								new_competitors,new_revenue,new_industry)
					add_data(new_entry)

def view_all_data():
	df = pd.read_sql('SELECT * FROM client_info', sess.bind)
	return df

def view_scoring_item():
	df = pd.read_sql_query('SELECT Unique_Lead_Assignment_Number, Customer_name, Lead_Score FROM client_info', sess.bind)
	return df

def view_all_customer():
	data = pd.read_sql_query('SELECT DISTINCT Customer_name FROM client_info', sess.bind)
	return data

def get_customer_record(name):
	data = pd.read_sql_query('SELECT * FROM client_info where Customer_name="{}"'.format(name), sess.bind)
	return data

def edit_single_data(id, column, value):
	sess.execute(update(UserInput).where(UserInput.Unique_Lead_Assignment_Number == id).
				values(column = value))
	try:
		sess.commit()
	except:
		sess.rollback()
	finally:
		sess.close()

def edit_customer_data(id, src_name, src_detail, cust_name,
				addr1, addr2, city, state, postcode, main_phone, cp_name, cp_email,
				cp_pos, cp_phone, website, phy_channel, biz_no, competitors, revenue,
				industry):
	sess.execute(update(UserInput).where(UserInput.Unique_Lead_Assignment_Number == id).
				values(Lead_Source_Name = src_name,
						Lead_Source_Details_if_any = src_detail,
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

def update_scoring(id, score):
	sess.execute(update(UserInput).where(UserInput.Unique_Lead_Assignment_Number == id).
				values(Lead_Score = score))
	try:
		sess.commit()
	except:
		sess.rollback()
	finally:
		sess.close()

def update_suspect_approve(id, name):
	sess.execute(update(UserInput).where(UserInput.Unique_Lead_Assignment_Number == id).
				values(Suspect_Accepted_By = name, Suspect_Accepted_At = date.today()))
	try:
		sess.commit()
	except:
		sess.rollback()
	finally:
		sess.close()

def update_prospect_approve(id, name):
	sess.execute(update(UserInput).where(UserInput.Unique_Lead_Assignment_Number == id).
				values(Prospect_Accepted_By = name, Prospect_Accepted_At = date.today()))
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
