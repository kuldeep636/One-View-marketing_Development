import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# ==================================
# CONSTANTS
# ==================================
SHEET_ID = "10EPhn0khnq7I3zMCZeQ374udiTEZP-Qs8fxme28V0fc"

# ==================================
# GOOGLE SHEET CLIENT
# ==================================
@st.cache_resource(ttl=3600)
def get_client():
    try:
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        creds = Credentials.from_service_account_info(
            st.secrets["gcp_service_account"],
            scopes=scopes
        )
        return gspread.authorize(creds)
    except Exception as e:
        st.error(f"Failed to authenticate with Google Sheets: {e}")
        raise

# ==================================
# GET SPREADSHEET
# ==================================
def get_sheet():
    client = get_client()
    return client.open_by_key(SHEET_ID)

# ==================================
# LOAD DATA FUNCTIONS
# ==================================
@st.cache_data(ttl=300)
def load_activity_data():
    sheet = get_sheet()
    worksheet = sheet.sheet1
    data = worksheet.get_all_records()
    return pd.DataFrame(data)

@st.cache_data(ttl=300)
def load_users():
    sheet = get_sheet()
    worksheet = sheet.worksheet("USERS")
    data = worksheet.get_all_records()
    return pd.DataFrame(data)

@st.cache_data(ttl=300)
def load_budget_data():
    sheet = get_sheet()
    worksheet = sheet.worksheet("Budget and Target Overview")
    data = worksheet.get_all_records()
    return pd.DataFrame(data)

@st.cache_data(ttl=300)
def load_expense_data():
    sheet = get_sheet()
    worksheet = sheet.worksheet("Expenes")
    data = worksheet.get_all_records()
    return pd.DataFrame(data)

# ==================================
# USER MANAGEMENT
# ==================================
def get_users_sheet():
    sheet = get_sheet()
    return sheet.worksheet("USERS")

def add_user(
    user_id,
    password,
    name,
    role,
    zone,
    brand,
    access_mapping=""
):
    try:
        worksheet = get_users_sheet()
        worksheet.append_row(
            [
                user_id,
                password,
                name,
                role,
                zone,
                brand,
                access_mapping
            ]
        )
        st.cache_data.clear()
        return True
    except Exception as e:
        st.error(f"Failed to add user: {e}")
        return False

# ==================================
# APPEND DATA TO SHEET
# ==================================
def append_dataframe_to_sheet(
    worksheet_name: str,
    df: pd.DataFrame
):
    if df.empty:
        st.warning("No data to upload.")
        return False
    try:
        st.info("Step 1 : Connected to append_dataframe_to_sheet()")
        sheet = get_sheet()
        st.info("Step 2 : Connected to Google Sheet")
        worksheet = sheet.worksheet(worksheet_name)
        st.info(f"Step 3 : Opened worksheet '{worksheet_name}'")
        sheet_headers = worksheet.row_values(1)
        st.success("Step 4 : Headers loaded successfully")
        df = df.copy()
        for col in sheet_headers:
            if col not in df.columns:
                df[col] = ""
        date_cols = ["Activity Start date", "Activity End date"]
        for col in date_cols:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors="coerce").dt.strftime("%d-%b-%Y")
        if "Upload Timestamp" in df.columns:
            df["Upload Timestamp"] = (
                pd.to_datetime(df["Upload Timestamp"], errors="coerce")
                .dt.strftime("%d-%b-%Y %I:%M %p")
            )
        df = df.reindex(columns=sheet_headers)
        rows = df.fillna("").astype(str).values.tolist()
        st.success(f"Step 5 : Prepared {len(rows)} rows for upload")
        st.info("Step 6 : Uploading rows...")
        st.write("Sheet Headers")
        st.write(sheet_headers)
        st.write("DataFrame Columns")
        st.write(df.columns.tolist())
        
        # Debug line moved inside try block
        st.write(rows[0])
        
        worksheet.append_rows(
            rows,
            value_input_option="USER_ENTERED"
        )
        st.success("Step 7 : Upload completed")
        st.cache_data.clear()
        return True
    except Exception as e:
        st.error(f"Failed to append data to {worksheet_name}: {e}")
        return False

# ==================================
# UPDATE ACTIVITY EXECUTION
# ==================================
def update_activity_execution(
    zone: str,
    brand: str,
    year: str,
    month: str,
    activity_description: str,
    execution_status: str,
    actual_investment: float,
    execution_date: str,
    remarks: str,
    supporting_link: str
):
    try:
        sheet = get_sheet()
        worksheet = sheet.sheet1
        headers = worksheet.row_values(1)
        records = worksheet.get_all_records()
        for row_no, row in enumerate(records, start=2):
            if (
                str(row.get("Zone", "")).strip() == str(zone).strip()
                and str(row.get("Brand", "")).strip() == str(brand).strip()
                and str(row.get("Year", "")).strip() == str(year).strip()
                and str(row.get("Month", "")).strip() == str(month).strip()
                and str(row.get("Activity Description", "")).strip()
                == str(activity_description).strip()
            ):
                updates = {
                    "Execution Status": execution_status,
                    "Actual Investment": actual_investment,
                    "Execution Date": execution_date,
                    "Remarks": remarks,
                    "Supporting Link": supporting_link
                }
                for col_name, value in updates.items():
                    if col_name in headers:
                        col_index = headers.index(col_name) + 1
                        worksheet.update_cell(row_no, col_index, value)
                st.cache_data.clear()
                return True
        st.warning("No matching record found to update.")
        return False
    except Exception as e:
        st.error(f"Update failed: {e}")
        return False
