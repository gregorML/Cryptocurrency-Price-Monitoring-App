import datetime
import streamlit as st

def timestamp_validation(start_date, start_time, end_date, end_time):
    start_timestamp = datetime.datetime.combine(start_date, start_time)
    end_timestamp = datetime.datetime.combine(end_date, end_time)
    if start_timestamp >= end_timestamp:
        st.error("The end time must be later than the start time.")
        return None, None
    else:
        return start_timestamp, end_timestamp
