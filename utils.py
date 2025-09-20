import pandas as pd
import geopandas as gpd
import plotly.express as px
from datetime import datetime, timedelta

def convert_timestamp(df, col):
    '''
    Converts dataframe column to timestamp column

    Adds an additional column of the same name with '_timestamp' appended
    '''
    timestamp = pd.to_datetime(df[col], format = "%Y/%m/%d %H:%M:%S %p")
    df[f"{col}_timestamp"] = timestamp
    return df

def day_breakdown(df, col, start_date, end_date):
    '''
    Returns the n-day breakdown of a dataframe starting from
    the date of when this function is invoked
    '''
    start = start_date.strftime("%Y/%m/%d %H:%M:%S %p")
    end = end_date.strftime("%Y/%m/%d %H:%M:%S %p")
    mask = (df[col] >= start) & (df[col] <= end)
    return df.loc[mask]

def df_to_gdf(df, col):
    '''
    Converts dataframe to geodataframe using the
    given column as WKT spatial data

    Uses CRS = EPSG:4326
    '''
    df_geom = gpd.GeoSeries.from_wkt(df[col])
    gdf = gpd.GeoDataFrame(data = df, geometry = df_geom, crs = "EPSG:4326")
    return gdf

def plotly_scatter_map(gdf, popup_name = "Address", popup_data = ["data_updated_at", "EAS SubID"]):
    '''
    Returns plotly express scatter map figure of given
    geodataframe

    Centers the map over San Francisco
    '''
    fig = px.scatter_map(gdf,
                    lat = gdf.geometry.y,
                    lon = gdf.geometry.x,
                    center = dict(lat = 37.7633748234765, lon = -122.44370085256286),
                    #37.7633748234765, -122.44370085256286
                    hover_name= popup_name,
                    hover_data = popup_data,
                    zoom=11,
                    width=800,
                    height=700,
                    opacity = 0.5)
    return fig