import pandas as pd
import streamlit as st

@st.cache_data
def preprocess():
    df = pd.read_csv('athlete_events.csv')
    region_df = pd.read_csv('noc_regions.csv')
    # filtering for summer olympics
    df=df[df['Season']=='Summer']
    # merge with region_df
    df=df.merge(region_df,on='NOC',how='left')
    # dropping duplicates
    df.drop_duplicates(inplace=True)
    # one hot encoding medals
    df=pd.concat([df,pd.get_dummies(df['Medal'],dtype=int)],axis=1)
    return df
