import streamlit as st
import pandas as pd
import requests
import io
import plotly.express as px
from cash_prices import cash_page
from futures_prices import futures_page
from basis_prices import basis_page
st.set_page_config(page_title="Wheat Charts", page_icon="🌾")
def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct.
        return True
    
def welcome_page():
    st.markdown("# Main page 🎈")
    st.sidebar.markdown("# Main page 🎈")
    st.header("Welcome to the BYU-I Idaho Grains App")
    st.subheader('Instructions')
    st.write('In this application we have infomation about selling crops in Idaho. Each tab to your left will have different tools to help you evaulate \nwhen and where to sell. Each page will allow you to choose a location as well as specify a crop. You will then be presented with historical data for each week of the year in both a table and a chart to help you analyze time based trends.')


page_names_to_funcs = {
    "Main Page": welcome_page,
    "Cash Prices": cash_page,
    "Futures Prices": futures_page,
    "Basis Prices": basis_page,
}

if check_password():
    selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
    page_names_to_funcs[selected_page]()
    