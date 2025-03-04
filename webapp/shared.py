
from pathlib import Path

import pandas as pd
import geopandas as gpd
from census import Census

CENSUS_KEY = '4d44b8d67afa803caa015e6449f42a84a44127c2'
app_dir = Path(__file__).parent

ca_fips = '06'
smc_fips = '081'
ssf_tracts = [
    '6001P',
    '6017',
    '6018P',
    '6019',
    '6020P',
    '6021',
    '6022',
    '6023P',
    '6024P',
    '6025',
    '6026',
    '6041.02P',
    '6042P'
]
sb_tracts = [
    '6023P',
    '6030P',
    '6035P',
    '6036P',
    '6037',
    '6038P',
    '6039P',
    '6040',
    '6041.01P',
    '6041.02P',
    '6042P',
    '6046P',
    '6135.01P'
]
tracts = ssf_tracts + sb_tracts
reformat = lambda tract: tract.replace('P', '')
tracts_reformatted = list(map(reformat, tracts))

print(app_dir)

census_tracts = gpd.read_file('../shapefiles/tl_2024_06_tract.shp')
ssf_sb_tracts = census_tracts[(census_tracts['COUNTYFP'] == smc_fips) & census_tracts['NAME'].isin(tracts_reformatted)]

daily_asds = pd.read_csv('../data/Daily ASDS 2018-2023 for South San Francisco San Bruno.csv')
hourly_asds = pd.read_csv('../data/Hourly ASDS 2018-2023 for South San Francisco San Bruno.csv')
metadata = gpd.read_file('../data/ASDS 2018-2023 for South San Francisco and San Bruno Metadata.csv', GEOM_POSSIBLE_NAMES="geometry", KEEP_GEOM_COLUMNS="NO")

c = Census(CENSUS_KEY)

df = pd.read_csv(app_dir / 'penguins.csv')


#c.acs5.state_county_tract('S2701', ca_fips, smc_fips, tracts)