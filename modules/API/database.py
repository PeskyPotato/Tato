import sqlite3


class Database():
    def __init__(self, db_location):
        self.__DB_LOCATION = db_location
        self.__connection = sqlite3.connect(self.__DB_LOCATION)
        self.cursor = self.__connection.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS links (
                link_id TEXT PRIMARY KEY,
                link TEXT
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS stats (
                id INTEGER PRIMARY KEY,
                timestamp INTEGER,
                ip TEXT,
                link_id REFERENCES links(link_id)
            )
        """)

    def insert_link(self, link, link_id):
        sql = """
            INSERT INTO links (
                link, link_id
            ) VALUES (
                ?, ?
            )
        """
        self.cursor.execute(sql, (link, link_id))
        self.__connection.commit()
        return self.cursor.lastrowid

    def insert_stat(self, timestamp, ip, link_id):
        sql = """
            INSERT INTO stats (
                timestamp, ip, link_id
            ) VALUES (
                ?, ?, ?
            )
        """
        self.cursor.execute(sql, (timestamp, ip, link_id))
        self.__connection.commit()
        return self.cursor.lastrowid

    def select_link(self, link_id):
        sql = """
            SELECT * FROM links
            WHERE link_id = ?
        """
        self.cursor.execute(sql, (link_id, ))
        return self.cursor.fetchone()

    def select_links(self):
        sql = """
            SELECT l.link_id,
                l.link,
	            s.timestamp,
	            COUNT (s.timestamp) AS clicks
            FROM links AS l
            LEFT JOIN stats AS s On l.link_id = s.link_id
            GROUP BY l.link_id 
            LIMIT 100
        """
        sql2 = """
            SELECT s.timestamp,
	l.new_link,
	COUNT (*) AS clicks
FROM stats as s
LEFT JOIN links AS l ON l.new_link = s.link_id 
        """
        self.cursor.execute(sql, )
        return self.cursor.fetchall()
