from project_orm import *
import streamlit as st
from st_aggrid import AgGrid,GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder
import streamlit_modal as modal
import streamlit.components.v1 as components
from streamlit_option_menu import option_menu
import pandas as pd
from uuid import uuid4
import scoring as sc

with st.sidebar:
	st.image("DHL.jpg",use_column_width=True)
	menu = ["Dashboard","Query","Upload","Scoring", "Convert"]
	icon = ['house', 'gear', 'cloud-upload', "list-task", "card-checklist"]
	choice = option_menu("Lead Generation Enhancement", menu, icons=icon, menu_icon="cast", default_index=1)

if choice == "Dashboard":
	open_add = st.button("Add New Record")
	if open_add:
		modal.open()
	if modal.is_open():
		with modal.container("Add New Record"):
			with st.expander("Lead Information"):
				id = st.text_input("Unique Lead ID", value=uuid4().hex, disabled=True)
				src1,src2 = st.columns(2)
				with src1:
					src_name = st.selectbox("Lead Source Name", ["Current DB", "Exhibition", "Social media", "blogs", "Website", "Referral", "Other"])
				with src2:
					if src_name == "Other":
						src_detail = st.text_input("Lead Source Details, if any")
					else: src_detail = None

				sus1,sus2 = st.columns(2)
				with sus1:
					sus_crt = st.date_input("Suspect Creation date by Lead Originator", value=None, disabled=True)
				with sus2:
					sus_name = st.text_input("Suspect Creation by Lead Originator Name")
			
			with st.expander("Customer information"):
				cust_name = st.text_input("Customer name")
				cust1,cust2 = st.columns(2)
				with cust1:
					addr1 = st.text_input("Address Line 1")
				with cust2:
					addr2 = st.text_input("Address Line 2")
				cust3,cust4 = st.columns(2)
				with cust3:
					city = st.text_input("City")
				with cust4:
					state = st.selectbox("State", [None,"Johor", "Kedah", "Kelantan", "Kuala Lumpur", "Labuan", "Malacca",
										"Negeri Sembilan", "Pahang", "Penang", "Perak", "Perlis", "Putrajaya",
										"Sabah", "Sarawak", "Selangor", "Terengganu"])
				cust5,cust6 = st.columns(2)
				with cust5:
					postcode = st.text_input("Post Code", max_chars=5)
				with cust6:
					main_phone = st.text_input("Main Phone#")

			with st.expander("Contact Person Information"):
				cp1,cp2 = st.columns(2)
				with cp1:
					cp_name = st.text_input("Contact Person Name")
				with cp2:
					cp_email = st.text_input("Contact Person Email")
				cp3,cp4 = st.columns(2)
				with cp3:
					cp_pos = st.selectbox("Contact Person Designation", ["Director & above", "Mid-level manager", "Senior", "Entry Level"])
				with cp4:
					cp_phone = st.text_input("Contact Person Phone No.")
			
			with st.expander("Business Information"):
				bi1,bi2,bi3 = st.columns(3)
				with bi1:
					website = st.text_input("Website")
				with bi2:
					phy_channel = st.selectbox("Physical Channel", ["B2B", "B2C"])
				with bi3:
					biz_no = st.text_input("SSM Number/Business Registration Number")
				bi4,bi5,bi6 = st.columns(3)
				with bi4:
					competitors = st.text_input("Competitors")
				with bi5:
					revenue = st.number_input("Monthly Total Potential Revenue")
				with bi6:
					industry = st.text_input("Industry")

			submit = st.button("Add")

			if submit:
				try:
					entry = UserInput(id,src_name,src_detail,sus_crt,sus_name,cust_name,addr1,
									addr2,city,state,postcode,main_phone,cp_name,cp_email,cp_pos,
									cp_phone,website,phy_channel,biz_no,competitors,revenue,industry)
					add_data(entry)
					st.success("New Lead ID {} added to database".format(id))
					st.experimental_rerun()
				except Exception as e:
					st.error(f"some error occurred : {e}")

	lead_df = view_all_data()
	st.dataframe(lead_df)

