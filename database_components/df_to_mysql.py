from database_components.db_engines import DatabaseMYSQLEngine
from sqlalchemy.types import String, Date, Integer

class SendDFtoMYSQLDB:
    def __init__(self, mysql_username, mysql_password, mysql_host, mysql_port, mysql_db_name):
        self.mysql_username=mysql_username
        self.mysql_password=mysql_password
        self.mysql_host=mysql_host
        self.mysql_port=mysql_port
        self.mysql_db_name=mysql_db_name

        database_mysql_engine=DatabaseMYSQLEngine()
        self.mysql_engine=database_mysql_engine.create_mysql_engine(mysql_username=self.mysql_username, 
                                                                    mysql_password=self.mysql_password, 
                                                                    mysql_host=self.mysql_host, 
                                                                    mysql_port=self.mysql_port, 
                                                                    mysql_db_name=self.mysql_db_name)


    def execute_df_to_mysql_db(self, df, output_table_name):
        dtype_dict={'date': Date, 
                    'day_of_the_week': String(50), 
                    'competition': String(50), 
                    'round': String(50), 
                    'venue': String(50), 
                    'squad': String(50),
                    'opponent': String(50), 
                    'game_started': String(50), 
                    'position': String(50), 
                    'minutes': Integer(), 
                    'goals': Integer(), 
                    'assists': Integer(),
                    'pens_made': Integer(), 
                    'pens_attempted': Integer(), 
                    'shots_total': Integer(), 
                    'shots_on_target': Integer(),
                    'cards_yellow': Integer(), 
                    'cards_red': Integer(), 
                    'fouls': Integer(), 
                    'fouled': Integer(), 
                    'offsides': Integer(), 
                    'crosses': Integer(), 
                    'tackles_won': Integer(), 
                    'interceptions': Integer(), 
                    'own_goals': Integer(), 
                    'touches': Integer(), 
                    'tackle': Integer(), 
                    'blocks': Integer(), 
                    'shot_creating_actions': Integer(), 
                    'goal-creating_actions': Integer(), 
                    'passes_completed': Integer(), 
                    'passes_attempted': Integer(), 
                    'carries': Integer(), 
                    'result': String(50), 
                    'penalty_shoot_out': String(50), 
                    'penalty_shoot_out_score_for': Integer(), 
                    'penalty_shoot_out_score_against': Integer(),
                    'player_name': String(50)}

        df.to_sql(name=output_table_name, 
                  con=self.mysql_engine,
                  dtype=dtype_dict,
                  if_exists='replace', 
                  index=False)
