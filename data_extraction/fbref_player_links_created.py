import requests
from bs4 import BeautifulSoup
import re
import time

class FBREFDataLinkCreation:
    def format_player_name_for_link(self, player_name):
        player_name_formatted=player_name.replace(" ", "-")

        return player_name_formatted

        
    def player_unique_link_code_search(self, player_name):
        first_two_letters=player_name.split("-")[1][0:2].lower().strip()

        player_directory_text=requests.get(fr'https://fbref.com/en/players/{first_two_letters}/').text
        time.sleep(3)
        player_directory_link_text=BeautifulSoup(player_directory_text, features="html.parser")

        player_directory_link_search=player_directory_link_text.select(rf"a[href*= '/{player_name}']")
        player_directory_link=[i.attrs.get('href') for i in player_directory_link_search][0].strip()

        player_unique_identifier=player_directory_link.split('/')[3].strip()

        return player_unique_identifier


    def player_main_link_creator(self, player_name, player_unique_identifier):
        main_link=rf"https://fbref.com/en/players/{player_unique_identifier}/all_comps/{player_name}-Stats---All-Competitions"
       
        return main_link

    
    def season_matchlog_links(self, player_name, fbref_player_url):
        player_link_text=requests.get(fbref_player_url).text
        time.sleep(3)

        soup_player_link_text=BeautifulSoup(player_link_text, features="html.parser")

        player_seasons_links=soup_player_link_text.select(rf"a[href*= '/summary/{player_name}-Match-Logs']")
        player_seasons_links_list=[i.attrs.get('href') for i in player_seasons_links]

        # Removing national team stats since they are already included in season stats
        national_team_filter_regex=re.compile(r"nat\_tm")
        player_seasons_links_list_filter_1=[i for i in player_seasons_links_list if not national_team_filter_regex.search(i)]

        season_filter_regex_1=re.compile(r"matchlogs\/[0-9]{4}-[0-9]{4}\/summary")
        player_seasons_links_list_filter_2=[i for i in player_seasons_links_list_filter_1 if season_filter_regex_1.search(i)]

        season_filter_regex_2=re.compile(r"matchlogs\/[0-9]{4}\/summary")
        player_seasons_links_list_filter_3=[i for i in player_seasons_links_list_filter_1 if season_filter_regex_2.search(i)]

        player_seasons_links_list_filter_4=player_seasons_links_list_filter_2+player_seasons_links_list_filter_3

        player_seasons_links_list_filter_5=["https://fbref.com" + player_season_url for player_season_url in player_seasons_links_list_filter_4]
        player_seasons_links_list_filter_5=list(set(player_seasons_links_list_filter_5))

        return player_seasons_links_list_filter_5



    def execute_fbref_data_link_created(self, player_name):
        formatted_player_name=self.format_player_name_for_link(player_name=player_name)

        player_identifier=self.player_unique_link_code_search(player_name=formatted_player_name)

        player_main_link=self.player_main_link_creator(player_name=formatted_player_name, 
                                                       player_unique_identifier=player_identifier) 
        
        player_season_matchlog_links=self.season_matchlog_links(player_name=formatted_player_name, 
                                                                fbref_player_url=player_main_link)
        
        return player_season_matchlog_links
