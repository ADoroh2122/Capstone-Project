import requests
import pandas as pd
import streamlit as st
import cfbd
import plotly.express as px

st.title("Welcome to Your Favorite College Football Team's Homepage!")
st.write("Within this page, you will be able to view your team's wins/losses since program inception")

configuration = cfbd.Configuration()
configuration.api_key['Authorization'] = 'XscFL3JKpF/UVy2fexpow+vZ/o6rlKfxtnQdN70yVY89w1aTyXYDO+o641kfK8zy'
configuration.api_key_prefix['Authorization'] = 'Bearer'

api_instance = cfbd.GamesApi(cfbd.ApiClient(configuration))

fav_team = st.text_input('What is your favorite team: ')
try:
    records = api_instance.get_team_records(team = f'{fav_team}')
    df = pd.DataFrame.from_records([g.to_dict() for g in records])
except:
    st.write('Please make sure to write the correct spelling of your team without the institution at the end. For example, Michigan State(correct), Michigan State University(incorrect).')
data = pd.json_normalize(df['total'])
df['total_games'] = data['games']
df['total_wins'] = data['wins']
df['total_losses'] = data['losses']
df['total_ties'] = data['ties']
data1 = pd.json_normalize(df['conference_games'])
df['total_conference_games'] = data1['games']
df['total_conference_wins'] = data1['wins']
df['total_conference_losses'] = data1['losses']
df['total_conference_ties'] = data1['ties']
data2 = pd.json_normalize(df['home_games'])
df['total_home_games'] = data2['games']
df['total_home_wins'] = data2['wins']
df['total__home_losses'] = data2['losses']
df['total__home_ties'] = data2['ties']

data3 = pd.json_normalize(df['away_games'])
df['total_away_games'] = data3['games']
df['total_away_wins'] = data3['wins']
df['total_away_losses'] = data3['losses']
df['total_away_ties'] = data3['ties']

del df['total']
del df['conference_games']
del df['home_games']
del df['away_games']


df['division'].replace('', 'Not Applicable', inplace=True)    
df['year'] = df['year'].astype(str).str.replace(',', '', regex=True)

if st.button("Come on, let's see my data"):
    df
st.button("Cool stuff, now let's see some visualizations")

vis_to_use = ['scatterplot', 'histogram', 'bar chart']
type_vis = st.selectbox('Select the type of visualization you would like to see:', options=vis_to_use)

if type_vis == 'scatterplot':
    answer = st.selectbox('Select a Column to Visualize on the X-axis:', options= list(df.columns))
    answer2 = st.selectbox('Select a Column to Visualize on the Y-axis:', options = list(df.columns))
    if answer and answer2:
        try:
            st.plotly_chart(px.scatter(df, x=answer, y=answer2), use_container_width=True)
        except BaseException:
            print("Error visualizing those combination of columns")

if type_vis == 'bar chart':
    answer = st.selectbox('Select a Column to Visualize on the X-axis:', options = list(df.columns))
    answer2 = st.selectbox('Select a Column to Visualize on the Y-axis:', options = list(df.columns))
    if answer and answer2:
        try:
            st.plotly_chart(px.bar(df, x=answer, y=answer2), use_container_width=True)
        except BaseException:
            print("Error visualizing those combination of columns")

if type_vis == 'histogram':
    answer = st.selectbox('Select a Column to Visualize on the X-axis:', options = list(df.columns))
    if answer:
        try:
            st.plotly_chart(px.histogram(df, x=answer, use_container_width=True))
        except BaseException:
            print("Error visualizing those combination of columns")
    

    #st.line_chart(data=df, x='year', y='total_wins')


# Connecting to Elephant SQL

    connection = 'postgresql://lbgowpbc:dNYHpRnfDLZbvt4iBvVhp11ziizGwLlI@castor.db.elephantsql.com/lbgowpbc'

    df.to_sql('team_records', index=False, con = connection, if_exists = 'replace')

    df.to_csv('team_records.csv', index=False)