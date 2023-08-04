import pymysql.cursors

class my_sql_serv:
    def __init__(self, db_config) -> None:
        self.connection = pymysql.connect(host = db_config["mysql"]["host"],
                             user = db_config["mysql"]["user"],
                             password = db_config["mysql"]["password"],
                             database = db_config["mysql"]["database"],
                             cursorclass=pymysql.cursors.DictCursor)

    def find_channel_id(self, channel_name) -> str:
        with self.connection.cursor() as cursor:
            cursor.execute("select a.channel_id from basefortgbot888.Channels as a where a.channel_name = %s", channel_name)
            row = cursor.fetchone()
            if row != None:
                return row["channel_id"]
            return ""

    def update_channels(self, channel_name, channel_id) -> None:
        with self.connection.cursor() as cursor:
            if channel_id != None:
                cursor.execute("INSERT INTO basefortgbot888.Channels (channel_name, channel_id) VALUES (%s, %s)", (channel_name, channel_id))  
                self.connection.commit()   
       
