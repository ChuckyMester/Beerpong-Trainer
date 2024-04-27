import customtkinter as ctk
import tkinter as tk
from tkinter import simpledialog
from database import Database
import sqlite3


class MainWindow(ctk.CTk):

    # Inicializalas
    def __init__(self):
        super().__init__()
        self.title('Main Menu')
        self.geometry('200x200')

        # Adatbazis object meghivasa
        self.database = Database()

        # Tracker mod gomb
        tracker_button = ctk.CTkButton(self, text='Tracker')
        tracker_button.pack(pady=10)

        # Training mod
        trainer_button = ctk.CTkButton(self, text='Training')
        trainer_button.pack(pady=10)

        # Scores
        score_button = ctk.CTkButton(self, text='Scores')
        score_button.pack(pady=10)

        # Players
        players_button = ctk.CTkButton(self, text='Players', command=self.open_player_window)
        players_button.pack(pady=10)

    
    def open_player_window(self):
        player_window = PlayerWindow(self)
        player_window.mainloop()



class PlayerWindow(ctk.CTk):
        
        # Inicializalas
        def __init__(self, parent):
            super().__init__()
            self.title('Player Management')
            self.geometry('500x500')

            # Kapcsolat létrehozása az adatbázissal
            self.connection = sqlite3.connect('players.db')
            self.cursor = self.connection.cursor()

            # Szülőablak
            self.parent = parent

            # Scrollbar hozzáadása
            scrollbar = tk.Scrollbar(self)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            # Játékosok listájának megjelenítése
            self.player_listbox = tk.Listbox(self, yscrollcommand=scrollbar.set)
            self.player_listbox.pack(pady=10, fill=tk.BOTH, expand=True)
            scrollbar.config(command=self.player_listbox.yview)

            # Gombok a játékosok kezeléséhez
            add_button = ctk.CTkButton(self, text='Add Player', command=self.add_player)
            add_button.pack(pady=5)

            delete_button = ctk.CTkButton(self, text='Delete Player', command=self.delete_player)
            delete_button.pack(pady=5)

            # Jatekosok mutatasa
            self.show_players()


        def show_players(self):
            self.cursor.execute("SELECT * FROM players")
            players = self.cursor.fetchall()
            for player in players:
                self.player_listbox.insert(tk.END, player[1])

            
        def add_player(self):
            player_name = simpledialog.askstring('Player Name', 'Enter player name:')
            if player_name:
                self.cursor.execute("INSERT INTO players (name) VALUES (?)", (player_name,))
                self.connection.commit()
                self.player_listbox.insert(tk.END, player_name)


        def delete_player(self):
            selected_index = self.player_listbox.curselection()
            if selected_index:
                player_name = self.player_listbox.get(selected_index)
                self.cursor.execute("DELETE FROM players WHERE name=?", (player_name,))
                self.connection.commit()
                self.player_listbox.delete(selected_index)
        






app = MainWindow()
app.mainloop()