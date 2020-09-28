import pandas as pd
import geopandas as gpd
import osmnx as ox
import networkx

def build_map_df(df):
    '''
    Loads Vilnius map and populates with latest date of apartments data on a street level.
    '''
    df = df[df['week']==df['week'].max()]
    #df = df[df['age_segment']!='New (2019+)']
    streets = df.groupby('street')['price_sq_m'].agg(['mean', 'count'])
    streets['street_rank'] = pd.qcut(streets['mean'], q=3,  labels=[1,2,3])
    streets['street_size'] = pd.qcut(streets['count'], q=3,  labels=[1,2,3])
    streets_new = streets

    Vilnius_map = "Vilnius,Lithuania"
    graph = ox.graph_from_place(Vilnius_map)
    networkx.classes.multidigraph.MultiDiGraph

    nodes , streets_gdf = ox.graph_to_gdfs(graph)
    streets_gdf2 = pd.DataFrame(streets_gdf)
    streets_gdf2['street'] = streets_gdf2['name'].astype('str')
    streets2 = streets.iloc[:,:0]

    streets_gdf2 = pd.merge(streets_gdf2, streets2, how='inner', left_on='street', right_on='street')
    streets_gdf = gpd.GeoDataFrame(streets_gdf2, geometry='geometry')
    streets_gdf = streets_gdf.reset_index()
    distinct_streets = streets_gdf.groupby('name').index.agg(['min'])
    streets_gdf = pd.merge(streets_gdf, distinct_streets, how='inner', left_on='index', right_on='min')


    return streets_gdf ,nodes, streets_new

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
    streets_gdf[['coord1','coord2']] = pd.DataFrame(streets_gdf['coordinates'].to_list(), columns=['coord1','coord2'])

    return streets_gdf

    
def get_radius(loc,streets_gdf,streets_new):
    coord1 = loc[0]
    coord2 = loc[1]    
    st1 = streets_gdf.iloc[:]['street'][streets_gdf['coord1']==coord1]
    st2 = streets_new['street_size'][streets_new.index.isin(st1)]
    
    if  st2[0] == 1:
        return 3
    elif st2[0] == 2:
        return 6   
    else:
        return 10  

def get_description(loc,streets_gdf, streets_new):
    coord1 = loc[0]
    coord2 = loc[1]
    st1 = streets_gdf.iloc[:]['street'][streets_gdf['coord1']==coord1]
    count = streets_new['count'][streets_new.index.isin(st1)].values
    mean =  streets_new['mean'][streets_new.index.isin(st1)].values
    return "No of objects: "+str(count)+". Average price sq. m.: "+str(mean)[:5]+"]"

    
def get_colour(loc,streets_gdf,streets):
    coord1 = loc[0]
    coord2 = loc[1]    
    st1 = streets_gdf.iloc[:]['street'][streets_gdf['coord1']==coord1]
    st2 = streets['street_rank'][streets.index.isin(st1)]
    
    if  st2[0] == 3:
        return 'blue'
    elif st2[0] == 2:
        return 'green' 
    else:
        return 'yellow'
       
    






