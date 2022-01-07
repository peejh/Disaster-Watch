from dbcrud import Session
from dbcrud import engine
from dbmodels import Place
import pandas as pd
import numpy as np

def insert_to_db(csvFile):
    pathfile = 'places/' + csvFile
    df = pd.read_csv(pathfile, na_filter=False)
    df = df.replace({np.nan: None})
    print(df.info())

    for index, row in df.iterrows():
        nomin_id = row['nomin_id']
        osm_id = row['osm_id']
        city = row['city']
        county = row['county']
        state = row['state']
        country = row['country']
        iso2 = row['iso2']
        lon = row['lon']
        lat = row['lat']
        zoom = row['zoom']
        bb_min_lat = row['bb_min_lat']
        bb_max_lat = row['bb_max_lat']
        bb_min_lon = row['bb_min_lon']
        bb_max_lon = row['bb_max_lon']
        bb_center_lat = row['bb_center_lat']
        bb_center_lon = row['bb_center_lon']
        display = row['display_name']
        display_ascii = row['display_ascii']
        city_ascii = row['city_ascii']
        osm_type = row['osm_type']
        place_class = row['place_class']
        place_type = row['place_type']
        importance = row['importance']

        place = Place(
            nomin_id = nomin_id,
            osm_id = osm_id,
            city = city,
            county = county,
            state = state,
            country = country,
            iso2 = iso2,
            lon = lon,
            lat = lat,
            zoom = zoom,
            bb_min_lat = bb_min_lat,
            bb_max_lat = bb_max_lat,
            bb_min_lon = bb_min_lon,
            bb_max_lon = bb_max_lon,
            bb_center_lat = bb_center_lat,
            bb_center_lon = bb_center_lon,
            display = display,
            display_ascii = display_ascii,
            city_ascii = city_ascii,
            osm_type = osm_type,
            place_class = place_class,
            place_type = place_type,
            importance = importance
        )

        session = Session()
        session.add(place)
        session.commit()
        session.close()


if __name__ == '__main__':

    placesFiles = ['country.withCoords.csv', 'provsNstates.withCoords.csv', 'worldcities.Canada.withCoords']

    for placesFile in placesFiles:
        insert_to_db(placesFile)
        