import re
import pandas as pd

def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'

    messages = re.split(pattern, data)[1:]

    dates = re.findall(pattern, data)

    # Your input string with a single-digit day
    index = 0;
    for i in dates:
        parts = i.split('/')
        # Check if the day part has a single digit, and add a leading zero if needed
        if len(parts[0]) == 1:
            parts[0] = '0' + parts[0]
        if len(parts[1]) == 1:
            parts[1] = '0' + parts[1]
        # Join the modified parts back into a string
        new = '/'.join(parts)
        dates[index] = new
        index = index + 1

    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    # convert message_date type
    df['message_date'] = pd.to_datetime(df['message_date'], format='%m/%d/%y, %H:%M - ')
    df.rename(columns={'message_date': 'date'}, inplace=True)

    # seperate users and messages
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # user name
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])
    df['users'] = users
    df['messages'] = messages
    df.drop(columns=['user_message'], inplace=True)

    df['year'] = df['date'].dt.year

    df['month_num']=df['date'].dt.month

    df['month'] = df['date'].dt.month_name()

    df['day'] = df['date'].dt.day

    df['only_date'] = df['date'].dt.date

    df['day_name'] = df['date'].dt.day_name()

    df['hour'] = df['date'].dt.hour

    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df