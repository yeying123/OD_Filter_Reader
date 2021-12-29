
from collections import namedtuple
import math
import pandas as pd
import streamlit as st
import base64

st.set_page_config(
     page_title="OD Selection from Remix",
     layout="wide",
     initial_sidebar_state="expanded")
st.sidebar.title('OD Selection from Remix')

# Input field to ask for Remix link to extract IDs
st.sidebar.header('Step 1: Add Remix Link')
title = st.sidebar.text_input('Remix Link:', 'Copy URL')

# Ask to upload file
st.sidebar.header('Step 2: Upload the OD data here')
st.sidebar.markdown('Make sure the csv file with these columns: "origin", "destination", and "count"')
st.sidebar.markdown('Note: select one file only')
uploaded_files = st.sidebar.file_uploader('Choose a CSV file', accept_multiple_files=True, type=['csv'])

# Ask to specify delimiter
st.sidebar.header('Step 3: Specify delimiter')
delimit=st.sidebar.text_input('Delimiter in csv file:', ';')

# Read IDs in the link
if title.find("od=destination")>0:
     from_='destination'
     to_='origin'
     ID_start=title.find("od=destination")+15
     ID=title[ID_start:]
     st.write('The ID(s): ',ID )
else:
     from_='origin'
     to_='destination'
     ID_start=title.find("od=origin")+10
     ID=title[ID_start:]
     st.write('The ID(s): ',ID )

# create empty dataframe (table)
table=pd.DataFrame()

# Generate the aggregated table
ID_list=ID.split(",")
if uploaded_files != []:
     for i in uploaded_files:
          df=pd.read_csv(i,delimiter=delimit)
          for t in ID_list:
               if int(t) in df[from_].values:
                    number=int(t)
                    df1=df.loc[df[from_]==number]
                    table=table.append(df1)
     
     def get_table_download_link(df):
               """Generates a link allowing the data in a given panda dataframe to be downloaded
               in:  dataframe
               out: href string
               """
               csv = df.to_csv(index=False)
               b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
               href = f'<a href="data:file/csv;base64,{b64}">Download table as csv file</a>'
               return href
     
     st.dataframe(table,600, 600)
     st.markdown(get_table_download_link(table), unsafe_allow_html=True)