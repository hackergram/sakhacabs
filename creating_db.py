import pygsheets
gd=pygsheets.authorize("/home/lilhack110/authdir/sheets.googleapis.com-python.json")
sakha=gd.open_by_key("1tcZWw19HBLta8Dmnby9ScjZC5S0fhYumfsIfDW6r3e8")
sakha_ws=sakha.worksheet_by_title("2018")
sakhadf=sakha_ws.get_as_df()
sakhadf.columns

#sakhadf.drop(sakhadf.ix[:,'Duty Cancelled':'No o f Ride'].head(0).columns, axis=1)
#sakha_cabs_df_drop=sakhadf.drop(sakhadf.ix[:,'Duty Cancelled':'No o f Ride'].head(0).columns, axis=1)
gd.list_ssheets()
sakha=gd.open_by_key("1QDzE009LaHhNbcF-xy5Fo1Kjj2Lj_u7iayITphcH1T4")
sakha_ws=sakha.worksheet_by_title("2018")
sakhadf=sakha_ws.get_as_df()
#sakha_cabs_df_drop=sakhadf.drop(sakhadf.ix[:,'Duty Cancelled':'No o f Ride'].head(0).columns, axis=1)
#sakha_cabs_df_drop.columns
#sakhacdf = sakha_cabs_df_drop.fillna(method='ffill')
#sakhacdf
#sakhacdf.head()
import pymongo
client= pymongo.MongoClient("mongodb://localhost:27017/")
sakha1=client.sakha
roster1=sakha1.mis_roster
#client.list_database_names
#print(client.list_database_names())
#sakha1.insert_many(df.to_dict('records'))
#sakha1.insert_many(sakhacdfdf.to_dict('records'))
#sakha1.insert_many(sakhacdf.to_dict('records'))
roster1=sakha1.mis_roster
#roster1.insert_many(sakhacdfdf.to_dict('records'))
roster1.insert_many(sakhadf.to_dict('records'))
