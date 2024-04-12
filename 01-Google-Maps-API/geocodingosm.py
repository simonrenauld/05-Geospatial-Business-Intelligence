import requests
import numpy as np
from tqdm import tqdm

# function to geocode a location using OpenStreetMap Nominatim API
def geocode(location):
    url = 'https://nominatim.openstreetmap.org/search'
    params = {'q': location, 'format': 'json', 'limit': 1}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if len(data) > 0:
            return data[0]
    return None

# load the data from a CSV file
geocoded_data_osm_2nd_itteration =  pd.read_csv('geocoded_data_osm.csv')

# create new columns for cleaned city and district names
geocoded_data_osm_2nd_itteration['city_cleaned_osm'] = np.nan
geocoded_data_osm_2nd_itteration['district_cleaned_osm'] = np.nan

# clean and geocode the DeliveryAddress column for rows with NaN values in longitude or city/district columns
for index, row in tqdm(geocoded_data_osm_2nd_itteration.iterrows(), total=len(geocoded_data_osm_2nd_itteration)):
    if np.isnan(row['longitude_osm']) or np.isnan(row['city']) or np.isnan(row['district']):
        # clean the DeliveryAddress column
        address = row['DeliveryAddress'].lower()
        address = address.replace(',', '')
        address = address.replace('.', '')
        address = address.replace('phường', '')
        address = address.replace('p.', '')
        address = address.replace('xã', '')
        address = address.replace('tx.', '')
        address = address.replace('huyện', '')
        address = address.replace('thành phố', '')
        address = address.replace('tp.', '')
        address = address.strip()

        # add the division names to the address
        address = f"{address}, {row['level2_division_name']}, {row['level1_division_name']}"

        # geocode the cleaned address
        result = geocode(address)
        if result is not None and 'address' in result:
            df.at[index, 'city_cleaned'] = result['address'].get('city', np.nan)
            df.at[index, 'district_cleaned'] = result['address'].get('district', np.nan)
            df.at[index, 'longitude_geocoding'] = result['lon']
            df.at[index, 'latitude_geocoding'] = result['lat']

# save the updated data to a new CSV file
geocoded_data_osm_2nd_itteration.to_csv('geocoded_data_osm_2nd_itteration.csv', encoding='utf-8-sig', index=False)
