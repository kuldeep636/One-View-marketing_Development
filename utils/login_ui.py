import streamlit as st


def inject_login_css():

    st.markdown("""
    <style>

    .stApp {
        background-color: #f5f7fa;
    }

    .login-container {
        background: white;
        padding: 35px;
        border-radius: 18px;
        box-shadow: 0px 8px 25px rgba(0,0,0,0.08);
        margin-top: 20px;
        margin-bottom: 20px;
    }

    .login-title {
        text-align:center;
        color:#002060;
        font-size:40px;
        font-weight:700;
        margin-bottom:5px;
    }

    .login-subtitle {
        text-align:center;
        color:#6c757d;
        font-size:16px;
        margin-bottom:25px;
    }

    .footer-text {
        text-align:center;
        color:#9aa0a6;
        font-size:12px;
    }

    .stButton > button {
        background-color:#002060;
        color:white;
        height:50px;
        border-radius:10px;
        border:none;
        font-weight:600;
    }

    .stButton > button:hover {
        background-color:#003080;
        color:white;
    }

    </style>
    """, unsafe_allow_html=True)
