# -*- coding: utf-8 -*-
"""
Created on Mon Oct  3 23:34:00 2022

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


#writing code snippet for less popular cars, you can use other cities mentioned in information.xlsx file instead of Tabriz city

for j in range(0, less_popular_car_models.shape[0]):
    
    if str(less_popular_car_models['type'][j]) == "nan":
           address = "https://divar.ir/s/"+"tabriz/car/"+less_popular_car_models['model'][j]+"/"+str(less_popular_car_models['sub_model'][j])
    else:
        address = "https://divar.ir/s/"+"tabriz/car/"+less_popular_car_models['model'][j]+"/"+str(less_popular_car_models['sub_model'][j])+"/"+str(less_popular_car_models['type'][j])
    #above conditional statement is to cover some cars which there is  no type in their name
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
        
        time.sleep(5)
        
        if j==0:
            print("Holla! -- we started scrapping Divar!")
            df_lessPop_merged = df6
            print(str(j) + " -- " + address +" -- analyzed and added to the database")
        
        else:
            
           df_lessPop_merged = pd.concat([df_lessPop_merged, df6], axis=0)
           print(str(j) + " -- " + address +" -- analyzed and added to the database")
           
        if j%30 == 1:
            time.sleep(60)
            
            
    except IndexError:
        print(str(j) + " -- " + address +" -- is not available")
        time.sleep(3)
    except KeyError:
        print(str(j) + " -- " + address +" -- not in the index")
        time.sleep(3)
    except ConnectionResetError:
        print(" -- connection resetted by the host -- ")
        today = datetime.date.today()
        filename = 'LessPopularCars-'+today.strftime("%d-%m-%y")+'.xlsx'
        df_lessPop_merged.to_excel(filename,index=False)
        
        

today = datetime.date.today()
filename = 'LessPopularCars-'+today.strftime("%d-%m-%y")+'.xlsx'
df_lessPop_merged.to_excel(filename,index=False)