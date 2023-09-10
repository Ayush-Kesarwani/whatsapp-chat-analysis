from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import re


extractor=URLExtract()

def fetch_stats(selected_user,df):

    if selected_user!='Overall':
        df = df[df['users'] == selected_user]

    # fetch the number of messages
    num_messages = df.shape[0]
    words = []

    # fetch the total number of words
    for message in df['messages']:
        words.extend(message.split())

    # fetch the number of media messages
    num_media_messages=df[df['messages']=='<Media omitted>\n'].shape[0]

    # fetch number of links shared
    links=[]
    for message in df['messages']:
        links.extend(extractor.find_urls((message)))

    return num_messages, len(words), num_media_messages, len(links)

def most_busy_users(df):
    x=df['users'].value_counts().head()
    df=round((df['users'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'users': 'percent'})
    return x,df


def create_wordCloud(selected_user,df):

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    temp = df[df['users'] != 'group_notification']
    temp = temp[temp['messages'] != '<Media omitted>\n']

    def remove_stop_words(message):
        y=[]
        for word in message.lower().split():
            y.append(word)
        return " ".join(y)

    wc=WordCloud(width=500,height=500,min_font_size=10,background_color='black')
    temp['messages']=temp['messages'].apply(remove_stop_words)
    df_wc=wc.generate(temp['messages'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user,df):

    f=open('stop_hinglish.txt','r')
    stop_words=f.read()

    if selected_user!='Overall':
        df = df[df['users'] == selected_user]

    temp = df[df['users'] != 'group_notification']
    temp = temp[temp['messages'] != '<Media omitted>\n']

    words = []
    for message in temp['messages']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df=pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def emoji_helper(selected_user,df):
    if selected_user!='Overall':
        df = df[df['users'] == selected_user]

    emoji_pattern = re.compile(
        r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF\U0001FAB0-\U0001FABF\U0001FAC0-\U0001FAFF\U00002702-\U000027B0\U000024C2-\U0001F251]+')

    emojis = []
    for message in df['messages']:
        emojis.extend(emoji_pattern.findall(message))

    emoji_df=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df

def monthly_timeline(selected_user,df):
    if selected_user!='Overall':
        df = df[df['users'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['messages'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def daily_timeline(selected_user,df):
    if selected_user!='Overall':
        df = df[df['users'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['messages'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):
    if selected_user!='Overall':
        df = df[df['users'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):
    if selected_user!='Overall':
        df = df[df['users'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    user_heatmap= df.pivot_table(index='day_name', columns='period', values='messages', aggfunc='count').fillna(0)

    return user_heatmap

