import pandas as pd
import geopandas as gpd
import osmnx as ox
import networkx

def build_map_df(df):
    '''
    Loads Vilnius map and populates with latest date of apartments data on a street level.
    '''
    df = df[df['week']==df['week'].max()]
    streets = df.groupby('street')['price_sq_m'].agg(['mean'])
    streets['street_rank'] = pd.qcut(streets['mean'], q=5,  labels=[5, 4, 3,2,1])

    Vilnius_map = "Vilnius,Lithuania"
    graph = ox.graph_from_place(Vilnius_map)
    networkx.classes.multidigraph.MultiDiGraph

    nodes , streets_gdf = ox.graph_to_gdfs(graph)
    streets_gdf2 = pd.DataFrame(streets_gdf)
    streets_gdf2['street'] = streets_gdf2['name'].astype('str')
    streets2 = streets2 = streets.iloc[:,:0]

    streets_gdf2 = pd.merge(streets_gdf2, streets2, how='inner', left_on='street', right_on='street')
    streets_gdf = gpd.GeoDataFrame(streets_gdf2, geometry='geometry')
    streets_gdf = streets_gdf.reset_index()
    distinct_streets = streets_gdf.groupby('name').index.agg(['min'])
    streets_gdf = pd.merge(streets_gdf, distinct_streets, how='inner', left_on='index', right_on='min')


    return streets_gdf ,nodes

def coord_lister(geom):
    coords = list(geom.coords)
    return (coords)

def street_coordinates_maker(streets_gdf):
    streets_gdf['coordinates'] = streets_gdf.geometry.apply(coord_lister)
    coordinates = streets_gdf['coordinates']
    coordinates2 = {}
    for items in coordinates.iteritems():
        coordinates2[items[0]] = [items[1][0][1],items[1][0][0]]
    
    streets_gdf['coordinates'] = [(v) for v in coordinates2.values()]

    return streets_gdf






