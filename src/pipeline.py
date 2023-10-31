import requests
import pandas as pd
import streamlit as st
import cfbd
import plotly.express as px
from cfbd.rest import ApiException
from dotenv import load_dotenv
from os import getenv

st.set_page_config(
    page_icon='📖',
    initial_sidebar_state='expanded'
)
page = st.sidebar.selectbox(
    'Page',
    ('Overall Record', 'Visualizations', 'Matchup Records')
)

configuration = cfbd.Configuration()
configuration.api_key['Authorization'] = 'XscFL3JKpF/UVy2fexpow+vZ/o6rlKfxtnQdN70yVY89w1aTyXYDO+o641kfK8zy'
configuration.api_key_prefix['Authorization'] = 'Bearer'
api_instance = cfbd.GamesApi(cfbd.ApiClient(configuration))
api_instance2 = cfbd.TeamsApi(cfbd.ApiClient(configuration))

st.title("Welcome to Your Favorite College Football Team's Homepage!")
fav_team = st.text_input('Your favorite team: ')
if fav_team:
    try:
        records = api_instance.get_team_records(team = f'{fav_team}')
        df = pd.DataFrame.from_records([g.to_dict() for g in records])
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
        del df['division']
   
        df['year'] = df['year'].astype(str).str.replace(',', '', regex=True)
        df['team_id'] = df['team_id'].astype(str).str.replace(',', '', regex=True)
    
    except:
        st.error('Please make sure to write the correct spelling of your team without the institution at the end. For example, Michigan State(correct), Michigan State University(incorrect).')

if page == 'Overall Record':

    if st.button("Come on, let's see my data"):
        df

if page == 'Visualizations':
    if st.checkbox("Cool stuff, now let's see some visualizations"):
        vis_to_use = ['scatterplot', 'histogram', 'bar chart']
        type_vis = st.selectbox('Select the type of visualization you would like to see:', options=vis_to_use)

        if type_vis == 'scatterplot':
            answer = st.selectbox('Select a Column to Visualize on the X-axis:', options= sorted(list(df.columns)))
            answer2 = st.selectbox('Select a Column to Visualize on the Y-axis:', options = sorted(list(df.columns)))
            if answer and answer2:
                try:
                    st.scatter_chart(data=df, x=answer, y=answer2)
                    #st.plotly_chart(px.scatter(df, x=answer, y=answer2), use_container_width=True)
                except BaseException:
                    print("Error visualizing those combination of columns")

        if type_vis == 'bar chart':
            answer = st.selectbox('Select a Column to Visualize on the X-axis:', options = sorted(list(df.columns)))
            answer2 = st.selectbox('Select a Column to Visualize on the Y-axis:', options = sorted(list(df.columns)))
            if answer and answer2:
                try:
                    st.plotly_chart(px.bar(df, x=answer, y=answer2), use_container_width=True)
                except BaseException:
                    print("Error visualizing those combination of columns")

        if type_vis == 'histogram':
            answer = st.selectbox('Select a Column to Visualize on the X-axis:', options = sorted(list(df.columns)))
            if answer:
                try:
                    st.plotly_chart(px.histogram(df, x=answer, use_container_width=True))
                except BaseException:
                        print("Error visualizing those combination of columns")

    
if page == 'Matchup Records':
    #if st.checkbox("How about we take a look at some matchups"):
    team2 = st.text_input("Please choose a second team: ")
    if team2:
        try:
            api_response = api_instance2.get_team_matchup(fav_team, team2)
            matchup = pd.DataFrame(api_response.to_dict()['games'])
            del matchup['week']
            del matchup['season_type']
            del matchup['_date']
            del matchup['neutral_site']
            del matchup['venue']
            matchup = matchup.fillna('Tie Game')
            matchup['season'] = matchup['season'].astype(str).str.replace(',', '', regex=True)

            win_count = 0
            loss_count = 0
            tie_count = 0

            for index, row in matchup.iterrows():
                if row['winner'] == f'{fav_team}':
                    win_count += 1
                elif row['winner'] == f'{team2}':
                    loss_count += 1
                elif row['winner'] == 'Tie Game':
                    tie_count += 1
                matchup.loc[index,'overall_record'] = f'{win_count}-{loss_count}-{tie_count}'
            matchup

        except:
            st.error('Please make sure to write the correct spelling of your team without the institution at the end. For example, Michigan State(correct), Michigan State University(incorrect).')

# Connecting to Elephant SQL

        #connection = 'postgresql://lbgowpbc:dNYHpRnfDLZbvt4iBvVhp11ziizGwLlI@castor.db.elephantsql.com/lbgowpbc'
        load_dotenv()
        sql_url = getenv('SQL_URL')

        df.to_sql('team_records', index=False, con = sql_url, if_exists = 'replace')
        matchup.to_sql('team_matchups', index=False, con = sql_url, if_exists = 'replace')