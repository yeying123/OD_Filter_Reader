
from collections import namedtuple
import math
import pandas as pd
import streamlit as st
import base64
import streamlit.components.v1 as components

st.set_page_config(
     page_title="OD Selection from Remix",
     layout="wide",
     initial_sidebar_state="expanded")
st.sidebar.title('OD Selection from Remix')

# Input field to ask for Remix link to extract IDs
st.sidebar.header('Step 1: Add Remix OD Layer Link ')
title = st.sidebar.text_input('Remix Link:', 'Copy URL')

# Ask to upload file
st.sidebar.header('Step 2: Upload the OD data file (with all OD pairs)')
st.sidebar.markdown('Make sure the csv file with these columns: "origin", "destination", and "count"')
st.sidebar.markdown('Note: upload one file only')
uploaded_files = st.sidebar.file_uploader('Choose a CSV file', accept_multiple_files=True, type=['csv'])

# Ask to specify delimiter
st.sidebar.header('Step 3: Specify csv file delimiter')
delimit=st.sidebar.text_input('After uploading the csv file, please specify the Delimiter in the csv file:', ';')

# Read IDs in the link
if title.find("od=destination")>0:
     from_='destination'
     to_='origin'
     ID_start=title.find("od=destination")+15
     ID=title[ID_start:]
     st.header('Selected IDs')
     st.write('The ID(s) extracted from the Remix URL: ',ID )
else:
     from_='origin'
     to_='destination'
     ID_start=title.find("od=origin")+10
     ID=title[ID_start:]
     st.header('Selected IDs')
     st.write('The ID(s)extracted from the Remix URL: ',ID)

st.write("###")
#components.html("""<hr style="height:2px;border:none;color:#444;background-color:#444;" /> """)

# create empty dataframe (table)
table=pd.DataFrame()

col1, col2= st.columns((0.8, 0.8))

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
     
     with col1:
          st.header('OD Selection Table')
          st.dataframe(table,450, 600)
          st.markdown(get_table_download_link(table), unsafe_allow_html=True)


     with col2:
          st.header('OD Pair Summary')
          summary=0
          for t in ID_list:
               if int(t) in table[from_].values:
                    number=int(t)
                    #st.write(t)
                    df=table.loc[table[from_]==number]
                    total=df['count'].sum()
                    st.write("Total travel from ", from_, " ", number , "is: ", total)
                    summary+=total
               else:
                    st.write("Total travel from ", from_, " ", number, "is: ", 'No matching record')
          st.write("Sum: ",summary)
