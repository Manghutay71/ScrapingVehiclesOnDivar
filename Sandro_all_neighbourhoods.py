# -*- coding: utf-8 -*-
"""
Created on Sat Oct  8 23:10:34 2022

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

#https://divar.ir/s/tehran/car/renault/sandero-stepway/automatic/aqdasiyeh 

counter = 0 

for j in range(82,neighbours_list.shape[0]):
    
    address = "https://divar.ir/s/"+str(neighbours_list.iloc[j]['city'])+"/car/renault/sandero-stepway/automatic/"+str(neighbours_list.iloc[j]['neighbour'])
    #print (address)

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
        df6['city'] = str(neighbours_list.iloc[j]['city'])
        df6['point'] = str(neighbours_list.iloc[j]['POINTS'])
        
        counter = counter + 1
        time.sleep(3)
        
        if counter == 1:
            print("Holla! -- we started scrapping Divar!")
            df_Sandro_merged = df6
            print(address +" -- analyzed and added to the database")
            time.sleep(2)
        else:
            
           df_Sandro_merged = pd.concat([df_Sandro_merged, df6], axis=0)
           print(str(j) + " -- " + address +" -- analyzed and added to the database")
           time.sleep(3)
           
    except IndexError:
        print(str(j) + " -- " + address +" -- is not available")
        time.sleep(3)
    
    except KeyError:
        print(str(j) + " -- " + address +" -- not in the index")
        time.sleep(3)
        
    except ValueError:
        print(str(j) + " -- " + address +" -- has a value Error")
        time.sleep(3)
      
        
    if counter%5 == 1:
        time.sleep(10)
        

today = datetime.date.today()
filename = 'SandroAutomatic_all_cities-'+today.strftime("%d-%m-%y")+'.xlsx'
df_Sandro_merged.to_excel(filename,index=False)
