import logging
import time

from configuration_vars.configuration import Config
from data_extraction.fbref_player_links_created import FBREFDataLinkCreation
from data_extraction.fbref_player_data_extraction import FBREFPlayerDataExtraction
from data_cleaning.clean_data import CleanData
from data_concatenation.dataframe_concat import CombineDataframes
from database_components.df_to_mysql import SendDFtoMYSQLDB

# Classes Being Called
logging.basicConfig(level=logging.INFO)
fbref_data_extraction_module=FBREFDataLinkCreation()
fbref_player_data_extraction=FBREFPlayerDataExtraction()
clean_data=CleanData()
combine_dataframes=CombineDataframes()
send_df_to_mysql_db=SendDFtoMYSQLDB(mysql_username=Config.MYSQL_USERNAME, 
                                    mysql_password=Config.MYSQL_PASSWORD, 
                                    mysql_host=Config.MYSQL_HOST, 
                                    mysql_port=Config.MYSQL_PORT, 
                                    mysql_db_name=Config.MYSQL_DB_NAME)

# Players That Data Will Be Extracted
players_list=[Config.PLAYER_1, Config.PLAYER_2]

player_dataframe_storage={}
for player in players_list:
    # Create Links That Will be Requested
    logging.info(f'Extracting {player} Player Links')
    player_links=fbref_data_extraction_module.execute_fbref_data_link_created(player_name=player)

    # Requesting Data From Links
    logging.info(f'Requesting {player} Player Links Data')
    player_data_df=fbref_player_data_extraction.execute_fbref_data_extraction(player_links_list=player_links)

    # Cleaning Data
    logging.info(f'Cleaning {player} Data')
    clean_data_df=clean_data.execute_data_cleaning(df=player_data_df, player_name=player)

    # Adding Dataframe to Storage Dictionary
    player_dataframe_storage[player]=clean_data_df

    # Waiting Period
    logging.info(f'Wating 30 Seconds For Next Player Request')
    time.sleep(30)


# Combine Dataframes from Dictionary
combined_player_dataframe=combine_dataframes.combine_dataframe_from_dict(player_data_dictionary=player_dataframe_storage)

# Send Data to DB
logging.info(f'Sending Data to MYSQL Database\n')
send_df_to_mysql_db.execute_df_to_mysql_db(df=combined_player_dataframe, 
                                           output_table_name=Config.MYSQL_TABLE_NAME)
