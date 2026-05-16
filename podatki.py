api_gdp = 'https://ec.europa.eu/eurostat/api/dissemination/sdmx/3.0/data/dataflow/ESTAT/nama_10_gdp/1.0/*.*.*.*?c[freq]=A&c[unit]=CP_MEUR&c[na_item]=B1GQ&c[geo]=SI&c[TIME_PERIOD]=2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023,2024,2025&compress=false&format=json&lang=en'
api_inflation = 'https://ec.europa.eu/eurostat/api/dissemination/sdmx/3.0/data/dataflow/ESTAT/prc_hicp_aind/1.0/*.*.*.*?c[freq]=A&c[unit]=INX_A_AVG&c[coicop]=CP00&c[geo]=BE,BG,CZ,DK,DE,EE,IE,EL,ES,FR,HR,IT,CY,LV,LT,LU,HU,MT,NL,AT,PL,PT,RO,SI,SK,FI,SE,IS,NO,CH,UK,ME,MK,AL,RS,TR,XK,US&c[TIME_PERIOD]=2016,2017,2018,2019,2020,2021,2022,2023,2024,2025&compress=false&format=json&lang=en'
import json
from classes import Drzava
import matplotlib.pyplot as plt

 
#print(set(df['Unit of measure']))
drzave_gdp = Drzava.split_gdp_data_by_country(Drzava.acquire_data('eu_gdp.json'));
drzave_inflation = Drzava.split_inflation_data_by_country(Drzava.acquire_data('eu_inflation(HICP).json'));
#print(df.keys())
#print(df['National accounts indicator (ESA 2010)'])
#print(po_drzavah['Slovenia'])
drzave = dict()
for ime_drzave in drzave_inflation.keys():
    if ime_drzave in drzave_gdp:
        drzave[ime_drzave] = (Drzava(ime_drzave, drzave_gdp[ime_drzave]['Time'], drzave_gdp[ime_drzave]['value'], drzave_inflation[ime_drzave]['value']))
#for drzava in drzave:
#    print(drzava.name)