import pandas as pd
from datetime import datetime
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pytz


conn = st.connection("gsheets", type=GSheetsConnection)

tz = pytz.timezone('Asia/Kolkata')

# Use datetime.datetime.now() instead of datetime.now()
current_datetime = datetime.now(tz)  
date = current_datetime.date()
time = current_datetime.time()



def database(user_input: str, response: str):
    data = pd.DataFrame(
    [
        {"Date": date,
         "Time": time,
         "Prompt": user_input,
         "Response": response},
    ]
    )

    example_data = conn.read(worksheet="Sheet1", usecols=[0, 1, 2, 3], ttl = 0.1)

    updated_data = pd.concat([example_data, data], ignore_index=True)
    conn.update(worksheet="Sheet1", data=updated_data)
