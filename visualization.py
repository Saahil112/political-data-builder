from arcgis.gis import GIS
from arcgis.geocoding import geocode
from IPython.display import display
import json
import pandas as pd
from config import *



def visualization(df):
    '''
    Using the ArcGIS REST API, this logs into the gis online account to open up the map of the 
    designated location with the datapoints corresponding to the queries, sampled, and aggregated 
    requests. 

    Input: Df: Pandas Dataframe
    Return: Opens a link for the ArcGIS data visualization map 
    '''
    gis = GIS(url='https://www.arcgis.com', username='sp21_cfp286', password='LoveData123')

    df = df.loc[:, ['jittered_lat', 'jittered_long']].dropna()
    df['jittered_lat'] = pd.to_numeric(df['jittered_lat'])
    df['jittered_long'] = pd.to_numeric(df['jittered_long'])
    coord = (df[['jittered_long', 'jittered_lat']])
    coord.columns = ['x', 'y']
    fc = gis.content.import_data(coord)
    fc_dict = dict(fc.properties)
    json_voters = json.dumps({"featureCollection": {"layers": [fc_dict]}})
    item_properties = {'title': 'Voters df',
                       'description': 'Example demonstrating conversion of pandas ' + \
                                      'dataframe object to a GIS item',
                       'text': json_voters,
                       'type': 'Feature Collection',
                       'acess': 'public'
                       }
    item = gis.content.add(item_properties)
    item.share(True)

    link_to_map = 'https://nyuds.maps.arcgis.com/home/webmap/viewer.html?useExisting=1&layers=' + str(item.id)
    return link_to_map