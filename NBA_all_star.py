import pandas as pd

# Fetch the data and create a DataFrame
df = pd.read_html('https://en.wikipedia.org/wiki/NBA_All-Star_Game')[2]

# We want to have the Year as Index and drop all the columns except: East scores, West scores and Host city
df.drop(axis=1, columns = ['Game MVP', 'Host Arena'], inplace = True)
df.set_index('Year', inplace = True)

# drop the state and number of times the city has hosted the game from the column, leaving it with just the city's name
df['Host city'] = df['Host city'].str.split(', ', 1, expand=True)

# drop unwanted rows (games with the new format and lockout year of 1999)
for index, row in df.iterrows():
    if row['Result'][:4] != 'East' and row['Result'][:4] != 'West':
        df.drop(index, inplace = True)

# Divide the result column into two new columns, one with the East Score and one with the West Score
east, west = [], []

for x, y in df['Result'].str.strip().str.replace('2OT','').str.split(', '):
    if x[:4] == 'East':
        e_value = ''.join(i for i in x if i.isdigit())
        east.append(int(e_value))
    elif x[:4] == 'West':
        w_value = ''.join(i for i in x if i.isdigit())
        west.append(int(w_value))
    if y[:4] == 'East':
        e_value = ''.join(i for i in y if i.isdigit())
        east.append(int(e_value))
    elif y[:4] == 'West':
        w_value = ''.join(i for i in y if i.isdigit())
        west.append(int(w_value))

df.insert(len(df.columns), 'East', east)
df.insert(len(df.columns), 'West', west)
df.drop(columns = 'Result', inplace=True)

# get games that had a difference of 1 points
df['Diff'] = abs(df['East']-df['West'])
group = df.groupby('Diff')
group.get_group(1)

# DataFrame with the differences as index and number of occurences sorted in descending order
group.size().sort_values(ascending=False)

# Dataframe with the host city as index, the average east and west scores in that city as 2 columns and the count of allstars games in that city as the third column
city_group = df.groupby('Host city')
hc_df = city_group.mean()[['East','West']]
hc_df['Count'] = city_group.value_counts()
hc = hc_df[hc_df['Count'] > 1].sort_values(by='Count', ascending = True)

print(hc)

