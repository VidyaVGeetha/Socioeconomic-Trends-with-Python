import seaborn as sns
import pandas as pd
import csv
import sqlite3
import prettytable
import matplotlib.pyplot as plt

#Connecting to SQLite & Creating connection object
conn=sqlite3.connect("socioeconomic.db")

# Creating cursor object
cur_object=conn.cursor()

#Read the data from the online CSV(from URL)
df = pd.read_csv('https://data.cityofchicago.org/resource/jcxq-k9xf.csv')

#Write the data into the SQLite database(Writing the DataFrame to SQLite)
df.to_sql('chicago_socioeconomic_data',conn,if_exists='replace',index=False,method='multi')

query="SELECT * FROM  chicago_socioeconomic_data ;"
df=pd.read_sql_query(query, conn)

#Print Dataframe
print(df)

#How Many rows are in the data sets
print("The total number of rows in the data set are:")
count_query=cur_object.execute("SELECT  COUNT(* )FROM chicago_socioeconomic_data ")
row_count=cur_object.fetchone()[0]
print(row_count)


#How many community areas in Chicago have a hardship index greater than 50.0?
community_area_names=cur_object.execute("""SELECT community_area_name 
FROM chicago_socioeconomic_data 
WHERE hardship_index>50.0
""")
print("Community areas in Chicago have a hardship index greater than 50.0")
for name in community_area_names:
    print(name)
    
#What is the maximum value of hardship index in this dataset?
query_max_hardship_inex=cur_object.execute("SELECT MAX(hardship_index) FROM chicago_socioeconomic_data")
print("Maximum value of hardship index in this dataset")
max_hardship_index=cur_object.fetchone()[0]
print(max_hardship_index)

#Which community area which has the highest hardship index?
query_communityArea=cur_object.execute("""SELECT community_area_name FROM chicago_socioeconomic_data 
                                       WHERE hardship_index=(SELECT MAX(hardship_index) FROM chicago_socioeconomic_data) """)
communityArea=cur_object.fetchone()[0]
print("community area which has the highest hardship index")
print(communityArea)

#Create a scatter plot using the variables per_capita_income_ and hardship_index
sns.scatterplot(data=df, x="per_capita_income_", y="hardship_index")

plt.title("Per Capita Income vs Hardship Index in Chicago")
plt.xlabel("Per Capita Income")
plt.ylabel("Hardship Index")
plt.grid(True)
plt.tight_layout()
plt.show()
conn.close()

