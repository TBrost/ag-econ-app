import streamlit as st
import pandas as pd
import requests
import io
import plotly.express as px
from datetime import datetime
from datetime import date
def futures_page():
    st.title("Future Prices")
    #st.write("Below is the cash price for wheat in different strands in different parts of the state. Select the region and strand you are interested in and the table and the chart will adjust to your input. This data is separated into rows by week of the year. In many areas and strands there is no information recorded, but for every week there should be an aggregate value for referance")


    # GitHub repository information
    owner = "tbrost"  # Replace with your GitHub username or organization name
    repo = "ag-econ-data"  # Replace with your repository name
    file_path = "data/Future_Data.csv"  # Replace with the path to your CSV file within the repo
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
    'Nezperce / Craigmont','Lewiston','Twin Falls / Buhl / Jerome / Wendell','Moscow / Genesee'))


    ATTRIBUTE = st.selectbox(
        'Select a Strain',
        ('Future - SWW', 'Future - HRW', 'Future - DNS'))
    
    start_date = st.date_input("Start Date", date(2015, 12, 31))
    start_date = datetime(start_date.year, start_date.month, start_date.day)
    end_date = st.date_input("End Date")
    end_date = datetime(end_date.year, end_date.month, end_date.day)

    df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')
    df['Date'] = df['Date'].dt.strftime("%Y/%d/%m")
    df['Date'] = pd.to_datetime(df['Date'], format='%Y/%d/%m')
    # Filter the DataFrame based on the selected date range
    df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

    df = df[['Location','year','week_of_year', 'Attribute','Value']]

    wheat_table=df.query('Attribute == @ATTRIBUTE & Location == @CITY')

    df_pivot = wheat_table.pivot(index=['Attribute','week_of_year', 'Location'], columns=['year'], values='Value')
    df_pivot['Average'] = df_pivot.mean(axis=1)
    df_pivot['Median'] = df_pivot.median(axis=1)
    df_pivot['Max'] = df_pivot.max(axis=1)
    df_pivot['Min'] = df_pivot.min(axis=1)
    df_pivot['Standard Deviation'] = df_pivot.std(axis=1)

    df_pivot = df_pivot.reset_index(names=['Attribute', 'week of year', 'Location'])
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

    # Create a Plotly line chart
    fig = px.line(df_pivot, x='week of year', y=selected_columns, title='Value Summaries by week of the year:')
    st.plotly_chart(fig)

    st.subheader('Annual Summary')
    
    # List of columns to exclude from summarization
    exclude_columns = ['Location', 'Attribute','week of year','Average','Median','Max','Min','Standard Deviation']

    # Identify columns to summarize (exclude the excluded columns)
    columns_to_summarize = [col for col in df_pivot.columns if col not in exclude_columns]

    # Summarize selected columns and save to another DataFrame
    summary_df = pd.DataFrame({
        'Mean': df_pivot[columns_to_summarize].mean(),
        'Min': df_pivot[columns_to_summarize].min(),
        'Max': df_pivot[columns_to_summarize].max()
    })
    # Reshape the DataFrame
    summary_df = summary_df.reset_index(names=['year', 'Mean', 'Min', 'Max'])
    fig2 = px.line(summary_df, x='year', y=['Mean', 'Max', 'Min'], title='Summary values over years (not adjusted for inflation):')
    summary_df.set_index('year', inplace=True)
    # Transpose (T) the DataFrame and reset the index
    reshaped_df = summary_df.T
    st.dataframe(reshaped_df)
    st.plotly_chart(fig2)

    #def link_to_github():
    #    href = '<a href="https://github.com/Lusk27/app_display/tree/main/Data" target="_blank">Link to GitHub</a>'
    #    return href

    #st.markdown(link_to_github(), unsafe_allow_html=True)