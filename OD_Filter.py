
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


# Ask to upload file
st.sidebar.subheader('Step 1: Upload the OD data file (with all OD pairs)')
st.sidebar.caption('Make sure the csv file with these columns: "origin", "destination", and "count"(all lowercase)')
st.sidebar.caption('Note: one file only')
uploaded_files = st.sidebar.file_uploader('Upload a CSV file', accept_multiple_files=True, type=['csv'])

# Ask to specify delimiter
st.sidebar.subheader('Step 2: Specify csv file delimiter')
delimit=st.sidebar.text_input('Specify the Delimiter used in the csv file:', ';')

# Input field to ask for Remix link to extract IDs
st.sidebar.subheader('Step 3: Add Remix OD Layer Link ')
title1 = st.sidebar.text_input('Remix Link:', 'Copy URL')

st.sidebar.subheader('Step 3.1(Optional): Add Another Remix OD Layer Link ')
title2 = st.sidebar.text_input('Remix 2nd Link:', 'Copy URL')


# Read IDs in the link
if title1 != 'Copy URL':
     if title1.find("od=destination")>0:
          from_='destination'
          to_='origin'
          ID_start=title1.find("od=destination")+15
          ID=title1[ID_start:]
          st.header('Selected IDs in Remix')
          st.write('The destination ID(s) extracted from the Remix URL: ',ID )
     else:
          from_='origin'
          to_='destination'
          ID_start=title1.find("od=origin")+10
          ID=title1[ID_start:]
          st.header('Selected IDs in Remix')
          st.write('The origin ID(s) extracted from the Remix URL: ',ID)

#st.write("###")
#components.html("""<hr style="height:2px;border:none;color:#444;background-color:#444;" /> """)

# create empty dataframe (table)
table=pd.DataFrame()

col1, col2= st.columns((1,1))

# Generate the aggregated table
if uploaded_files != []:
     if title1=='Copy URL':
          st.write('URL missing')
     else:
          ID_list=ID.split(",")
          for i in uploaded_files:
               df=pd.read_csv(i,delimiter=delimit)
               if len(df.columns)==1:
                    st.write('Make sure you have the right delimiter in Step 2')
               for t in ID_list:
                    if int(t) in df[from_].values:
                         number=int(t)
                         df1=df.loc[df[from_]==number]
                         table=table.append(df1)


          with col1:
               st.header('OD Selection Table (1)')
               st.dataframe(table,450, 600)
               def convert_df(df):
               # IMPORTANT: Cache the conversion to prevent computation on every rerun
                    return df.to_csv().encode('utf-8')
               csv = convert_df(table)

               st.download_button(
                    "Press to Download CSV",
                    csv,
                    "OD_Selection_Table_1.csv",
                    "text/csv",
                    key='download-csv'
                    )


          with col2:
               st.header('OD Pair Summary')
               summary=0
               for t in ID_list:
                    if int(t) in table[from_].values:
                         number=int(t)
                         #st.write(t)
                         df_new=table.loc[table[from_]==number]
                         total=df_new['count'].sum()
                         st.write("Total travel from ", from_, " ", number , "is: ", total)
                         summary+=total
                    else:
                         number=int(t)
                         st.write("Total travel from ", from_, " ", number, "is: ", 'No matching record')
               st.write("Sum: ",summary)

st.markdown("""---""")

if title2 != 'Copy URL' and len(title2)>0:
     if title2.find("od=destination")>0:
          from_2='destination'
          to_2='origin'
          ID_start2=title2.find("od=destination")+15
          ID2=title2[ID_start2:]
          st.header('Selected IDs in Remix (2nd Link)')
          st.write('The destination ID(s) extracted from the 2nd Remix URL: ',ID2 )
     else:
          from_2='origin'
          to_2='destination'
          ID_start2=title2.find("od=origin")+10
          ID2=title2[ID_start2:]
          st.header('Selected IDs in Remix (2nd Link)')
          st.write('The origin ID(s) extracted from the 2nd Remix URL: ',ID2)
     
     #st.write('ID2:',ID2)

     # create empty dataframe (table)
     table2=pd.DataFrame()
     #st.write(from_2)
     col3, col4= st.columns((0.8, 0.8))
     
     ID_list2=ID2.split(",")
     #st.write('ID_list2:',ID_list2)

     for t in ID_list2:
          if int(t) in df[from_2].values:
               number=int(t)
               df_2=df.loc[df[from_2]==number]
               table2=table2.append(df_2)

     def get_table_download_link(df_2):
               """Generates a link allowing the data in a given panda dataframe to be downloaded
               in:  dataframe
               out: href string
               """
               csv2 = df_2.to_csv(index=False)
               b64 = base64.b64encode(csv2.encode()).decode()  # some strings <-> bytes conversions necessary here
               href = f'<a href="data:file/csv;base64,{b64}">Download table as csv file</a>'
               return href

     with col3:
          st.header('OD Selection Table (2)')
          st.dataframe(table2,450, 600)
          def convert_df(df):
          # IMPORTANT: Cache the conversion to prevent computation on every rerun
               return df.to_csv().encode('utf-8')
          csv = convert_df(table2)

          st.download_button(
               "Press to Download CSV",
               csv,
               "OD_Selection_Table_2.csv",
               "text/csv",
               key='download-csv'
               )


     with col4:
          st.header('OD Pair Summary')
          summary=0
          for t in ID_list2:
               if int(t) in table2[from_2].values:
                    number=int(t)
                    #st.write(t)
                    df_2=table2.loc[table2[from_2]==number]
                    total2=df_2['count'].sum()
                    st.write("Total travel from ", from_2, " ", number , "is: ", total2)
                    summary+=total2
               else:
                    number=int(t)
                    st.write("Total travel from ", from_2, " ", number, "is: ", 'No matching record')
          st.write("Sum: ",summary)

