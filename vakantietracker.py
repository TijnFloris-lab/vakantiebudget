
import streamlit as st
import pandas as pd
import datetime
import gspread
from google.oauth2.service_account import Credentials
import json

# Pagina-instellingen
st.set_page_config(page_title="Vakantie Budget Tracker", layout="wide")
st.title("🏖️ Vakantie Budget Tracker")

# Google Sheets authenticatie via secrets
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SERVICE_ACCOUNT_INFO = json.loads(st.secrets["GOOGLE_SERVICE_ACCOUNT"])
SHEET_NAME = "VakantieUitgaven"

@st.cache_resource
def get_gsheet():
    creds = Credentials.from_service_account_info(SERVICE_ACCOUNT_INFO, scopes=SCOPES)
    client = gspread.authorize(creds)
    try:
        sheet = client.open(SHEET_NAME).sheet1
    except gspread.SpreadsheetNotFound:
        sheet = client.create(SHEET_NAME).sheet1
        sheet.append_row(["Datum", "Hotel", "Eten", "Transport", "Activiteiten", "Totaal"])
    return sheet

# Haal het Google Sheet werkblad op
sheet = get_gsheet()
records = sheet.get_all_records()
st.session_state.uitgaven = records

# Sidebar instellingen
with st.sidebar:
    st.header("Instellingen")