elif choice == "Query":
	df = view_all_data()
	gd = GridOptionsBuilder.from_dataframe(df)
	gd.configure_pagination(enabled=True)
	# gd.configure_default_column(editable=True)
	gd.configure_selection(selection_mode='single', use_checkbox=True)
	gridoptions = gd.build()
	grid_table = AgGrid(df, gridOptions=gridoptions,
						update_mode=GridUpdateMode.SELECTION_CHANGED
						)
	sel_row = grid_table["selected_rows"]
	if sel_row:
		id = sel_row[0]["Unique_Lead_Assignment_Number"]
		
	open_edit = st.button("Edit")
	if open_edit and sel_row:
		modal.open()
	if modal.is_open():
		with modal.container("Edit Lead ID - {}".format(id)):
			src_name = sel_row[0]["Lead_Source_Name"]
			src_detail = sel_row[0]["Lead_Source_Details_if_any"]
			cust_name = sel_row[0]["Customer_name"]
			addr1 = sel_row[0]["Address_Line_1"]
			addr2 = sel_row[0]["Address_Line_2"]
			city = sel_row[0]["City"]
			state = sel_row[0]["State"]
			postcode = sel_row[0]["Post_Code"]
			main_phone = sel_row[0]["Main_Phone"]
			cp_name = sel_row[0]["Contact_Person_Name"]
			cp_email = sel_row[0]["Contact_Person_Email"]
			cp_pos = sel_row[0]["Contact_Person_Designation"]
			cp_phone = sel_row[0]["Contact_Person_Phone"]
			website = sel_row[0]["Website"]
			phy_channel = sel_row[0]["Physical_Channel"]
			biz_no = sel_row[0]["SSM_Number_Business_Registration_Number"]
			competitors = sel_row[0]["Competitors"]
			revenue = sel_row[0]["Total_Potential_Revenue_per_Month"]
			industry = sel_row[0]["Industry"]

			src1,src2 = st.columns(2)
			with src1:
				sel_src = [None,"Current DB","Exhibition","Social media","Blogs","Website","Referral","Other"]
				if src_name not in sel_src: sel_src.insert(0, src_name)
				new_src_name = st.selectbox("Lead Source Name", sel_src, index=sel_src.index(src_name))
			with src2:
				new_src_detail = st.text_input("Lead Source Details, if any", value = src_detail) if new_src_name == "Other" else None

			with st.expander("Customer information"):
				new_cust_name = st.text_input("Customer name", value=cust_name)
				cust1,cust2 = st.columns(2)
				with cust1:
					new_addr1 = st.text_input("Address Line 1", value=addr1)
				with cust2:
					new_addr2 = st.text_input("Address Line 2", value=addr2)

				cust3,cust4 = st.columns(2)
				with cust3:
					new_city = st.text_input("City", value=city)
				with cust4:
					sel_state = [None,"Johor", "Kedah", "Kelantan", "Kuala Lumpur", "Labuan", "Malacca",
											"Negeri Sembilan", "Pahang", "Penang", "Perak", "Perlis", "Putrajaya",
											"Sabah", "Sarawak", "Selangor", "Terengganu"]
					if state not in sel_state: state = None
					new_state = st.selectbox("State", sel_state, index = sel_state.index(state))

				cust5,cust6 = st.columns(2)
				with cust5:
					new_postcode = st.text_input("Post Code", value=postcode, max_chars=5)
				with cust6:
					new_main_phone = st.text_input("Main Phone#", value=main_phone)

			with st.expander("Contact Person Information"):
				cp1,cp2 = st.columns(2)
				with cp1:
					new_cp_name = st.text_input("Contact Person Name", value=cp_name)
				with cp2:
					new_cp_email = st.text_input("Contact Person Email", value=cp_email)
				cp3,cp4 = st.columns(2)
				with cp3:
					new_cp_pos = st.text_input("Contact Person Designation", value=cp_pos)
				with cp4:
					new_cp_phone = st.text_input("Contact Person Phone", value=cp_phone)

			with st.expander("Business Information"):
				bi1,bi2,bi3 = st.columns(3)
				with bi1:
					new_website = st.text_input("Website", value=website)
				with bi2:
					phy_list = [None,"B2B", "B2C"]
					new_phy_channel = st.selectbox("Physical Channel", phy_list, index=phy_list.index(phy_channel))
				with bi3:
					new_biz_no = st.text_input("SSM Number/Business Registration Number", value=biz_no)
				bi4,bi5,bi6 = st.columns(3)
				with bi4:
					new_competitors = st.text_input("Competitors", value=competitors)
				with bi5:
					new_revenue = st.number_input("Monthly Total Potential Revenue", value=revenue if revenue is not None else 0)
				with bi6:
					new_industry = st.text_input("Industry", value=industry)
			edit = st.button("Edit info")
			if edit:
				try:
					edit_customer_data(id,new_src_name,new_src_detail,new_cust_name,new_addr1,new_addr2,new_city,
									new_state,new_postcode,new_main_phone,new_cp_name,new_cp_email,new_cp_pos,
									new_cp_phone,new_website,new_phy_channel,new_biz_no,new_competitors,
									new_revenue,new_industry)
					st.success("New Lead ID {} has been edited".format(id))
				except Exception as e:
					st.error(f"some error occurred : {e}")
	delete = st.button("Delete")
	if delete and sel_row:
		try:
			delete_data(id)
			st.success("New Lead ID {} has been deleted".format(id))
			st.experimental_rerun()
		except Exception as e:
				st.error(f"some error occurred : {e}")

