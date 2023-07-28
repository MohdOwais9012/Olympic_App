import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
import pickle

def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == year) & (medal_df['region'] == country)]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                      ascending=False).reset_index()

    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']

    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['total'] = x['total'].astype('int')

    return x


def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return years,country


def data_over_time(df, col):
    temp_df = df.drop_duplicates(['Year', col])
    nations_over_time = temp_df['Year'].value_counts().reset_index()
    nations_over_time.columns = ['Edition', 'No of ' + col + 's']
    nations_over_time = nations_over_time.sort_values('Edition')
    return nations_over_time

def most_successful(df, sport):
    temp_df = df[df['Sport'] == sport]
    x = temp_df['Name'].value_counts().reset_index()
    x.columns = ['Name', 'Medals']
    x = x.head(15)
    x = x.merge(temp_df, left_on='Name', right_on='Name', how='left')
    return x


def yearwise_medal_tally(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()
    return final_df

def country_event_heatmap(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    if new_df.empty:
        # If the DataFrame is empty, return a message indicating no medals for the selected country
        print(f"No medals for {country} in the dataset.")
        return pd.DataFrame(columns=['Sport', 'Year', 'Medal'])
    pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return pt

def most_successful_countrywise(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df[temp_df['region'] == country]

    x = temp_df['Name'].value_counts().reset_index().head(10)
    x.rename(columns={'index': 'Name', 'Name': 'Medals'}, inplace=True)
    return x

def weight_v_height(df, sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    
    # Map medal values to colors
    medal_colors = {
        'Gold': 'gold',
        'Silver': 'silver',
        'Bronze': 'peru',
        'No Medal': 'gray'
    }
    
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
    else:
        temp_df = athlete_df

    # Convert Medal values to numerical values for coloring
    temp_df['Medal_color'] = temp_df['Medal'].map(medal_colors)

    # Use matplotlib scatterplot with 'Medal_color' for coloring
    fig, ax = plt.subplots()
    ax.scatter(temp_df['Weight'], temp_df['Height'], c=temp_df['Medal_color'], marker='o', alpha=0.6)
    ax.set_xlabel('Weight')
    ax.set_ylabel('Height')
    ax.set_title('Weight vs Height')
    plt.legend(handles=[plt.Line2D([], [], marker='o', color='gold', label='Gold', linestyle='None'),
                        plt.Line2D([], [], marker='o', color='silver', label='Silver', linestyle='None'),
                        plt.Line2D([], [], marker='o', color='peru', label='Bronze', linestyle='None'),
                        plt.Line2D([], [], marker='o', color='gray', label='No Medal', linestyle='None')])
    
    # Return the figure, not display it here
    return fig


def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final

# pickle_in = open("trained_model.pkl","rb")
# classifier=pickle.load(pickle_in)

def prediction_ans(age,id,year,sport):
   # predictionans = classifier.predict([[age,id,year,sport]])
    predictionans = 0
    if(age < 32):
        return 1
    return predictionans
