#for data manipulation and nun=merical computation 
import pandas as pd
import numpy as np

#for data visulation
import seaborn as sns
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings('ignore')

#creating dataframe
ipl = pd.read_csv('ipl_2022_dataset.csv')
#print(ipl)

#print(ipl.shape) #prints number of rows and columns

#print(ipl.info) #summary of dataframe..shows column names, non null values, data types.

#print(ipl.columns) #prints the column names

ipl.drop('Unnamed: 0', axis = 1, inplace = True) #drops the unnamed column in the dataset 
#print(ipl)

#print(ipl.isnull().sum()) #number of null values that are present in the each column of the dataset

#print(ipl[ipl['Cost IN $ (000)'].isnull()]) #prints all the rows where cost in $ has null

#now replace all these NaN with 0
ipl['COST IN ₹ (CR.)'] = ipl['COST IN ₹ (CR.)'].fillna(0)
ipl['Cost IN $ (000)'] = ipl['Cost IN $ (000)'].fillna(0)

#print(ipl[ipl['2021 Squad'].isnull()]) #prints all the rows where 2021 squad has null 

#now replace those as not participated
ipl['2021 Squad'] = ipl['2021 Squad'].fillna('Not Participated')

#print(ipl.isnull().sum()) #checks whether all the nulls values are removed or not

#now we will add an extra column status and a list team
teams = ipl[ipl['COST IN ₹ (CR.)']>0]['Team'].unique() #Get all unique team names where player cost is greater than 0
#print(teams)

ipl['status'] = ipl['Team'].replace(teams,'sold') #Replace every value that matches something in teams with 'sold'.
#print(ipl)

#get the players with same name
#print(ipl[ipl['Player'].duplicated(keep=False)])

#number of players with same type
types = ipl['TYPE'].value_counts() #like an hash map
types = types.reset_index() #turns hash map into a table
#print(types)

#count the number of players in each category and visualize using pie chart
plt.pie(
    types['count'],             
    labels = types['TYPE'],      
    labeldistance = 1.2,        
    autopct = '%1.2f%%',         
    shadow = True,               
    startangle = 60              
)
plt.title('Role Of Players Participated', fontsize = 15)
plt.show()

#players sold and unsold using a bar graph
plt.figure(figsize=(10,5))

fig = sns.countplot(x='status',
                    data=ipl,
                    palette=['Green','Red'])

plt.xlabel('Sold or Unsold')
plt.ylabel('Number of Players')
plt.title('Sold vs Unsold', fontsize=15)

for p in fig.patches:
    fig.annotate(format(p.get_height(), '.0f'),
                 (p.get_x() + p.get_width()/2., p.get_height()),
                 ha='center',
                 va='center',
                 xytext=(0,4),
                 textcoords='offset points')

plt.show()

#total sold and unsold players
#print(ipl.groupby('status')['Player'].count())
 
#Total number of players bought by each team

plt.figure(figsize=(20,10))

fig = sns.countplot(
    x = 'Team',
    data = ipl[ipl['Team'] != 'Unsold']
)

plt.xlabel('Team Names')
plt.ylabel('Number of Players')
plt.title('Players bought by each team', fontsize=12)

plt.xticks(rotation=70)

for p in fig.patches:
    fig.annotate(
        format(p.get_height(), '.0f'),
        (p.get_x() + p.get_width()/2., p.get_height()),
        ha='center',
        va='center',
        xytext=(0,4),
        textcoords='offset points'
    )

plt.show()

#add new column retention 
ipl['retention'] = ipl['Base Price']
ipl['retention'].replace(['2 Cr','40 Lakh','20 Lakh','1 Cr','75 Lakh','50 Lakh','30 Lakh','1.5 Cr'],'From Auction',inplace=True)

ipl['Base Price'].replace('Draft Pick',0, inplace=True)

#now add 2 more columns base price unit and base price
ipl['base_price_unit']=ipl['Base Price'].apply(lambda x: str(x).split(' ')[-1])
ipl['base_price']=ipl['Base Price'].apply(lambda x:str(x).split(' ')[0])

ipl['base_price'].replace('Retained',0,inplace=True)
#print(ipl)

#Total players retained and bought by each team
#print(ipl.groupby(['Team','retention'])['retention'].count()[:-1])


plt.figure(figsize=(20,10))

fig = sns.countplot(
    x='Team',
    data=ipl[ipl['Team']!='Unsold'],
    hue='TYPE'
)

plt.title('Players in each team')
plt.xlabel('Team Names')
plt.ylabel('Number of Players')

plt.xticks(rotation=50)

plt.show()

#Highest amount spent on a single player by each team
#print(ipl[ipl['retention']=='From Auction'].groupby(['Team'])sort_values(ascending=False))

#Player retained af maximum price
#print(ipl[ipl['retention']=='Retained'].sort_values(by ='COST IN ₹ (CR.)',ascending = False).head(1))

#Top 5 bowlers
#top 5 bowlers based on highest price

top_bowlers = ipl[ipl['TYPE'] == 'BOWLER'] \
                .sort_values(by='COST IN ₹ (CR.)', ascending=False) \
                .head(5)

#print(top_bowlers[['Player', 'Team', 'COST IN ₹ (CR.)']])

ipl = ipl.rename(columns={'2021 Squad' : 'Prev_team'})

unsold_players = ipl[(ipl.Prev_team != 'Not Participated') & (ipl.Team == 'Unsold')][['Player','Prev_team']]
print(unsold_players)