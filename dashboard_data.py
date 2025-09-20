from utils import *

class dashboard_data:

    def __init__(self, df, start_date, end_date):
        '''
        Creates a new instance of an address data dataframe
        that fall within a specific time period

        By default, an instance of this class will be created for
        address data within the last 7 days
        '''
        def etl(df):
            return (df.pipe(convert_timestamp, "data_updated_at")
                    .pipe(day_breakdown, "data_updated_at_timestamp", start_date, end_date)
            )
        self.df = etl(df)
        self.gdf = df_to_gdf(self.df, "point")
        self.start_date = start_date
        self.end_date = end_date
        self.dim = self.df.shape
        # display columns for dash data table
        self.display_cols = ["Address", "ZIP Code", "EAS SubID", "Parcel Number",
         "Block", "Lot", "complete_landmark_name", "direct_source", "data_updated_at"]

    def get_scatter_map(self, popup_name = "Address", popup_data = ["data_updated_at", "EAS SubID"]):
        '''
        Returns plotly express scatter map figure of given
        geodataframe

        Centers the map over San Francisco
        '''
        
        fig = plotly_scatter_map(self.gdf, popup_name, popup_data)
        return fig
    
    def get_display_df(self, start_date = None, end_date = None):
        '''
        Returns dataframe with set of columns for display on
        Dash Data Table

        Sorts the dataframe by timestamp and address
        '''
        data = day_breakdown(self.df, "data_updated_at_timestamp", self.start_date, self.end_date)
        return data[self.display_cols].sort_values(["data_updated_at",
                                                       "Address"], ascending = [False, True])