elif choice == "Upload":
	st.subheader("Upload Dataset")

	uploaded_file = st.file_uploader("Choose a CSV file")
	if uploaded_file is not None:
		uploaded_df = pd.read_csv(uploaded_file)
		df_col = list(uploaded_df.columns)
		df_col.insert(0,"")
		st.empty()
		st.sidebar.subheader("Dataset Information Available")
		load_cust_name = st.sidebar.selectbox("Customer Name", df_col)
		cleanup_names(uploaded_df, load_cust_name)
		load_addr1 = st.sidebar.selectbox("Address Line 1", df_col)
		load_addr2 = st.sidebar.selectbox("Address Line 2", df_col)
		load_city = st.sidebar.selectbox("City", df_col)
		load_state = st.sidebar.selectbox("State", df_col)
		load_postcode = st.sidebar.selectbox("Post Code", df_col)
		cleanup_postcode(uploaded_df,load_postcode)
		load_main_phone = st.sidebar.selectbox("Main Phone#", df_col)
		cleanup_phone(uploaded_df,load_main_phone)
		load_cp_name = st.sidebar.selectbox("Contact Person Name", df_col)
		load_cp_email = st.sidebar.selectbox("Contact Person Email", df_col)
		load_cp_pos = st.sidebar.selectbox("Contact Person Designation", df_col)
		load_cp_phone = st.sidebar.selectbox("Contact Person Phone", df_col)
		cleanup_phone(uploaded_df,load_cp_phone)
		load_website = st.sidebar.selectbox("Website", df_col)
		load_phy_channel = st.sidebar.selectbox("Physical Channel", df_col)
		load_biz_no = st.sidebar.selectbox("SSM Number/Business Registration Number", df_col)
		load_competitors = st.sidebar.selectbox("Competitiors", df_col)
		load_revenue = st.sidebar.selectbox("Monthly Total Potential Revenue", df_col)
		cleanup_revenue(uploaded_df, load_revenue)
		load_industry = st.sidebar.selectbox("Industry", df_col)
		uploaded_gd = GridOptionsBuilder.from_dataframe(uploaded_df)
		uploaded_gd.configure_selection(selection_mode='multiple',
										use_checkbox=True,
										pre_selected_rows=create_indexlist(uploaded_df))
		uploaded_gd.configure_pagination(enabled=True)
		uploaded_gd.configure_default_column(editable=True, groupable=True)
		gridoptions = uploaded_gd.build()
		grid_table = AgGrid(uploaded_df, gridOptions=gridoptions,
						update_mode=GridUpdateMode.SELECTION_CHANGED,
						reload_data=True)
		load_sel_row = grid_table["selected_rows"]
		sel_name = ["Current DB", "Exhibition", "Social media", "blogs", "Website", "Referral", "Other"]
		src_name_input = st.selectbox("Lead Source Name", sel_name)
		src_extra = st.text_input("Lead Source if any") if src_name_input == "Other" else None
		extra1,extra2 = st.columns(2)
		with extra1:
			load_sus_crt_input = st.date_input("Suspect Creation date by Lead Originator",value=None,disabled=True)
		with extra2:
			load_sus_name_input = st.text_input("Suspect Creation by Lead Originator Name")
		add_all = st.button("Add")
		if add_all:
			try:
				add_all_data(load_sel_row,src_name_input,src_extra,load_sus_crt_input,load_sus_name_input,
					load_cust_name,load_addr1,load_addr2,load_city,load_state,load_postcode,load_main_phone,load_cp_name,
					load_cp_email,load_cp_pos,load_cp_phone,load_website,load_phy_channel,load_biz_no,load_competitors,
					load_revenue,load_industry)
				st.success("successful upload {} to database".format(uploaded_file))
			except Exception as e:
				st.error(f"some error occurred : {e}")

