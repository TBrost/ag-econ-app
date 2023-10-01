import streamlit as st
import pandas as pd
import requests
import io
import plotly.express as px
def cash_page():
    st.title("Cash Prices")
    #st.write("Below is the cash price for wheat in different strands in different parts of the state. Select the region and strand you are interested in and the table and the chart will adjust to your input. This data is separated into rows by week of the year. In many areas and strands there is no information recorded, but for every week there should be an aggregate value for referance")


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
        ('Barley (Feed)', 'Barley (Malting)', 'SWW (Milling)', 'HRW (11.5% Protein)', 'DNS (14% Protein)', 'HWW'))
    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")

    # Filter the DataFrame based on the selected date range
    df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

    df = df[['Location','year','week_of_year', 'Attribute','Value']]
    wheat_table=df.query('Attribute == @ATTRIBUTE & Location == @CITY')

    df_pivot = wheat_table.pivot(index=['Attribute','week_of_year', 'Location', 'Contract', 'Date'], columns=['year'], values='Value')
    df_pivot['Average'] = df_pivot.mean(axis=1)
    df_pivot['Median'] = df_pivot.median(axis=1)
    df_pivot['Max'] = df_pivot.max(axis=1)
    df_pivot['Min'] = df_pivot.min(axis=1)
    df_pivot['Standard Deviation'] = df_pivot.std(axis=1)

    df_pivot = df_pivot.reset_index(names=['Attribute', 'week of year', 'Location', 'Contract', 'Date'])
    st.dataframe(df_pivot)



    filename= f'{ATTRIBUTE}_{CITY}_data.csv'
    def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv().encode('utf-8')
    

    csv = convert_df(df_pivot)

    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name=filename,
        mime='text/csv',
    )
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




    #st.subheader('Charted over the Year')
    #st.write("Seelct which metrics you want to see, you can select multiple")


    #def link_to_github():
    #    href = '<a href="https://github.com/Lusk27/app_display/tree/main/Data" target="_blank">Link to GitHub</a>'
    #    return href

    #st.markdown(link_to_github(), unsafe_allow_html=True)