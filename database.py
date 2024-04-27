import sqlite3

class Database():
    def __init__(self):
        # Adatbázis inicializálása
        self.connection = sqlite3.connect('players.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS players (
                            id INTEGER PRIMARY KEY,
                            name TEXT)''')
        self.connection.commit()
        self.connection.close()