elif choice == "Scoring":
	df_scoring = pd.DataFrame(view_all_data())
	df_sel = st.radio("Scoring for:", ["All","Unapprove Suspect","Unapprove Prospect"])
	if df_sel == "Unapprove Suspect":
		df_scoring = df_scoring[df_scoring.Suspect_Accepted_By.isnull()]
	if df_sel == "Unapprove Prospect":
		df_scoring = df_scoring[df_scoring.Suspect_Accepted_By.notnull()]
		df_scoring = df_scoring[df_scoring.Prospect_Accepted_By.isnull()]
	st.sidebar.subheader("Scoring Model")
	conditions = ["Revenue", "Physical Channel", "Competitors", "Contact Person Designation"]
	options = st.multiselect("Rules to score",conditions)
	if options:
		df_scoring['Lead_Score'] = 0
	if "Revenue" in options:
		with st.sidebar.expander("Revenue Rules"):
			average_revenue = st.number_input("Minimum Revenue required to achieve higher score", value = 10000, max_value=None,min_value=0)
			max_revenue = st.number_input("max score",max_value=100,min_value=0, value=5, key="max score for revenue")
			min_revenue = st.number_input("min score",max_value=100,min_value=0, value=1, key="min score for revenue")
			weight_revenue = st.slider("Choose the weight for revenue scoring",max_value=1.0,value=1.0)
		sc.revenue(df_scoring,weight_revenue,max_revenue,min_revenue,average_revenue)

	if "Physical Channel" in options:
		with st.sidebar.expander("Physical Channel Rules"):
			max_pc = st.number_input("score if B2C",max_value=100,min_value=0, value=5)
			min_pc = st.number_input("score if B2B",max_value=100,min_value=0, value=1)
			weight_pc = st.slider("Choose the weight for weight scoring",max_value=1.0,value=1.0)
		sc.channel(df_scoring,weight_pc,max_pc,min_pc)

	if "Competitors" in options:
		with st.sidebar.expander("Competitors Rules"):
			cmp_sel = ["FedEx","J&T Express", "Lalamove", "Ninjavan", "GDEX", "Skynet", "PosLaju", "ABX Express", "EasyParcel", "Pgeon", "CityLink"]
			cmp_list = st.multiselect("Competitors to achieve higher score",cmp_sel)
			max_cmp = st.number_input("max score",max_value=100,min_value=0, value=5, key="max score for competitor")
			min_cmp = st.number_input("min score",max_value=100,min_value=0, value=1, key="min score for competitor")
			weight_cmp = st.slider("Choose the weight for competitors scoring",max_value=1.0,value=1.0)			
		sc.competitors(df_scoring,weight_cmp,cmp_list,max_cmp,min_cmp)

	if "Contact Person Designation" in options:
		with st.sidebar.expander("Contact Person Designation"):
			lv1 = st.number_input("score for Director & above", max_value=100, value=10)
			lv2 = st.number_input("score for Mid-level manager", max_value=100, value=8)
			lv3 = st.number_input("score for Senior", max_value=100, value=8)
			lv4 = st.number_input("score for Entry Level", max_value=100, value=8)
			weight_dsig = st.slider("Choose the weight for competitors scoring",max_value=1.0,value=1.0)
		sc.designation(df_scoring,weight_dsig,lv1,lv2,lv3,lv4)

	if "tmp" in df_scoring:
		del df_scoring['tmp']
	df1 = df_scoring[['Unique_Lead_Assignment_Number','Customer_name','Lead_Score']]
	# df1['Lead_Score'] = df1['Lead_Score'].astype(int)
	st.dataframe(df1)
	submit_scoring = st.button("Save", key="submit score")

	if submit_scoring:
		for index, row in df_scoring.iterrows():
			try:
				update_scoring(row[0],row[-1])
			except Exception as e:
					st.error(f"some error occurred : {e}")
		st.success("New Scoring Model have been updated")
				
