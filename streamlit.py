
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

basic_episode_ratings = pd.read_csv('basic_episode_ratings.csv')
basic_series_ratings = pd.read_csv('basic_series_ratings.csv') 

st.set_page_config(
    page_title="IMDB Ratings",
    page_icon="🎥",
    layout="wide",
)

st.title("IMDB Ratings for All Series")

st.image("https://upload.wikimedia.org/wikipedia/commons/6/69/IMDB_Logo_2016.svg")

st.text('*Please note that the Series name is case sensitive')


tv_series_name = st.text_input('Show title', '')
st.write('The current Show is:  ', tv_series_name)

st.text('Example: \'The Office\' or \'tt0386676\' ')

selected_shows_list = []
selected_shows_Id = []

if not tv_series_name.isspace():
    if not tv_series_name == "":
        
        selected_shows = basic_series_ratings[basic_series_ratings.primaryTitle.str.contains(tv_series_name)]
        selected_shows2 = basic_series_ratings[basic_series_ratings.originalTitle.str.contains(tv_series_name)]
        selected_shows3 = basic_series_ratings[basic_series_ratings.tconst.str.contains(tv_series_name)]

        dup_selected_shows = pd.concat([selected_shows, selected_shows2, selected_shows3], ignore_index=True)
        
        selected_shows = dup_selected_shows.drop_duplicates()
        
        selected_shows_list = selected_shows['primaryTitle'].tolist()
        
        selected_shows_Id = selected_shows['tconst'].tolist()
        
        selected_shows_list = list(zip(selected_shows_list, selected_shows_Id))
        
selected_show = ''

selected_show2 = st.selectbox('Show: ', selected_shows_list)

def convert(df):
    df=pd.pivot_table(df,index=['episodeNumber'],columns='seasonNumber',values='averageRating',fill_value=np.nan)

    return df

if st.button('Show Chart'):

    episodes = basic_episode_ratings[basic_episode_ratings['parentTconst'] == selected_show2[1]].sort_values(by=['seasonNumber', 'episodeNumber'])
    episodes = episodes[['averageRating', 'seasonNumber', 'episodeNumber']]

    df = convert(episodes)

    line_chart = px.line(df, markers=True)

    st.plotly_chart(line_chart)

    heatmap = px.imshow(df, text_auto=True, aspect="auto")

    st.plotly_chart(heatmap)


st.text("Information courtesy of IMDb (https://www.imdb.com). Used with permission")
st.text("https://developer.imdb.com/non-commercial-datasets/")