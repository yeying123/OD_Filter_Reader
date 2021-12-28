
from collections import namedtuple
import math
import pandas as pd
import streamlit as st
import pydeck as pdk
import geopandas as gpd
import itertools
import base64

st.set_page_config(layout="wide")
st.sidebar.header('Upload the OD data here')
st.sidebar.markdown('Make sure the csv file with these columns: "origin", "destination", and "count"')
st.sidebar.markdown('Note: select one file only')

# Ask to upload file
uploaded_files = st.sidebar.file_uploader('Choose a CSV file', accept_multiple_files=True, type=['csv'])

delimit=st.sidebar.text_input('Delimiter in csv file:', ',')

for i in uploaded_files:
     table=pd.read_csv(i,delimiter=delimit)
     #st.write(table.head(5))

# Input field to ask for Remix link to extract IDs
title = st.text_input('Remix Link', 'Copy URL here')
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

ID_list=ID.split(",")

#st.write(table)
#st.write(table.loc[table['origin']==4135506582950])

summary=0

for t in ID_list:
     t=int(t)
     #st.write(t)
     df=table.loc[table[from_]==t]
     total=df['count'].sum()
     st.write("Total travel from ", from_, " ", t , "is: ", total)
     summary+=total

st.write("Sum: ",summary)
