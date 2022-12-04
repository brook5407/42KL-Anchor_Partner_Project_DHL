<h1 align="center">
	 🚚Lead Generation Enhancement
</h1>

<p align="center">
	<b><i>Because Swap_push isn’t as natural</i></b><br>
</p>

<p align="center">
	<img alt="GitHub repo size" src="https://img.shields.io/github/repo-size/brook5407/42KL-Anchor_Partner_Project_DHL">
	<img alt="Lines of code" src="https://img.shields.io/tokei/lines/github/brook5407/42KL-Anchor_Partner_Project_DHL">
	<img alt="GitHub language count" src="https://img.shields.io/github/languages/count/brook5407/42KL-Anchor_Partner_Project_DHL">
	<img alt="GitHub top language" src="https://img.shields.io/github/languages/top/brook5407/42KL-Anchor_Partner_Project_DHL">
	<img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/brook5407/42KL-Anchor_Partner_Project_DHL">
</p>

<h3 align="center">
	<a href="#-about">About</a>
	<span> · </span>
	<a href="#%EF%B8%8F-project-context">Context</a>
	<span> · </span>
	<a href="#-feature">Feature</a>
	<span> · </span>
	<a href="#-install">Install</a>
	<span> · </span>
	<a href="#-architecture">Architecture</a>
</h3>

---

## 💻 About

> Development of a prototype tool that will be able to support DHL Express operation team’s lead generation process.

## 🛠️ Project Context

DHL Express aspires to build a clean B2B database of 400,000 to 500,000 customers through various touchpoints (e.g. customer service, operations, etc.) As part of its operational enhancement, the company is seeking to develop a tool that can better assist in their B2B lead generation.

**Current Pain Points:**
- Information on the suspects is unstructured – no consistent format on data input
- Further filtration from suspects to prospects, and conversion from prospects to customers are done through mass/broad-based strategies (e.g. telemarketing team disseminating general marketing materials to all suspects)

**Goals:**
- The tool is to be able to systematically clean, score, and prioritize existing customer lead data
- The tool should help DHL Express to better target its leads and convert them to customers

## 💡 Feature

**Dashboard:**
- Data Visualisation - User able to visualise the current performance of the Suspect from 
	- pie chart - Report the percentage of suspect has been approved, precentage of record from lead source, percentage of imcomplete record in the database
	- line chart - Report the number of record has updated follow by date
	- Table - Read all the record from database

![Dashboard](https://user-images.githubusercontent.com/100013115/205224278-0450e90e-1334-42ef-a960-baee1bea3666.gif)
- Add Record Function - User could mannually fill out the suspect information and add to database.

![Add function](https://user-images.githubusercontent.com/100013115/205224325-412f00dc-3dcb-4193-9d40-461cab0738e3.gif)

**Query**
- Group by and sort function - User able to sort the table or group the table.

![table function](https://user-images.githubusercontent.com/100013115/205224528-d22bf633-9205-4a48-9f38-5487c2735e10.gif)
- Export function - User able to export the table to csv or xlxl format.

![Export database dataset](https://user-images.githubusercontent.com/100013115/205224582-fb4a07f3-aebd-417f-92e8-e545ed90185b.jpg)
- Deduplicate function - Remove duplicate record by compared the name (similarity more than 80%) and postcode (similarity 100%), duplicate record will recplace any None value column automatically and update to database.

![Deduplicate function](https://user-images.githubusercontent.com/100013115/205224622-de1c9f7a-c430-45fd-8ac7-a6468c7326c3.jpg)
- Edit function - Edit any selected record manually.
- Delete function - Delete any selected record manually.

![Edit   delete function](https://user-images.githubusercontent.com/100013115/205224715-55c00813-5eea-4627-ba21-55ff8717804d.jpg)

**Upload**
- Upload function - Only accept csv format file to be uploaded.
- Match function - User required to match the available information from the uploaded dataset.

![Upload function](https://user-images.githubusercontent.com/100013115/205224847-ecf77f88-14f0-4622-b662-9afa5cb570db.jpg)

**Scoring**
- Rule function - User able to select favour scoring method to score the suspect.
- Configure Scoring Model - User able to configure the score for every rule. (Default amount has been provided)
- Lead type function - User able to set the minimum amount to reach certain level lead type.
- Save fuction - Once the score has been setted, User could save the score and will updated to database.

![Scoring](https://user-images.githubusercontent.com/100013115/205225724-8ca96e31-63f7-47a9-9dcb-efa503d348d0.jpg)

**Convert**
- Convert function - User able to select the record that meet the criteria to convert the suspect to prospect

![Convert function](https://user-images.githubusercontent.com/100013115/205226870-f70d345e-adf1-4cf2-bddc-20164fc14da9.jpg)

## ⏳ install

1. Install pip (if its not installed) `sudo apt-get install python3-pip`
2. Install virtualenv `sudo pip3 install virtualenv`
3. Create a virtualenv `virtualenv dhl_env`
4. Activate your virtualenv `source dhl_env/bin/activate`
5. Install the libraries from the requirements file: `pip install -r requirements.txt`
6. run the web apps `streamlit run app.py`

Test run using streamlit cloud: https://brook5407-anchor-partner-project---dhl-app-73qbr6.streamlit.app/

## 🧱 Architecture

- Framework: Streamlit
- Database: Sqlite
- Language: Python

