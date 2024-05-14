import sqlite3

class Database():

    def __init__(self):
        # Adatbázis inicializálása
        self.connection = sqlite3.connect('players.db')
        self.cursor = self.connection.cursor()
        self.create_players_table()
        self.create_matches_table()


    # Jatekosok tablajanak letrehozasa 
    def create_players_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY,
                name TEXT
            )
        ''')
        self.connection.commit()


    # Meccsek tablajanak letrehozasa
    def create_matches_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS matches (
                match_id INTEGER PRIMARY KEY,
                player_id INTEGER,
                mode TEXT,
                throws INTEGER,
                hits INTEGER,
                misses INTEGER,
                doubles INTEGER,
                triples INTEGER,
                percentage TEXT,
                date TEXT,
                FOREIGN KEY(player_id) REFERENCES players(id)
            )
        ''')
        self.connection.commit()

    # Egy jatekos meccsenek talahoz adasa
    def add_match(self, player_name, mode, throws, hits, misses, doubles, triples, percentage, date):

        player_id = self.get_player_id_by_name(player_name)

        if player_id is None:
            return "Player not found"
        
        self.cursor.execute('''
            INSERT INTO matches (player_id, mode, throws, hits, misses, doubles, triples, percentage, date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (player_id, mode, throws, hits, misses, doubles, triples, percentage, date))
        self.connection.commit()


    # Jatekos ID-janak megkeresese nev alapjan, hogy a meccset elmenthessuk az adatbazisba
    def get_player_id_by_name(self, name):

        self.cursor.execute('SELECT id FROM players WHERE name = ?', (name,))
        result = self.cursor.fetchone()
        return result[0] if result else None
    

    def get_player_name_by_id(self, id):
        self.cursor.execute('SELECT name FROM players WHERE id = ?', (id,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    

    # Kiválasztjuk az összes adatot a megfelelő névhez és játékmódhoz
    def get_player_match_data(self, player_name, game_mode):
        player_id = self.get_player_id_by_name(player_name)
        self.cursor.execute("SELECT * FROM matches WHERE player_id = ? AND mode = ?", (player_id, game_mode))
        results = self.cursor.fetchall()
        return results
    

    # Legjobb meccs lekérése percentage alapján
    def get_best_match_data(self, match_id):
        self.cursor.execute("SELECT * FROM matches WHERE match_id = ?", (match_id,))
        results = self.cursor.fetchall()
        return results
    

    # A solo jatekmodban a rekordot tarto jatekos nevenek lekerese
    def get_record_holder_player(self, game_mode):
        self.cursor.execute("SELECT player_id FROM matches WHERE mode = ? ORDER BY percentage DESC LIMIT 1", (game_mode,))
        player_id = self.cursor.fetchone()
        name = self.get_player_name_by_id(player_id[0])
        return name


    # Adatbázis kapcsolat bezárása
    def close(self):
        self.connection.close()