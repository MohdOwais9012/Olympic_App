import streamlit as st
import pandas as pd
import preprocessor,helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

page_bg_img = """
<style>
background-image url("wp2379663.jpg")
background-size: cover;
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)


df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df,region_df)

st.sidebar.title("Olympics Analysis")
st.sidebar.image('https://wallpapercave.com/wp/wp2379663.jpg')
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Overview','Medal Distribution','Overall Analysis','Analysis Based on Athlete','Prediction')
)

if user_menu == 'Overview':
    st.title("What is Olympic?")
    st.write('The Olympics is a prestigious international multi-sport event held every four years, comprising Summer and Winter editions. Athletes from around the world compete, promoting unity, sportsmanship, and human excellence, inspired by its ancient Greek origins.')
    st.title('Summary of 120 Years of Olympics')
    st.image('https://user-images.githubusercontent.com/73730336/156466867-c3600a60-b116-4c3d-a889-8b3549b007dc.jpg',width=800)
    st.title('Objective')
    st.write("Our primary objective is to conduct a comprehensive analysis of the Olympics, spanning across various editions, sports, and nations. By harnessing the vast dataset at our disposal, we aspire to provide a holistic view of the Games, uncovering fascinating correlations between factors such as host countries, athlete demographics, event performances, and medal distributions. Furthermore, our analysis will explore the impact of socio-economic and geopolitical factors on Olympic participation and success, fostering a deeper understanding of the Games' significance beyond the realm of sports.")
    st.title('Methodology')
    st.write("To achieve our goals, we will employ a multi-faceted approach that combines data collection, cleansing, and processing with sophisticated statistical techniques and data visualization. We will draw data from reputable historical records, official Olympic databases, and credible sources to ensure the accuracy and reliability of our findings.")
    st.title('Key Areas of Analysis:')
    st.write("1. Historical Evolution: Tracing the origins of the modern Olympics and examining how the event has evolved over time, including the inclusion of new sports and changes in format.")
    st.write("2. Medals Distribution: Investigating the distribution of medals across different countries and sports, identifying dominant nations and trends in athletic performances.")
    st.write("3. Overall Analysis: Overall, an in-depth analysis of the Olympics dataset can provide valuable insights into the world of sports, international competition, and the impact of the Games on athletes and host countries. It can also highlight areas for improvement in terms of inclusivity, gender representation, and anti-doping efforts to ensure the integrity and fairness of the Olympic Games.")
    st.write("4. Analysis Based on Athlete: analyzing athletes in the Olympics involves understanding their performance, achievements, and impact on the games.")
    st.write("5. Prediction: While these predictions are speculative, the Olympic Games have consistently evolved to reflect the changing times and global landscape. The future of the Olympics promises to be exciting and full of opportunities for innovation, sustainability, and inclusivity.")
    st.title("Technology and Libraries Used:")
    st.write("1. Python")
    st.write("2. Pandas")
    st.write("3. NumPy")
    st.write("4. Seaborn")
    st.write("5. MatplotLib")
    st.write("6. StreamLit")
    st.write("7. SkLearn")
    st.title("Dataset Used")
    st.write(df.head())
    st.title("Explanation in Youtube Video")
    st.video("https://youtu.be/tkgNkFAzQQ8")
    st.title("Team Members")
    st.write("1. Nandini Agarwal")
    st.write("2. Isha Jindal")
    st.write("3. Mohd Owais")
     
     
if user_menu == 'Medal Distribution':
    st.image("https://www.grunge.com/img/gallery/can-you-buy-an-olympic-medal/l-intro-1627941236.jpg")
    st.sidebar.header("Medal Tally")
    years,country = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox("Select Year",years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Tally")
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title("Medal Tally in " + str(selected_year) + " Olympics")
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " overall performance")
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " performance in " + str(selected_year) + " Olympics")
    st.table(medal_tally)


if user_menu == 'Overall Analysis':
    st.image('https://www.bestvpnanalysis.com/wp-content/uploads/2018/01/Winter-Olympics-Opening-Ceremony-2.jpg')
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title("Top Statistics")
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athletes)

    nations_over_time = helper.data_over_time(df,'region')
    fig = px.line(nations_over_time, x="Edition", y="No of regions")
    st.title("Participating Nations over the years")
    st.plotly_chart(fig)

    events_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(events_over_time, x="Edition", y="No of Events")
    st.title("Events over the years")
    st.plotly_chart(fig)

    athlete_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athlete_over_time, x="Edition", y="No of Names")
    st.title("Athletes over the years")
    st.plotly_chart(fig)

    st.title("No. of Events over time(Every Sport)")
    fig,ax = plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
                annot=True)
    st.pyplot(fig)
    st.title("Most successful Athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')

    selected_sport = st.selectbox('Select a Sport',sport_list)
    x = helper.most_successful(df,selected_sport)
    st.table(x)

if user_menu == 'Analysis Based on Athlete':
    st.image('https://www.eatingdisorderhope.com/wp-content/uploads/2018/06/olympia-1543733_1280-1024x682.png')
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],show_hist=False, show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.title("Distribution of Age")
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age wrt Sports(Gold Medalist)")
    st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    st.title('Height Vs Weight')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(df,selected_sport)
    st.pyplot(temp_df)

    st.title("Men Vs Women Participation Over the Years")
    final = helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)


if user_menu == 'Prediction':
    st.title("Predict if Athlete will win the Medal?")
    age = st.text_input('Age')
    id =  st.text_input('ID')
    year = st.text_input('Year')
    sport = st.text_input('Sport')
    result =  0
    if st.button('Predict'):
         result = helper.prediction_ans(int(age),id,year,sport)
         if(result == 1):
             st.success("Success")
         else:
             st.success("Failure")
         
    
    
     