elif choice == "Convert":
	tab1,tab2 = st.tabs(["Suspect Approve", "Prospect Approve"])
	with tab1:
		df_convert_sus = pd.DataFrame(view_all_data())
		df_convert_sus = df_convert_sus[df_convert_sus.Suspect_Accepted_By.isnull()]
		df_convert_sus = df_convert_sus[['Unique_Lead_Assignment_Number', 'Customer_name','Lead_Score']]
		gd_sus = GridOptionsBuilder.from_dataframe(df_convert_sus)
		gd_sus.configure_selection(selection_mode='multiple',
										use_checkbox=True)
		gd_sus.configure_pagination(enabled=True)
		gd_sus.configure_grid_options(enableCellTextSelection=True)
		gd_sus.configure_grid_options(ensureDomOrder=True)
		gd_sus.configure_default_column(groupable=True)
		gridoptions = gd_sus.build()
		table_sus = AgGrid(df_convert_sus, gridOptions=gridoptions,
						update_mode=GridUpdateMode.SELECTION_CHANGED)
		sel_sus = table_sus["selected_rows"]
		sus_input = st.text_input("Approved by:", key="suspect input")
		submit_sus = st.button("Approve", key="suspect submit")
		if submit_sus and sel_sus:
			if sus_input == "":
				st.error("Please fill out the name for approve.")
			else:
				for i in sel_sus:
					sus_id = i["Unique_Lead_Assignment_Number"]
					update_suspect_approve(sus_id, sus_input)
				st.success("Selected receords have been Approved")
				st.experimental_rerun()

	with tab2:
		df_convert_pro = pd.DataFrame(view_all_data())
		df_convert_pro = df_convert_pro[df_convert_pro.Suspect_Accepted_By.notnull()]
		df_convert_pro = df_convert_pro[df_convert_pro.Prospect_Accepted_By.isnull()]
		df_convert_pro = df_convert_pro[['Unique_Lead_Assignment_Number', 'Customer_name','Lead_Score']]
		gd_pro = GridOptionsBuilder.from_dataframe(df_convert_pro)
		gd_pro.configure_selection(selection_mode='multiple',
										use_checkbox=True)
		gd_pro.configure_pagination(enabled=True)
		gd_pro.configure_default_column(editable=True, groupable=True)
		gridoptions = gd_pro.build()
		table_pro = AgGrid(df_convert_pro, gridOptions=gridoptions,
						update_mode=GridUpdateMode.SELECTION_CHANGED)
		sel_pro = table_pro["selected_rows"]
		pro_input = st.text_input("Approved by:", key="prospect input")
		submit_pro = st.button("Approve", key="prospect submit")
		if submit_pro and sel_pro:
			if pro_input == "":
				st.error("Please fill out the name for approve.")
			else:
				for i in sel_pro:
					pro_id = i["Unique_Lead_Assignment_Number"]
					update_prospect_approve(pro_id, pro_input)
				st.success("Selected receords have been Approved")
				st.experimental_rerun()