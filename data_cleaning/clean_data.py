import numpy as np

class CleanData:
    def result_splitting(self, df):
        df['result_temp']=df['result'].str.split(' ', n=1).str[0].str.strip()
        df['result_score']=df['result'].str.split(' ', n=1).str[1].str.strip()

        df=df.drop(columns=['result'], inplace=False)
        df=df.rename(columns={'result_temp': 'result'})

        return df
    

    def penalty_shoot_out(self, df):
        penalty_shoot_out_pattern=r"^\d\s+\(\d\)"
        df['penalty_shoot_out']=df['result_score'].str.match(penalty_shoot_out_pattern)
        df['penalty_shoot_out']=df['penalty_shoot_out'].replace({False: "N",
                                                                 True: "Y"})
        
        penalty_shoot_out_score_pattern=r"\(\d+\)"
        df['penalty_shoot_out_score']=df['result_score'].str.findall(penalty_shoot_out_score_pattern)
        df['penalty_shoot_out_score']=df['penalty_shoot_out_score'].apply(lambda y: np.nan if len(y)==0 else y)
        df["penalty_shoot_out_score_for"]=df["penalty_shoot_out_score"].str[0]
        df["penalty_shoot_out_score_against"]=df["penalty_shoot_out_score"].str[1]

        penalty_shoot_out_score_values_pattern=r"\d+"
        df['penalty_shoot_out_score_for']=df['penalty_shoot_out_score_for'].str.findall(penalty_shoot_out_score_values_pattern)
        df['penalty_shoot_out_score_against']=df['penalty_shoot_out_score_against'].str.findall(penalty_shoot_out_score_values_pattern)
        df["penalty_shoot_out_score_for"]=df["penalty_shoot_out_score_for"].str[0].astype(float)
        df["penalty_shoot_out_score_against"]=df["penalty_shoot_out_score_against"].str[0].astype(float)

        df.loc[df['penalty_shoot_out_score_for']>df["penalty_shoot_out_score_against"], 'result'] = 'W'
        df.loc[df['penalty_shoot_out_score_for']<df["penalty_shoot_out_score_against"], 'result'] = 'L'

        df=df.drop(columns=['penalty_shoot_out_score', 'result_score'], inplace=False)

        return df
    

    def fill_certain_na_values(self, df):
        df[['minutes', 'goals']]=df[['minutes', 'goals']].fillna(0)

        return df
    

    def player_name(self, df, player_name):
        df['player_name']=player_name

        df=df.fillna(value=np.nan)
        df=df.replace({np.nan: None,
                       '': None})

        return df
    

    def dataframe_final_format(self, df):
        df=df.sort_values(by='date', ascending=True, inplace=False)
        df=df.reset_index(drop=True, inplace=False)

        return df


    def execute_data_cleaning(self, df, player_name):
        df_clean_1=self.result_splitting(df=df)
        df_clean_2=self.penalty_shoot_out(df=df_clean_1)
        df_clean_3=self.fill_certain_na_values(df=df_clean_2)
        df_clean_4=self.player_name(df=df_clean_3, player_name=player_name)
        df_clean_5=self.dataframe_final_format(df=df_clean_4)

        return df_clean_5
