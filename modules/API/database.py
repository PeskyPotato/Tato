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
                id INTEGER PRIMARY KEY,
                link TEXT,
                new_link TEXT
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS stats (
                id TEXT PRIMARY KEY,
                timestamp INTEGER,
                ip TEXT,
                link_id REFERENCES links(id)
            )
        """)

    def insert_link(self, link, new_link):
        sql = """
            INSERT INTO links (
                link, new_link
            ) VALUES (
                ?, ?
            )
        """
        self.cursor.execute(sql, (link, new_link))
        self.__connection.commit()
        return self.cursor.lastrowid

    def select_link(self, link_id):
        sql = """
            SELECT * FROM links
            WHERE new_link = ?
        """
        self.cursor.execute(sql, (link_id, ))
        return self.cursor.fetchone()

    def select_links(self):
        sql = """
            SELECT * FROM links
            LIMIT 100
        """
        self.cursor.execute(sql, )
        return self.cursor.fetchall()
