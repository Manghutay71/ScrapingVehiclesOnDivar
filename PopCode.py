# -*- coding: utf-8 -*-
"""
Created on Wed Oct  5 12:09:36 2022

@author: TheGreatEngineer
"""

import pandas as pd
from bs4 import BeautifulSoup
import requests
import time
import datetime



popular_car_models = pd.read_excel(open('information.xlsx', 'rb'),sheet_name='popular cars')
less_popular_car_models = pd.read_excel(open('information.xlsx', 'rb'),sheet_name='less popular cars')
full_city_list = pd.read_excel(open('information.xlsx', 'rb'),sheet_name='cities')
neighbours_list = pd.read_excel(open('information.xlsx', 'rb'),sheet_name='neighbours')
tehran_super_neighbour_list = pd.read_excel(open('information.xlsx', 'rb'),sheet_name='super neighbours')


parser = "html.parser"

year = ['1380-1380','1381-1381','1382-1382','1383-1383','1384-1384','1385-1385','1386-1386','1387-1387','1388-1388','1389-1389','1390-1390','1391-1391','1392-1392','1393-1393','1394-1394','1395-1395','1396-1396','1397-1397','1398-1398','1399-1399','1400-1400','1401-1401']
usage = ['0-25000','25000-80000','80000-150000','150000-300000','300000-600000']
        
#https://divar.ir/s/tabriz/car/pride/131/se?production-year=1393-1393&usage=0-60000
#https://divar.ir/s/tabriz/car/hyundai/sonata-nf/3300cc?production-year=1393-1393&usage=30000-60000
prideDatabase = popular_car_models[popular_car_models['model'] == 'pride']

counter = 0 

for j in range(24,prideDatabase.shape[0]):
    
    for i in range(len(year)):
        
        for k in range(len(usage)):
            
            if str(prideDatabase.iloc[j]['type']) == "nan":
                
                address = "https://divar.ir/s/tabriz/car/pride/"+str(prideDatabase.iloc[j]['sub_model'])+"?production-year="+ year[i]+"&usage="+ usage[k]
            else:
                address = "https://divar.ir/s/tabriz/car/pride/"+str(prideDatabase.iloc[j]['sub_model'])+"/"+str(prideDatabase.iloc[j]['type'])+"?production-year="+ year[i]+"&usage="+ usage[k]

            req = requests.get(address)
            #building the request 
            soup = BeautifulSoup(req.text, parser)
            
            try:
                #trying to read and analyze recieved data
                text = soup.find_all('script',{"type":"application/ld+json"})[1]

                text_one = str(text)
                ff = text_one[34:-9]
                text_two = ff[1:]
                df = pd.read_json(text_two)
                df1 = df[['offers', 'color', 'knownVehicleDamages', 'url','brand','productionDate','mileageFromOdometer','name', 'description', 'vehicleTransmission']]
                df2 = pd.concat([df1, df1["offers"].apply(pd.Series)], axis=1)
                df2 = df2[['price' , 'color', 'knownVehicleDamages', 'url','brand','productionDate','mileageFromOdometer','name', 'description', 'vehicleTransmission']]
                df2 = df2.rename(columns = {'name':'model'})
                df3 =pd.concat([df2, df2["brand"].apply(pd.Series)], axis=1)
                df3 = df3[['name','model','price' , 'color', 'knownVehicleDamages', 'url','productionDate','mileageFromOdometer', 'description', 'vehicleTransmission']]
                df4 = pd.concat([df3, df3["mileageFromOdometer"].apply(pd.Series)], axis=1)
                df4 = df4.rename(columns = {'value':'mileage'})
                df4 = df4[['name','model','color','mileage','vehicleTransmission','knownVehicleDamages', 'productionDate', 'url', 'description','price']]
                try:
                    dfExtra1 = pd.DataFrame(df4['model'].str.split('،').to_list(), columns=['model1','model2'])
                    df5 = pd.concat([df4[['name','color']], dfExtra1, df4[['mileage','vehicleTransmission','knownVehicleDamages', 'productionDate', 'url', 'description','price']]] , axis=1)
                except ValueError:
                    df5 = pd.concat([df4[['name','color','model']], df4[['mileage','vehicleTransmission','knownVehicleDamages', 'productionDate', 'url', 'description','price']]] , axis=1)
                    # in some cases which are rare the model column only contains one sigle word, above statement cover this rows by cathing a value error.
                    
                df5.drop(df5.index[df5['price'] == '0'], inplace = True)
                df6 = df5.reset_index(drop=True)
                counter = counter + 1
                time.sleep(3)
                
                if counter == 1:
                    print("Holla! -- we started scrapping Divar!")
                    df_Pop_merged = df6
                    print(address +" -- analyzed and added to the database")
                    time.sleep(5)
                else:
                    
                   df_Pop_merged = pd.concat([df_Pop_merged, df6], axis=0)
                   print(str(j) + " -- " + address +" -- analyzed and added to the database")
                   time.sleep(5)
                   
            except IndexError:
                print(str(j) + " -- " + address +" -- is not available")
                time.sleep(8)
            
            except KeyError:
                print(str(j) + " -- " + address +" -- not in the index")
                time.sleep(3)
                
            except ValueError:
                print(str(j) + " -- " + address +" -- has a value Error")
                time.sleep(3)
                
            except ProtocolError:
                print(str(j) + " -- " + address +" -- invalid Chunk length error happend !")
                
            except InvalidChunkLength:
                print(str(j) + " -- " + address +" -- invalid Chunk length error happend !")
                
            except ChunkedEncodingError:
                print(str(j) + " -- " + address +" -- invalid Chunk length error happend !")
              
                
            if counter%5 == 1:
                time.sleep(20)
            
            
        

today = datetime.date.today()
filename = 'PopularCars-'+today.strftime("%d-%m-%y")+'.xlsx'
df_Pop_merged.to_excel(filename,index=False)
