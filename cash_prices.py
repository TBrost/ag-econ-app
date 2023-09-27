import streamlit as st
import pandas as pd
import requests
import io
import plotly.express as px
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

if check_password():

    st.title("Cash Prices")
    st.write("Below is the cash price for wheat in different strands in different parts of the state. Select the region and strand you are interested in and the table and the chart will adjust to your input. This data is separated into rows by week of the year. In many areas and strands there is no information recorded, but for every week there should be an aggregate value for referance")


    # GitHub repository information
    owner = "tbrost"  # Replace with your GitHub username or organization name
    repo = "ag-econ-data"  # Replace with your repository name
    file_path = "data/Cash_Data.csv"  # Replace with the path to your CSV file within the repo
    access_token = st.secrets["token"]  # Replace with your personal access token

    # Construct the raw file URL with the access token
    raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/main/{file_path}"
    headers = {"Authorization": f"token {access_token}"}

    # Make a GET request to the raw file URL
    response = requests.get(raw_url, headers=headers)
    df = pd.read_csv(io.StringIO(response.text))


    #st.download_button("Download Data", df)
    CITY = st.selectbox(
        'Select a City',
        ('Rexburg / Ririe','Idaho Falls','Blackfoot / Pocatello','Grace / Soda Springs','Burley / Rupert','Meridian',
    'Nezperce / Craigmont','Nampa / Weiser','Twin Falls / Buhl / Jerome / Wendell','Moscow / Genesee'))


    ATTRIBUTE = st.selectbox(
        'Select a Strain',
        ('Barley - 48 lbs+', 'Malting', 'Wheat - Milling (SWW)', 'HRW (11.5% Protein)', 'DNS (14% Protein)', 'HWW'))


    wheat_table=df.query('Attribute == @ATTRIBUTE & Location == @CITY')

    df_pivot = wheat_table.pivot(index=['Attribute','week_of_year', 'Location'], columns=['year'], values='Value')
    df_pivot['Average'] = df_pivot.mean(axis=1)
    df_pivot['Median'] = df_pivot.median(axis=1)
    df_pivot['Max'] = df_pivot.max(axis=1)
    df_pivot['Min'] = df_pivot.min(axis=1)
    df_pivot['Standard Deviation'] = df_pivot.std(axis=1)

    df_pivot = df_pivot.reset_index(names=['Attribute', 'week of year', 'year'])
    st.dataframe(df_pivot)

    # Allow users to select summary columns for the line chart
    selected_columns = st.multiselect(
        'Select summary columns for the line chart',
        ['Average', 'Median', 'Max', 'Min', 'Standard Deviation'],
        ['Median', 'Max', 'Min']
    )

    #st.line_chart(df_pivot[['Average','Max','Min']])
    # Create a Plotly line chart
    fig = px.line(df_pivot, x='week of year', y=selected_columns, title='Three Lines Chart')
    st.plotly_chart(fig)




    st.subheader('Charted over the Year')
    st.write("Seelct which metrics you want to see, you can select multiple")


    def link_to_github():
        href = '<a href="https://github.com/Lusk27/app_display/tree/main/Data" target="_blank">Link to GitHub</a>'
        return href

    st.markdown(link_to_github(), unsafe_allow_html=True)