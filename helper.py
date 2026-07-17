import numpy as np




def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(
        subset=[
            'Team', 'region', 'NOC', 'Games', 'Year',
            'City', 'Sport', 'Event', 'Medal'
        ]
    )

    country_selected = country != 'Overall'

    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df

    elif year == 'Overall' and country != 'Overall':
        temp_df = medal_df[medal_df['region'] == country]

    elif year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]

    else:
        temp_df = medal_df[
            (medal_df['Year'] == int(year)) &
            (medal_df['region'] == country)
        ]

    if country_selected:
        x = (
            temp_df
            .groupby('Year')[['Gold', 'Silver', 'Bronze']]
            .sum()
            .sort_values('Year')
            .reset_index()
        )
    else:
        x = (
            temp_df
            .groupby('region')[['Gold', 'Silver', 'Bronze']]
            .sum()
            .sort_values('Gold', ascending=False)
            .reset_index()
        )

    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']

    return x

def medal(df):
    medal_tally=df.drop_duplicates(subset=['Team','region','NOC','Games','Year','City','Sport','Event','Medal'])

    medal_tally = medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                    ascending=False).reset_index()

    medal_tally['total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']

    return medal_tally

def country_year_list(df):
    years=df['Year'].unique().tolist()
    years.sort()
    years.insert(0,'Overall')

    country=np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0,'Overall')

    return years,country

def data_over_time(df,col):
    nations_over_time=df.drop_duplicates(['Year',col])['Year'].value_counts().reset_index().sort_values('Year')
    nations_over_time.rename(columns={'count':col},inplace=True)
    return nations_over_time

def most_successful(df, sport):
    temp_df = df.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    top_athletes = (
        temp_df['Name']
        .value_counts()
        .reset_index()
        .head(15)
    )

    result = top_athletes.merge(
        df,
        on='Name',
        how='left'
    )[['Name','count','Sport','region']].drop_duplicates('Name')

    return result

def yearwise_medal_tally(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df.drop_duplicates(
        subset=[
            'Team', 'NOC', 'Games',
            'Year', 'City', 'Sport',
            'Event', 'Medal'
        ]
    )
    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()
    return final_df

def country_event_heatmap(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df.drop_duplicates(
        subset=[
            'Team', 'NOC', 'Games',
            'Year', 'City', 'Sport',
            'Event', 'Medal'
        ]
    )

    new_df = temp_df[temp_df['region'] == country]

    pt=new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return pt

def most_successful_country_wise(df, country):
    temp_df = df.dropna(subset=['Medal'])

    temp_df = temp_df[temp_df['region'] == country]

    top_athletes = (
        temp_df['Name']
        .value_counts()
        .reset_index()
        .head(10)
    )

    result = top_athletes.merge(
        df,
        on='Name',
        how='left'
    )[['Name','count','Sport']].drop_duplicates('Name')

    return result

def weight_v_height(df,sport):
    athlete_df=df.drop_duplicates(subset=['Name','region'])
    athlete_df['Medal'] = athlete_df['Medal'].fillna('No Medal')
    if sport != 'Overall':
        athlete_df=athlete_df[athlete_df['Sport'] == sport]
    return athlete_df

def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')

    final.fillna(0, inplace=True)

    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)
    return final