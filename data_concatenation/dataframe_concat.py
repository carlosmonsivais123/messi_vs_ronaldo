import pandas as pd

class CombineDataframes:
    def combine_dataframe_from_dict(self, player_data_dictionary):
        final_df=pd.DataFrame()
        for value in player_data_dictionary.values():
            final_df=pd.concat([final_df, value])

        final_df=final_df.reset_index(drop=True, inplace=False)

        return final_df
