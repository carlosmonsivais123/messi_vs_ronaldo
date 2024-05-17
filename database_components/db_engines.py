from sqlalchemy import create_engine

class DatabaseMYSQLEngine:
    def create_mysql_engine(self, mysql_username, mysql_password, mysql_host, mysql_port, mysql_db_name):
        engine=create_engine(f"mysql+pymysql://{mysql_username}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_db_name}")

        return engine
