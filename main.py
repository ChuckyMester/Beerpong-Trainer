import customtkinter as ctk
import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
from tkinter import ttk
from database import Database
import datetime
import helpers



# Fomenu ablak
class MainWindow(ctk.CTk):

    # Inicializalas
    def __init__(self):
        super().__init__()
        self.title('Main Menu')
        self.geometry('200x200')
        # Icon used from: https://www.flaticon.com
        self.iconbitmap(helpers.decide_logo_by_system())

        # Adatbazis object meghivasa
        self.database = Database()

        # Tracker mod gomb
        tracker_one_v_one_end_button = ctk.CTkButton(self, text='Tracker', command=self.open_tracker_window)
        tracker_one_v_one_end_button.pack(pady=10)

        # Training mod
        trainer_one_v_one_end_button = ctk.CTkButton(self, text='Training')
        trainer_one_v_one_end_button.pack(pady=10)

        # Scores
        score_one_v_one_end_button = ctk.CTkButton(self, text='Scores', command=self.open_score_window)
        score_one_v_one_end_button.pack(pady=10)

        # Players
        players_one_v_one_end_button = ctk.CTkButton(self, text='Players', command=self.open_player_window)
        players_one_v_one_end_button.pack(pady=10)

    
    def open_player_window(self):
        player_window = PlayerWindow(self)
        player_window.mainloop()


    def open_tracker_window(self):
        tracker_window = TrackerWindow(self)
        tracker_window.mainloop()

    def open_score_window(self):
        score_window = ScoreWindow(self)
        score_window.mainloop()



# Jatekos menedzsment ablak
class PlayerWindow(ctk.CTk):
        
        # Inicializalas
        def __init__(self, parent):
            super().__init__()
            self.title('Player Management')
            self.geometry('500x500')
            # Icon used from: https://www.flaticon.com
            self.iconbitmap(helpers.decide_logo_by_system())

            # Kapcsolat létrehozása az adatbázissal
            self.database = Database()

            # Szülőablak
            self.parent = parent

            # Scrollbar hozzáadása
            scrollbar = ttk.Scrollbar(self)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            # TreeView style beallitasa
            style = ttk.Style(self)
            style.theme_use('clam')  # A 'clam' téma jobban támogatja a testreszabást
            style.configure("Treeview", font=('Calibri', 15), rowheight=25, background="#28282B", fieldbackground="#28282B", foreground="#FFFFFF")
            style.configure("Treeview.Heading", font=('Calibri', 16, 'bold'))  # Fejlécek stílusának beállítása
            style.map('Treeview.Row', background=[('selected', '#347083')], foreground=[('selected', '#ffffff')])  # Kiválasztott sor háttérszíne

            # Treeview létrehozása és konfigurálása
            self.player_tree = ttk.Treeview(self, columns=("Name"), show="headings", yscrollcommand=scrollbar.set)
            self.player_tree.heading("Name", text="Name")
            self.player_tree.pack(pady=10, fill=tk.BOTH, expand=True)
            scrollbar.config(command=self.player_tree.yview)

            # Gombok a játékosok kezeléséhez
            add_one_v_one_end_button = ctk.CTkButton(self, text='Add Player', command=self.add_player)
            add_one_v_one_end_button.pack(pady=5)

            delete_one_v_one_end_button = ctk.CTkButton(self, text='Delete Player', command=self.delete_player)
            delete_one_v_one_end_button.pack(pady=5)

            # Jatekosok mutatasa
            self.show_players()


        # Jatekosok mutatasa
        def show_players(self):
            self.player_tree.delete(*self.player_tree.get_children())
            self.database.cursor.execute("SELECT name FROM players")
            players = self.database.cursor.fetchall()
            for name in players:
                self.player_tree.insert('', tk.END, values=name)


        # Jatekos hozzadasa
        def add_player(self):
            player_name = ctk.CTkInputDialog(text="Name:", title="Add player").get_input()
            if player_name:
                # Ellenőrizzük, hogy létezik-e már a játékos
                self.database.cursor.execute("SELECT * FROM players WHERE name=?", (player_name,))
                if self.database.cursor.fetchone() is not None:
                    messagebox.showerror("Error", "A player with this name already exists!")
                else:
                    self.database.cursor.execute("INSERT INTO players (name) VALUES (?)", (player_name,))
                    self.database.connection.commit()
                    self.show_players()

         
        # Elem torlese a Treeview-bol
        def delete_player(self):
            selected_item = self.player_tree.selection()
            if selected_item:
                player_name = self.player_tree.item(selected_item, "values")[0]  # A név kivétele
                self.database.cursor.execute("DELETE FROM players WHERE name=?", (player_name,))
                self.database.connection.commit()
                self.player_tree.delete(selected_item)
        


# Tracker jatekmod ablakai
class TrackerWindow(ctk.CTk):
    # Inicializalas
    def __init__(self, parent):
        super().__init__()
        self.title('Tracker')
        self.geometry('500x200')
        # Icon used from: https://www.flaticon.com
        self.iconbitmap(helpers.decide_logo_by_system())

        # Kapcsolat létrehozása az adatbázissal
        self.database = Database()

        # Szülőablak
        self.parent = parent

        # Játékmód választása címke
        self.mode_label = ctk.CTkLabel(self, text="Select Game Mode:")
        self.mode_label.pack(pady=10)

        # 1v1 rádiógomb
        self.mode_var = tk.IntVar(value=1)  # Alapértelmezett kiválasztva
        self.mode_1v1_one_v_one_end_button = ctk.CTkRadioButton(self, text="1v1", variable=self.mode_var, value=1)
        self.mode_1v1_one_v_one_end_button.pack(pady=4)

        # 2v2 rádiógomb
        self.mode_2v2_one_v_one_end_button = ctk.CTkRadioButton(self, text="2v2", variable=self.mode_var, value=0)
        self.mode_2v2_one_v_one_end_button.pack(pady=4)

        # Solo rádiógomb
        self.mode_solo_one_v_one_end_button = ctk.CTkRadioButton(self, text="Solo", variable=self.mode_var, value=2)
        self.mode_solo_one_v_one_end_button.pack(pady=4)

        # "Select" gomb
        self.select_one_v_one_end_button = ctk.CTkButton(self, text="Select", command=self.select_players)
        self.select_one_v_one_end_button.pack(pady=10)


    # Ha a modot kivalasztottuk, akkor valasszuk ki a jatekosokat
    def select_players(self):

        self.geometry('500x250')

        # Jelenlegi widgeteket kitoroljuk
        self.mode_label.pack_forget()
        self.mode_1v1_one_v_one_end_button.pack_forget()
        self.mode_2v2_one_v_one_end_button.pack_forget()
        self.select_one_v_one_end_button.pack_forget()
        self.mode_solo_one_v_one_end_button.pack_forget()

        # Jatekos varok
        self.player1_var = tk.StringVar()
        self.player2_var = tk.StringVar()
        self.player3_var = tk.StringVar()
        self.player4_var = tk.StringVar()

        # Jatekosok
        self.players = self.load_players()

        # Valasztott jatekmod alapjan ujrarendereljuk az ablakot
        # 1v1
        if self.mode_var.get() == 1:
            self.player1_label = ctk.CTkLabel(self, text="Player 1:")
            self.player1_label.pack(pady=5)
            self.player1_combo = ctk.CTkComboBox(self, variable=self.player1_var, state='readonly', values=self.players)
            self.player1_combo.pack(pady=5)

            self.player2_label = ctk.CTkLabel(self, text="Player 2:")
            self.player2_label.pack(pady=5)
            self.player2_combo = ctk.CTkComboBox(self, variable=self.player2_var, state='readonly', values=self.players)
            self.player2_combo.pack(pady=5)

            self.game_start_one_v_one_end_button = ctk.CTkButton(self, text='Start', command=lambda: self.prepare_game_window('1v1'))
            self.game_start_one_v_one_end_button.pack(pady=25)


        # 2v2
        elif self.mode_var.get() == 0:
            self.player1_label = ctk.CTkLabel(self, text="Player 1:")
            self.player1_label.pack(pady=5)
            self.player1_combo = ctk.CTkComboBox(self, variable=self.player1_var, state='readonly', values=self.players)
            self.player1_combo.pack(pady=5)

            self.player2_label = ctk.CTkLabel(self, text="Player 2:")
            self.player2_label.pack(pady=5)
            self.player2_combo = ctk.CTkComboBox(self, variable=self.player2_var, state='readonly', values=self.players)
            self.player2_combo.pack(pady=5)

            self.player3_label = ctk.CTkLabel(self, text="Player 3:")
            self.player3_label.pack(pady=5)
            self.player3_combo = ctk.CTkComboBox(self, variable=self.player3_var, state='readonly', values=self.players)
            self.player3_combo.pack(pady=5)

            self.player4_label = ctk.CTkLabel(self, text="Player 4:")
            self.player4_label.pack(pady=5)
            self.player4_combo = ctk.CTkComboBox(self, variable=self.player4_var, state='readonly', values=self.players)
            self.player4_combo.pack(pady=5)

            self.game_start_one_v_one_end_button = ctk.CTkButton(self, text='Start', command=lambda: self.prepare_game_window('2v2'))
            self.game_start_one_v_one_end_button.pack(pady=10)


        # Solo    
        elif self.mode_var.get() == 2:
            self.player1_label = ctk.CTkLabel(self, text="Player:")
            self.player1_label.pack(pady=(40,5))
            self.player1_combo = ctk.CTkComboBox(self, variable=self.player1_var, state='readonly', values=self.players)
            self.player1_combo.pack(pady=5)

            self.game_start_one_v_one_end_button = ctk.CTkButton(self, text='Start', command=lambda: self.prepare_game_window('solo'))
            self.game_start_one_v_one_end_button.pack(pady=25)


    def prepare_game_window(self, game_mode):
        # A kivalasztott neveket kirakjuk a valtozokba
        # Ha Solo
        self.player1_var.set(self.player1_combo.get())

        # Ha 2 jatekos van
        if game_mode == '1v1':
            self.player2_var.set(self.player2_combo.get())

        # Ha 4 jatekos van, a masik ketto valtozonak is adunk erteket
        if game_mode =='2v2':
            self.player3_var.set(self.player3_combo.get())
            self.player4_var.set(self.player4_combo.get())

        # 1v1 jatekmod eseteben ellenorzes, hogy van-e azonos nevu jatekos
        if game_mode == '1v1':
            # Letrehozunk egy halmazt, es azt vizsgaljuk, hogy van-e kozottuk azonos ertek
            if len({self.player1_var.get(), self.player2_var.get()}) < 2:
                messagebox.showerror("Error", "The 2 players can't be the same!")
                return
            if not self.player1_var.get() or not self.player2_var.get():
                messagebox.showerror("Error", "You need to choose 2 players!")
                print(self.player1_var.get(), self.player2_var.get())
                return

        # 2v2 jatekmod eseteben ellenorzes, hogy van-e azonos nevu jatekos
        if game_mode == '2v2':
            # Letrehozunk egy halmazt, es azt vizsgaljuk, hogy van-e kozottuk azonos ertek
            if len({self.player1_var.get(), self.player2_var.get(), self.player3_var.get(), self.player4_var.get()}) < 4:
                messagebox.showerror("Error", "The 2 players can't be the same!")
                return

        # Eddig hasznalt widgetek eltuntese
        self.player1_label.pack_forget()
        self.player1_combo.pack_forget()
        self.game_start_one_v_one_end_button.pack_forget()

        if game_mode == '1v1':
            self.player2_label.pack_forget()
            self.player2_combo.pack_forget()

        if game_mode == '2v2':
            self.player3_label.pack_forget()
            self.player3_combo.pack_forget()
            self.player4_label.pack_forget()
            self.player4_combo.pack_forget()

        # Tracker ablak megnyitasa valasztott jatekmodtol fuggoen
        match game_mode:
            case '1v1':
                self.one_v_one_tracker_window_starting_player()
            case '2v2':
                self.two_v_two_tracker_window()
            case 'solo':
                self.solo_tracker_window()


    # 1v1 Kezdojatekos kijelolese
    def one_v_one_tracker_window_starting_player(self):

        # Ablak meretnek valtoztatasa
        self.geometry('500x200')

        # Jatekosok valtozoba helyezese
        one_v_one_player1 = self.player1_var.get()
        one_v_one_player2 = self.player2_var.get()

        # Kezdojatekos eldontese
        self.starting_player_label = ctk.CTkLabel(self, text='Who will be the starting player?', font=('Arial',26))
        self.starting_player_label.pack(pady=20)

        self.starting_player_one_v_one_end_button1 = ctk.CTkButton(self, text=one_v_one_player1, font=('Arial',16), height=70, command=lambda: self.update_starting_player('1v1', one_v_one_player1, one_v_one_player2))
        self.starting_player_one_v_one_end_button1.place(rely=0.4, relx=0.2)

        self.starting_player_one_v_one_end_button2 = ctk.CTkButton(self, text=one_v_one_player2, font=('Arial',16), height=70, command=lambda: self.update_starting_player('1v1', one_v_one_player2, one_v_one_player1))
        self.starting_player_one_v_one_end_button2.place(rely=0.4, relx=0.5)


    # 1v1 Jatekablak
    def one_v_one_tracker_window(self, starting_player, other_player, p1hag=0, p2hag=0, p1mag=0, p2mag=0 ,p1tag=0, p2tag=0, p1dag=0, p2dag=0, p1tripleag=0, p2tripleag=0):

        # Widgetek eltuntetese as ablak meretenek atallitasa
        self.geometry('690x430')
        self.starting_player_label.pack_forget()
        self.starting_player_one_v_one_end_button1.place_forget()
        self.starting_player_one_v_one_end_button2.place_forget()

        # Valtozok a jatekhoz
        self.one_v_one_player1 = starting_player
        self.one_v_one_player2 = other_player
        self.one_v_one_player1_cups_left = 10
        self.one_v_one_player2_cups_left = 10
        self.one_v_one_player1_total_throws = 0
        self.one_v_one_player2_total_throws = 0
        self.one_v_one_player1_total_hits = 0
        self.one_v_one_player2_total_hits = 0
        self.one_v_one_player1_total_miss = 0
        self.one_v_one_player2_total_miss = 0
        self.one_v_one_starter_throw_happened = False # Kezdokor valtozo
        self.one_v_one_player1_doubles = 0
        self.one_v_one_player2_doubles = 0
        self.one_v_one_player1_triple = 0
        self.one_v_one_player2_triple = 0
        self.one_v_one_player1_throws_without_miss = 0 # Duplazashoz valtozo
        self.one_v_one_player2_throws_without_miss = 0 # Duplazashoz valtozo
        self.one_v_one_third_shot = False   # 3. dobas valtozo
        self.one_v_one_overtime_var = False
        self.one_v_one_player1_throw_before_overtime = 0 # Overtime elotti dopbasokat overtimenal atrakjuk ebbe a valtozoba
        self.one_v_one_player2_throw_before_overtime = 0 # Overtime elotti dopbasokat overtimenal atrakjuk ebbe a valtozoba
        self.one_v_one_player1_double_before_overtime = 0 # Overtime elotti duplakat overtimenal atrakjuk ebbe a valtozoba
        self.one_v_one_player2_double_before_overtime = 0 # Overtime elotti duplakat overtimenal atrakjuk ebbe a valtozoba
        self.one_v_one_overtime_started = False # Ha az overtime elkezdodott true-ra allitjuk majd
        self.one_v_one_player1_first_throw = False      # Ezek az overtimenal kellenek, hogy tudjuk hany dobasa van a jatekosnak, hogy visszaszalhasson
        self.one_v_one_player1_second_throw = False     # Ezek az overtimenal kellenek, hogy tudjuk hany dobasa van a jatekosnak, hogy visszaszalhasson
        self.one_v_one_player2_first_throw = False      # Ezek az overtimenal kellenek, hogy tudjuk hany dobasa van a jatekosnak, hogy visszaszalhasson
        self.one_v_one_player2_second_throw = False     # Ezek az overtimenal kellenek, hogy tudjuk hany dobasa van a jatekosnak, hogy visszaszalhasson
        self.one_v_one_overtime_first_throw = False    # Ha ket dobas van visszaszallni, megtortent-e az elso
        self.one_v_one_player1_throw_after_games = p1tag    # Ha a user folytatja a jatekot, akkor ebben a valtozoban taroljuk az elozo meccsek statisztikajat
        self.one_v_one_player2_throw_after_games = p2tag    # Ha a user folytatja a jatekot, akkor ebben a valtozoban taroljuk az elozo meccsek statisztikajat
        self.one_v_one_player1_double_after_game = p1dag    # Ha a user folytatja a jatekot, akkor ebben a valtozoban taroljuk az elozo meccsek statisztikajat
        self.one_v_one_player2_double_after_game = p2dag    # Ha a user folytatja a jatekot, akkor ebben a valtozoban taroljuk az elozo meccsek statisztikajat
        self.one_v_one_player1_hits_after_games = p1hag     # Ha a user folytatja a jatekot, akkor ebben a valtozoban taroljuk az elozo meccsek statisztikajat
        self.one_v_one_player2_hits_after_games = p2hag     # Ha a user folytatja a jatekot, akkor ebben a valtozoban taroljuk az elozo meccsek statisztikajat
        self.one_v_one_player1_miss_after_games = p1mag     # Ha a user folytatja a jatekot, akkor ebben a valtozoban taroljuk az elozo meccsek statisztikajat
        self.one_v_one_player2_miss_after_games = p2mag     # Ha a user folytatja a jatekot, akkor ebben a valtozoban taroljuk az elozo meccsek statisztikajat
        self.one_v_one_player1_triple_after_game = p1tripleag
        self.one_v_one_player2_triple_after_game = p2tripleag



        # Keret a címke számára a tetején
        self.one_v_one_top_frame = ctk.CTkFrame(self)
        self.one_v_one_top_frame.pack(pady=10, fill="x")

        # Soron levo jatekos label
        self.one_v_one_current_player_label = ctk.CTkLabel(self.one_v_one_top_frame, text="Soron levo jatekos:", font=("Arial", 24))
        self.one_v_one_current_player_label.pack(side='left', padx=(200,0))

        # Soron levo jatekos var label
        self.one_v_one_current_name_label = ctk.CTkLabel(self.one_v_one_top_frame, text=self.one_v_one_player1, font=("Arial", 24))
        self.one_v_one_current_name_label.pack(side='left', padx=25)

        # Player1 keret
        self.one_v_one_player1_frame = ctk.CTkFrame(self, width=240, height=100)
        self.one_v_one_player1_frame.pack(side="left", padx=10, pady=10, fill="both", expand=True)

        # Player2 keret
        self.one_v_one_player2_frame = ctk.CTkFrame(self, width=240, height=100)
        self.one_v_one_player2_frame.pack(side="right", padx=10, pady=10, fill="both", expand=True)

        # Player1 nev es fentlevo poharak
        self.one_v_one_player1_name_label = ctk.CTkLabel(self.one_v_one_player1_frame, text=self.one_v_one_player1, font=("Arial", 26))
        self.one_v_one_player1_name_label.pack(pady=(20, 5))
        self.one_v_one_player1_score_label = ctk.CTkLabel(self.one_v_one_player1_frame, text=str(self.one_v_one_player1_cups_left), font=("Arial", 24))
        self.one_v_one_player1_score_label.pack(pady=5)

        # Player1 gombok
        self.one_v_one_player1_button_frame = ctk.CTkFrame(self.one_v_one_player1_frame)
        self.one_v_one_player1_button_frame.pack(pady=10)
        self.one_v_one_player1_hit_button = ctk.CTkButton(self.one_v_one_player1_button_frame, text="Hit", command=lambda: self.one_v_one_hit(self.one_v_one_player1), fg_color="green", height=60, font=("Arial", 25))
        self.one_v_one_player1_hit_button.pack(side='left', padx=10)
        self.one_v_one_player1_miss_button = ctk.CTkButton(self.one_v_one_player1_button_frame, text="Miss", command=lambda: self.one_v_one_miss(self.one_v_one_player1), fg_color="red", height=60, font=("Arial", 25))
        self.one_v_one_player1_miss_button.pack(side='left', padx=10)

        # Player1 Total throw statisztika 
        self.one_v_one_player1_total_throws_stat_frame = ctk.CTkFrame(self.one_v_one_player1_frame)
        self.one_v_one_player1_total_throws_stat_frame.pack(pady=(20,0), fill="x")
        self.one_v_one_player1_total_throws_stat_label = ctk.CTkLabel(self.one_v_one_player1_total_throws_stat_frame, text="Total throws:", font=("Arial", 20))
        self.one_v_one_player1_total_throws_stat_label.pack(side='left', padx=10)
        self.one_v_one_player1_total_throws_var_label = ctk.CTkLabel(self.one_v_one_player1_total_throws_stat_frame, text=self.one_v_one_player1_total_throws + self.one_v_one_player1_throw_before_overtime + self.one_v_one_player1_throw_after_games, font=("Arial", 20))
        self.one_v_one_player1_total_throws_var_label.pack(side='left', padx=10)

        # Player1 Total hits statisztika 
        self.one_v_one_player1_total_hits_stat_frame = ctk.CTkFrame(self.one_v_one_player1_frame)
        self.one_v_one_player1_total_hits_stat_frame.pack(pady=0, fill="x")
        self.one_v_one_player1_total_hits_stat_label = ctk.CTkLabel(self.one_v_one_player1_total_hits_stat_frame, text="Total hits:", font=("Arial", 20))
        self.one_v_one_player1_total_hits_stat_label.pack(side='left', padx=10)
        self.one_v_one_player1_total_hits_var_label = ctk.CTkLabel(self.one_v_one_player1_total_hits_stat_frame, text=self.one_v_one_player1_total_hits + self.one_v_one_player1_hits_after_games, font=("Arial", 20))
        self.one_v_one_player1_total_hits_var_label.pack(side='left', padx=10)

        # Player1 Total miss statisztika 
        self.one_v_one_player1_total_miss_stat_frame = ctk.CTkFrame(self.one_v_one_player1_frame)
        self.one_v_one_player1_total_miss_stat_frame.pack(pady=0, fill="x")
        self.one_v_one_player1_total_miss_stat_label = ctk.CTkLabel(self.one_v_one_player1_total_miss_stat_frame, text="Total misses:", font=("Arial", 20))
        self.one_v_one_player1_total_miss_stat_label.pack(side='left', padx=10)
        self.one_v_one_player1_total_miss_var_label = ctk.CTkLabel(self.one_v_one_player1_total_miss_stat_frame, text=self.one_v_one_player1_total_miss + self.one_v_one_player1_miss_after_games, font=("Arial", 20))
        self.one_v_one_player1_total_miss_var_label.pack(side='left', padx=10)

        # Player1 Dupla statisztika 
        self.one_v_one_player1_doubles_stat_frame = ctk.CTkFrame(self.one_v_one_player1_frame)
        self.one_v_one_player1_doubles_stat_frame.pack(pady=0, fill="x")
        self.one_v_one_player1_doubles_stat_label = ctk.CTkLabel(self.one_v_one_player1_doubles_stat_frame, text="Doubles:", font=("Arial", 20))
        self.one_v_one_player1_doubles_stat_label.pack(side='left', padx=10)
        self.one_v_one_player1_doubles_var_label = ctk.CTkLabel(self.one_v_one_player1_doubles_stat_frame, text=self.one_v_one_player1_doubles + self.one_v_one_player1_double_before_overtime + self.one_v_one_player1_double_after_game, font=("Arial", 20))
        self.one_v_one_player1_doubles_var_label.pack(side='left', padx=10)

        # Player1 Tripla statisztika 
        self.one_v_one_player1_triple_stat_frame = ctk.CTkFrame(self.one_v_one_player1_frame)
        self.one_v_one_player1_triple_stat_frame.pack(pady=0, fill="x")
        self.one_v_one_player1_triple_stat_label = ctk.CTkLabel(self.one_v_one_player1_triple_stat_frame, text="Triples:", font=("Arial", 20))
        self.one_v_one_player1_triple_stat_label.pack(side='left', padx=10)
        self.one_v_one_player1_triple_var_label = ctk.CTkLabel(self.one_v_one_player1_triple_stat_frame, text=self.one_v_one_player1_triple + self.one_v_one_player1_triple_after_game, font=("Arial", 20))
        self.one_v_one_player1_triple_var_label.pack(side='left', padx=10)

        # Player1 Total percentage statisztika 
        self.one_v_one_player1_total_percentage_stat_frame = ctk.CTkFrame(self.one_v_one_player1_frame)
        self.one_v_one_player1_total_percentage_stat_frame.pack(pady=0, fill="x")
        self.one_v_one_player1_total_percentage_stat_label = ctk.CTkLabel(self.one_v_one_player1_total_percentage_stat_frame, text="Total percentage:", font=("Arial", 20))
        self.one_v_one_player1_total_percentage_stat_label.pack(side='left', padx=10)
        self.one_v_one_player1_total_percentage_var_label = ctk.CTkLabel(self.one_v_one_player1_total_percentage_stat_frame, text=f'{self.calculate_percentage(self.one_v_one_player1_total_hits + self.one_v_one_player1_hits_after_games, self.one_v_one_player1_total_throws + self.one_v_one_player1_throw_before_overtime + self.one_v_one_player1_throw_after_games)}%', font=("Arial", 20))
        self.one_v_one_player1_total_percentage_var_label.pack(side='left', padx=10)

        # Player2 nev es fentlevo poharak
        self.one_v_one_player2_name_label = ctk.CTkLabel(self.one_v_one_player2_frame, text=self.one_v_one_player2, font=("Arial", 26))
        self.one_v_one_player2_name_label.pack(pady=(20, 5))
        self.one_v_one_player2_score_label = ctk.CTkLabel(self.one_v_one_player2_frame, text=str(self.one_v_one_player2_cups_left), font=("Arial", 24))
        self.one_v_one_player2_score_label.pack(pady=5)

        # Player2 gombok
        self.one_v_one_player2_one_v_one_end_button_frame = ctk.CTkFrame(self.one_v_one_player2_frame)
        self.one_v_one_player2_one_v_one_end_button_frame.pack(pady=10)
        self.one_v_one_player2_hit_one_v_one_end_button = ctk.CTkButton(self.one_v_one_player2_one_v_one_end_button_frame, text="Hit", command=lambda: self.one_v_one_hit(self.one_v_one_player2), fg_color="green", height=60, font=("Arial", 25))
        self.one_v_one_player2_hit_one_v_one_end_button.pack(side='left', pady=2, padx=10)
        self.one_v_one_player2_miss_one_v_one_end_button = ctk.CTkButton(self.one_v_one_player2_one_v_one_end_button_frame, text="Miss", command=lambda: self.one_v_one_miss(self.one_v_one_player2), fg_color="red", height=60, font=("Arial", 25))
        self.one_v_one_player2_miss_one_v_one_end_button.pack(side='left', pady=2, padx=10)

        # Az elejen a player2 gombjait deaktivaljuk
        if self.one_v_one_starter_throw_happened == False:
            self.one_v_one_player2_hit_one_v_one_end_button.configure(state=ctk.DISABLED)
            self.one_v_one_player2_miss_one_v_one_end_button.configure(state=ctk.DISABLED)
        
        # Player2 Total throw statisztika 
        self.one_v_one_player2_total_throws_stat_frame = ctk.CTkFrame(self.one_v_one_player2_frame)
        self.one_v_one_player2_total_throws_stat_frame.pack(pady=(20,0), fill="x")
        self.one_v_one_player2_total_throws_stat_label = ctk.CTkLabel(self.one_v_one_player2_total_throws_stat_frame, text="Total throws:", font=("Arial", 20))
        self.one_v_one_player2_total_throws_stat_label.pack(side='left', padx=10)
        self.one_v_one_player2_total_throws_var_label = ctk.CTkLabel(self.one_v_one_player2_total_throws_stat_frame, text=self.one_v_one_player2_total_throws + self.one_v_one_player2_throw_before_overtime + self.one_v_one_player2_throw_after_games, font=("Arial", 20))
        self.one_v_one_player2_total_throws_var_label.pack(side='left', padx=10)

        # Player2 Total hits statisztika 
        self.one_v_one_player2_total_hits_stat_frame = ctk.CTkFrame(self.one_v_one_player2_frame)
        self.one_v_one_player2_total_hits_stat_frame.pack(pady=0, fill="x")
        self.one_v_one_player2_total_hits_stat_label = ctk.CTkLabel(self.one_v_one_player2_total_hits_stat_frame, text="Total hits:", font=("Arial", 20))
        self.one_v_one_player2_total_hits_stat_label.pack(side='left', padx=10)
        self.one_v_one_player2_total_hits_var_label = ctk.CTkLabel(self.one_v_one_player2_total_hits_stat_frame, text=self.one_v_one_player2_total_hits + self.one_v_one_player2_hits_after_games, font=("Arial", 20))
        self.one_v_one_player2_total_hits_var_label.pack(side='left', padx=10)

        # Player2 Total miss statisztika 
        self.one_v_one_player2_total_miss_stat_frame = ctk.CTkFrame(self.one_v_one_player2_frame)
        self.one_v_one_player2_total_miss_stat_frame.pack(pady=0, fill="x")
        self.one_v_one_player2_total_miss_stat_label = ctk.CTkLabel(self.one_v_one_player2_total_miss_stat_frame, text="Total misses:", font=("Arial", 20))
        self.one_v_one_player2_total_miss_stat_label.pack(side='left', padx=10)
        self.one_v_one_player2_total_miss_var_label = ctk.CTkLabel(self.one_v_one_player2_total_miss_stat_frame, text=self.one_v_one_player2_total_miss + self.one_v_one_player2_miss_after_games, font=("Arial", 20))
        self.one_v_one_player2_total_miss_var_label.pack(side='left', padx=10)

        # Player2 Dupla statisztika 
        self.one_v_one_player2_doubles_stat_frame = ctk.CTkFrame(self.one_v_one_player2_frame)
        self.one_v_one_player2_doubles_stat_frame.pack(pady=0, fill="x")
        self.one_v_one_player2_doubles_stat_label = ctk.CTkLabel(self.one_v_one_player2_doubles_stat_frame, text="Doubles:", font=("Arial", 20))
        self.one_v_one_player2_doubles_stat_label.pack(side='left', padx=10)
        self.one_v_one_player2_doubles_var_label = ctk.CTkLabel(self.one_v_one_player2_doubles_stat_frame, text=self.one_v_one_player2_doubles + self.one_v_one_player2_double_before_overtime + self.one_v_one_player2_double_after_game, font=("Arial", 20))
        self.one_v_one_player2_doubles_var_label.pack(side='left', padx=10)

        # Player2 Tripla statisztika 
        self.one_v_one_player2_triple_stat_frame = ctk.CTkFrame(self.one_v_one_player2_frame)
        self.one_v_one_player2_triple_stat_frame.pack(pady=0, fill="x")
        self.one_v_one_player2_triple_stat_label = ctk.CTkLabel(self.one_v_one_player2_triple_stat_frame, text="Triples:", font=("Arial", 20))
        self.one_v_one_player2_triple_stat_label.pack(side='left', padx=10)
        self.one_v_one_player2_triple_var_label = ctk.CTkLabel(self.one_v_one_player2_triple_stat_frame, text=self.one_v_one_player2_triple + self.one_v_one_player2_triple_after_game, font=("Arial", 20))
        self.one_v_one_player2_triple_var_label.pack(side='left', padx=10)

        # Player2 Total percentage statisztika 
        self.one_v_one_player2_total_percentage_stat_frame = ctk.CTkFrame(self.one_v_one_player2_frame)
        self.one_v_one_player2_total_percentage_stat_frame.pack(pady=0, fill="x")
        self.one_v_one_player2_total_percentage_stat_label = ctk.CTkLabel(self.one_v_one_player2_total_percentage_stat_frame, text="Total percentage:", font=("Arial", 20))
        self.one_v_one_player2_total_percentage_stat_label.pack(side='left', padx=10)
        self.one_v_one_player2_total_percentage_var_label = ctk.CTkLabel(self.one_v_one_player2_total_percentage_stat_frame, text=f'{self.calculate_percentage(self.one_v_one_player2_total_hits + self.one_v_one_player2_hits_after_games, self.one_v_one_player2_total_throws + self.one_v_one_player2_throw_before_overtime + self.one_v_one_player2_throw_after_games)}%', font=("Arial", 20))
        self.one_v_one_player2_total_percentage_var_label.pack(side='left', padx=10)

        # Shortcut gombok bevezetese
        self.bind('<Key-h>', self.one_v_one_handle_keypress)
        self.bind('<Key-m>', self.one_v_one_handle_keypress)


    #1v1 Hit funkcio
    def one_v_one_hit(self, player):
        match player:
            # Ha one_v_one_player1 hit
            case self.one_v_one_player1:
                # Ha a hosszabbitas nem aktiv
                if self.one_v_one_overtime_var == False and self.one_v_one_overtime_started == False:
                    self.one_v_one_player1_total_throws += 1
                    self.one_v_one_player1_total_hits += 1
                    self.one_v_one_player2_cups_left -= 1

                    # Dobasok nyomon kovetese a hosszabbitas vegett
                    if self.one_v_one_player1_first_throw == False:
                        self.one_v_one_player1_first_throw = True
                    elif self.one_v_one_player1_second_throw == False:
                        self.one_v_one_player1_second_throw = True
                    
                    # Labelek valtoztatasa
                    self.one_v_one_player1_total_throws_var_label.configure(text=self.one_v_one_player1_total_throws + self.one_v_one_player1_throw_before_overtime + self.one_v_one_player1_throw_after_games)
                    self.one_v_one_player1_total_hits_var_label.configure(text=self.one_v_one_player1_total_hits + self.one_v_one_player1_hits_after_games)
                    self.one_v_one_player1_total_percentage_var_label.configure(text=f'{self.calculate_percentage(self.one_v_one_player1_total_hits, self.one_v_one_player1_total_throws + self.one_v_one_player1_throw_before_overtime + self.one_v_one_player1_throw_after_games)}%')
                    self.one_v_one_player2_score_label.configure(text=self.one_v_one_player2_cups_left)

                    # Ha nem a 3. dobas
                    if self.one_v_one_third_shot == False:
                        # Egyhuzamban torteno hitek noveles
                        self.one_v_one_player1_throws_without_miss += 1

                        if self.one_v_one_player1_throws_without_miss == 2:
                            self.one_v_one_player1_doubles += 1
                            self.one_v_one_player1_doubles_var_label.configure(text=self.one_v_one_player1_doubles + self.one_v_one_player1_double_before_overtime + self.one_v_one_player1_double_after_game)
                            self.one_v_one_third_shot = True
                            self.one_v_one_check_endgame()
                            return
                    else:
                        self.one_v_one_player1_triple += 1
                        self.one_v_one_player1_triple_var_label.configure(text=self.one_v_one_player1_triple + self.one_v_one_player1_triple_after_game)
                        self.one_v_one_third_shot = False
                        self.one_v_one_player1_throws_without_miss = 0

                    # Aktiv jatekos cserejenek ellenorzese(Elso korben egybol cserelunk, mert a kezdes 1 labdaval tortenik)
                    if self.one_v_one_starter_throw_happened == False:
                        self.one_v_one_deactivate_button(self.one_v_one_player1)
                        self.one_v_one_player1_throws_without_miss = 0 # Visszaallitjuk a valtozot nullara, hogy ne szamolja hibasan a duplazast
                        self.one_v_one_starter_throw_happened = True

                    if self.one_v_one_player1_doubles % 2 == 0:
                        if self.one_v_one_player1_total_throws % 2 == 1:
                            self.one_v_one_deactivate_button(self.one_v_one_player1)
                    else:
                        if self.one_v_one_player1_total_throws % 2 == 0:
                            self.one_v_one_deactivate_button(self.one_v_one_player1)

                    # Jatek vegenek ellenorzese
                    self.one_v_one_check_endgame()
                
                # Addig kell dobni meg el nem eri a 0-at az ellenfel poharainak a szama
                elif self.one_v_one_overtime_var == True and self.one_v_one_overtime_started == False:
                    self.one_v_one_player1_total_throws += 1
                    self.one_v_one_player1_total_hits += 1
                    self.one_v_one_player2_cups_left -= 1

                    # Labelek valtoztatasa
                    self.one_v_one_player1_total_throws_var_label.configure(text=self.one_v_one_player1_total_throws + self.one_v_one_player1_throw_before_overtime + self.one_v_one_player1_throw_after_games)
                    self.one_v_one_player1_total_hits_var_label.configure(text=self.one_v_one_player1_total_hits + self.one_v_one_player1_hits_after_games)
                    self.one_v_one_player1_total_percentage_var_label.configure(text=f'{self.calculate_percentage(self.one_v_one_player1_total_hits, self.one_v_one_player1_total_throws + self.one_v_one_player1_throw_before_overtime + self.one_v_one_player1_throw_after_games)}%')
                    self.one_v_one_player2_score_label.configure(text=self.one_v_one_player2_cups_left)

                    # Ha sikerult ledobni az osszes hatrelevo poharat elinditjuk az overtimeot
                    if self.one_v_one_player2_cups_left == 0:
                        self.one_v_one_overtime_start()

                # 3v3 hosszabbitas
                else:
                    self.one_v_one_player1_total_throws += 1
                    self.one_v_one_player1_total_hits += 1
                    self.one_v_one_player2_cups_left -= 1

                    # Dobasok nyomon kovetese a hosszabbitas vegett a hosszabbitasban
                    if self.one_v_one_player1_first_throw == False:
                        self.one_v_one_player1_first_throw = True
                    elif self.one_v_one_player1_second_throw == False:
                        self.one_v_one_player1_second_throw = True
                    
                    # Labelek valtoztatasa
                    self.one_v_one_player1_total_throws_var_label.configure(text=self.one_v_one_player1_total_throws + self.one_v_one_player1_throw_before_overtime + self.one_v_one_player1_throw_after_games)
                    self.one_v_one_player1_total_hits_var_label.configure(text=self.one_v_one_player1_total_hits + self.one_v_one_player1_hits_after_games)
                    self.one_v_one_player1_total_percentage_var_label.configure(text=f'{self.calculate_percentage(self.one_v_one_player1_total_hits, self.one_v_one_player1_total_throws + self.one_v_one_player1_throw_before_overtime + self.one_v_one_player1_throw_after_games)}%')
                    self.one_v_one_player2_score_label.configure(text=self.one_v_one_player2_cups_left)

                    # Ha nem a 3. dobas
                    if self.one_v_one_third_shot == False:
                        # Egyhuzamban torteno hitek noveles
                        self.one_v_one_player1_throws_without_miss += 1

                        if self.one_v_one_player1_throws_without_miss == 2:
                            self.one_v_one_player1_doubles += 1
                            self.one_v_one_third_shot = True
                            self.one_v_one_check_endgame()
                            return
                    else:
                        self.one_v_one_player1_triple += 1
                        self.one_v_one_player1_triple_var_label.configure(text=self.one_v_one_player1_triple + self.one_v_one_player1_triple_after_game)
                        self.one_v_one_third_shot = False
                        self.one_v_one_player1_throws_without_miss = 0

                    # Aktiv jatekos cserejenek ellenorzese(Elso korben egybol cserelunk, mert a kezdes 1 labdaval tortenik)
                    if self.one_v_one_starter_throw_happened == False:
                        self.one_v_one_deactivate_button(self.one_v_one_player1)
                        self.one_v_one_player1_throws_without_miss = 0 # Visszaallitjuk a valtozot nullara, hogy ne szamolja hibasan a duplazast
                        self.one_v_one_starter_throw_happened = True

                    if self.one_v_one_player1_doubles % 2 == 0:
                        if self.one_v_one_player1_total_throws % 2 == 0:
                            self.one_v_one_deactivate_button(self.one_v_one_player1)
                    else:
                        if self.one_v_one_player1_total_throws % 2 == 1:
                            self.one_v_one_deactivate_button(self.one_v_one_player1)

                    # Jatek vegenek ellenorzese
                    self.one_v_one_check_endgame()


            # Ha player 2 hit
            case self.one_v_one_player2:
                # Ha a hosszabbitas nem aktiv
                if self.one_v_one_overtime_var == False and self.one_v_one_overtime_started == False:
                    self.one_v_one_player2_total_throws += 1
                    self.one_v_one_player2_total_hits += 1
                    self.one_v_one_player1_cups_left -= 1

                    # Dobasok nyomon kovetese a hosszabbitas vegett
                    if self.one_v_one_player2_first_throw == False:
                        self.one_v_one_player2_first_throw = True
                    elif self.one_v_one_player2_second_throw == False:
                        self.one_v_one_player2_second_throw = True

                    # Labelek megvaltoztatasa
                    self.one_v_one_player2_total_throws_var_label.configure(text=self.one_v_one_player2_total_throws + self.one_v_one_player2_throw_before_overtime + self.one_v_one_player2_throw_after_games)
                    self.one_v_one_player2_total_hits_var_label.configure(text=self.one_v_one_player2_total_hits + self.one_v_one_player2_hits_after_games)
                    self.one_v_one_player2_total_percentage_var_label.configure(text=f'{self.calculate_percentage(self.one_v_one_player2_total_hits, self.one_v_one_player2_total_throws + self.one_v_one_player2_throw_before_overtime + self.one_v_one_player2_throw_after_games)}%')
                    self.one_v_one_player1_score_label.configure(text=self.one_v_one_player1_cups_left)

                    # Ha nem a 3. dobas
                    if self.one_v_one_third_shot == False:
                        # Egyhuzamban torteno hitek noveles
                        self.one_v_one_player2_throws_without_miss += 1

                        if self.one_v_one_player2_throws_without_miss == 2:
                            self.one_v_one_player2_doubles += 1
                            self.one_v_one_player2_doubles_var_label.configure(text=self.one_v_one_player2_doubles + self.one_v_one_player2_double_before_overtime + self.one_v_one_player2_double_after_game)
                            self.one_v_one_third_shot = True
                            self.one_v_one_check_endgame()
                            return
                    else:
                        self.one_v_one_player2_triple += 1
                        self.one_v_one_player2_triple_var_label.configure(text=self.one_v_one_player2_triple + self.one_v_one_player2_triple_after_game)
                        self.one_v_one_third_shot = False
                        self.one_v_one_player2_throws_without_miss = 0

                    # Aktiv jatekos cserejenek ellenorzese(Elso korben egybol cserelunk, mert a kezdes 1 labdaval tortenik)        
                    if self.one_v_one_player2_doubles % 2 == 0:
                        if self.one_v_one_player2_total_throws % 2 == 0:
                            self.one_v_one_deactivate_button(self.one_v_one_player2)
                    else:
                        if self.one_v_one_player2_total_throws % 2 == 1:
                            self.one_v_one_deactivate_button(self.one_v_one_player2)

                    # Jatek vegenek ellenorzese
                    self.one_v_one_check_endgame()

                # Addig kell dobni meg el nem eri a 0-at az ellenfel poharainak a szama
                elif self.one_v_one_overtime_var == True and self.one_v_one_overtime_started == False:
                    self.one_v_one_player2_total_throws += 1
                    self.one_v_one_player2_total_hits += 1
                    self.one_v_one_player1_cups_left -= 1

                    # Labelek valtoztatasa
                    self.one_v_one_player2_total_throws_var_label.configure(text=self.one_v_one_player2_total_throws + self.one_v_one_player2_throw_before_overtime + self.one_v_one_player2_throw_after_games)
                    self.one_v_one_player2_total_hits_var_label.configure(text=self.one_v_one_player2_total_hits + self.one_v_one_player2_hits_after_games)
                    self.one_v_one_player2_total_percentage_var_label.configure(text=f'{self.calculate_percentage(self.one_v_one_player2_total_hits, self.one_v_one_player2_total_throws + self.one_v_one_player2_throw_before_overtime + self.one_v_one_player2_throw_after_games)}%')
                    self.one_v_one_player1_score_label.configure(text=self.one_v_one_player1_cups_left)
                    
                    # Ha sikerult ledobni az osszes hatrelevo poharat elinditjuk az overtimeot
                    if self.one_v_one_player1_cups_left == 0:
                        self.one_v_one_overtime_start()

                # 3v3 hosszabbitas
                else:
                    self.one_v_one_player2_total_throws += 1
                    self.one_v_one_player2_total_hits += 1
                    self.one_v_one_player1_cups_left -= 1

                    # Dobasok nyomon kovetese a hosszabbitas vegett a hosszabbitasban
                    if self.one_v_one_player2_first_throw == False:
                        self.one_v_one_player2_first_throw = True
                    elif self.one_v_one_player2_second_throw == False:
                        self.one_v_one_player2_second_throw = True

                    # Labelek megvaltoztatasa
                    self.one_v_one_player2_total_throws_var_label.configure(text=self.one_v_one_player2_total_throws + self.one_v_one_player2_throw_before_overtime + self.one_v_one_player2_throw_after_games)
                    self.one_v_one_player2_total_hits_var_label.configure(text=self.one_v_one_player2_total_hits + self.one_v_one_player2_hits_after_games)
                    self.one_v_one_player2_total_percentage_var_label.configure(text=f'{self.calculate_percentage(self.one_v_one_player2_total_hits, self.one_v_one_player2_total_throws + self.one_v_one_player2_throw_before_overtime + self.one_v_one_player2_throw_after_games)}%')
                    self.one_v_one_player1_score_label.configure(text=self.one_v_one_player1_cups_left)

                    # Ha nem a 3. dobas
                    if self.one_v_one_third_shot == False:
                        # Egyhuzamban torteno hitek noveles
                        self.one_v_one_player2_throws_without_miss += 1

                        if self.one_v_one_player2_throws_without_miss == 2:
                            self.one_v_one_player2_doubles += 1
                            self.one_v_one_third_shot = True
                            self.one_v_one_check_endgame()
                            return
                    else:
                        self.one_v_one_player2_triple += 1
                        self.one_v_one_player2_triple_var_label.configure(text=self.one_v_one_player2_triple + self.one_v_one_player2_triple_after_game)
                        self.one_v_one_third_shot = False
                        self.one_v_one_player2_throws_without_miss = 0

                    # Aktiv jatekos cserejenek ellenorzese(Elso korben egybol cserelunk, mert a kezdes 1 labdaval tortenik)        
                    if self.one_v_one_player2_doubles % 2 == 0:
                        if self.one_v_one_player2_total_throws % 2 == 0:
                            self.one_v_one_deactivate_button(self.one_v_one_player2)
                    else:
                        if self.one_v_one_player2_total_throws % 2 == 1:
                            self.one_v_one_deactivate_button(self.one_v_one_player2)

                    # Jatek vegenek ellenorzese
                    self.one_v_one_check_endgame()


    # 1v1 Miss funckio
    def one_v_one_miss(self, player):
        match player:
            # Ha one_v_one_player1 miss
            case self.one_v_one_player1:
                # Ha a hosszabbitas nem aktiv
                if self.one_v_one_overtime_var == False and self.one_v_one_overtime_started == False:
                    self.one_v_one_player1_total_throws += 1
                    self.one_v_one_player1_total_miss += 1

                    # Dobasok nyomon kovetese a hosszabbitas vegett
                    if self.one_v_one_player1_first_throw == False:
                        self.one_v_one_player1_first_throw = True
                    elif self.one_v_one_player1_second_throw == False:
                        self.one_v_one_player1_second_throw = True
                    
                    # Labelek valtoztatasa
                    self.one_v_one_player1_total_throws_var_label.configure(text=self.one_v_one_player1_total_throws + self.one_v_one_player1_throw_before_overtime + self.one_v_one_player1_throw_after_games)
                    self.one_v_one_player1_total_miss_var_label.configure(text=self.one_v_one_player1_total_miss + self.one_v_one_player1_miss_after_games)
                    self.one_v_one_player1_total_percentage_var_label.configure(text=f'{self.calculate_percentage(self.one_v_one_player1_total_hits, self.one_v_one_player1_total_throws + self.one_v_one_player1_throw_before_overtime + self.one_v_one_player1_throw_after_games)}%')

                    # Egyhuzamban torteno hitek 0-zasa  es 3. dobas valtozojanak visszaallitasa
                    self.one_v_one_player1_throws_without_miss = 0
                    if self.one_v_one_third_shot == True:
                        self.one_v_one_third_shot = False

                    # Aktiv jatekos cserejenek ellenorzese(Elso korben egybol cserelunk, mert a kezdes 1 labdaval tortenik)
                    if self.one_v_one_starter_throw_happened == False:
                        self.one_v_one_deactivate_button(self.one_v_one_player1)
                        self.one_v_one_starter_throw_happened = True

                    if self.one_v_one_player1_doubles % 2 == 0:
                        if self.one_v_one_player1_total_throws % 2 == 1:
                            self.one_v_one_deactivate_button(self.one_v_one_player1)
                    else:
                        if self.one_v_one_player1_total_throws % 2 == 0:
                            self.one_v_one_deactivate_button(self.one_v_one_player1)

                # Ha hosszabbitasert zajlo harcban miss instant Lose (Kiveve ha csk masodikra vagy harmadikra ment be)
                elif self.one_v_one_overtime_var == True and self.one_v_one_overtime_started == False:
                    self.one_v_one_player1_total_throws += 1
                    self.one_v_one_player1_total_miss += 1

                    # Ha egy pohara van az ellenfelnek, es masodikra ment be vagy triplabol
                    if self.one_v_one_player2_cups_left == 1:
                         if self.one_v_one_player2_second_throw == True or self.one_v_one_third_shot == True:
                            if self.one_v_one_overtime_first_throw == False:
                                self.one_v_one_overtime_first_throw = True
                                return
                        
                    self.one_v_one_check_endgame()
                
                # 3v3 hosszabbitas
                else:
                    self.one_v_one_player1_total_throws += 1
                    self.one_v_one_player1_total_miss += 1

                    # Dobasok nyomon kovetese a hosszabbitas vegett a hosszabbitasban
                    if self.one_v_one_player1_first_throw == False:
                        self.one_v_one_player1_first_throw = True
                    elif self.one_v_one_player1_second_throw == False:
                        self.one_v_one_player1_second_throw = True
                    
                    # Labelek valtoztatasa
                    self.one_v_one_player1_total_throws_var_label.configure(text=self.one_v_one_player1_total_throws + self.one_v_one_player1_throw_before_overtime + self.one_v_one_player1_throw_after_games)
                    self.one_v_one_player1_total_miss_var_label.configure(text=self.one_v_one_player1_total_miss + self.one_v_one_player1_miss_after_games)
                    self.one_v_one_player1_total_percentage_var_label.configure(text=f'{self.calculate_percentage(self.one_v_one_player1_total_hits, self.one_v_one_player1_total_throws + self.one_v_one_player1_throw_before_overtime + self.one_v_one_player1_throw_after_games)}%')

                    # Egyhuzamban torteno hitek 0-zasa  es 3. dobas valtozojanak visszaallitasa
                    self.one_v_one_player1_throws_without_miss = 0
                    if self.one_v_one_third_shot == True:
                        self.one_v_one_third_shot = False

                    # Aktiv jatekos csereje
                    if self.one_v_one_player1_doubles % 2 == 0:
                        if self.one_v_one_player1_total_throws % 2 == 0:
                            self.one_v_one_deactivate_button(self.one_v_one_player1)
                    else:
                        if self.one_v_one_player1_total_throws % 2 == 1:
                            self.one_v_one_deactivate_button(self.one_v_one_player1)

            # Ha player 2 miss
            case self.one_v_one_player2:
                # Ha a hosszabbitas nem aktiv
                if self.one_v_one_overtime_var == False and self.one_v_one_overtime_started == False:
                    self.one_v_one_player2_total_throws += 1
                    self.one_v_one_player2_total_miss += 1

                    # Dobasok nyomon kovetese a hosszabbitas vegett
                    if self.one_v_one_player2_first_throw == False:
                        self.one_v_one_player2_first_throw = True
                    elif self.one_v_one_player2_second_throw == False:
                        self.one_v_one_player2_second_throw = True

                    # Labelek megvaltoztatasa
                    self.one_v_one_player2_total_throws_var_label.configure(text=self.one_v_one_player2_total_throws + self.one_v_one_player2_throw_before_overtime + self.one_v_one_player2_throw_after_games)
                    self.one_v_one_player2_total_miss_var_label.configure(text=self.one_v_one_player2_total_miss + self.one_v_one_player2_miss_after_games)
                    self.one_v_one_player2_total_percentage_var_label.configure(text=f'{self.calculate_percentage(self.one_v_one_player2_total_hits, self.one_v_one_player2_total_throws + self.one_v_one_player2_throw_before_overtime + self.one_v_one_player2_throw_after_games)}%')

                    # Egyhuzamban torteno hitek 0-zasa es 3. dobas valtozojanak visszaallitasa
                    self.one_v_one_player2_throws_without_miss = 0
                    if self.one_v_one_third_shot == True:
                        self.one_v_one_third_shot = False

                    # Aktiv jatekos cserejenek ellenorzese(Elso korben egybol cserelunk, mert a kezdes 1 labdaval tortenik)        
                    if self.one_v_one_player2_doubles % 2 == 0:
                        if self.one_v_one_player2_total_throws % 2 == 0:
                            self.one_v_one_deactivate_button(self.one_v_one_player2)
                    else:
                        if self.one_v_one_player2_total_throws % 2 == 1:
                            self.one_v_one_deactivate_button(self.one_v_one_player2)

                # Ha hosszabbitasban miss instant Lose, kiveve ha csak masodikra vagy triplabol ment be
                elif self.one_v_one_overtime_var == True and self.one_v_one_overtime_started == False:
                    self.one_v_one_player2_total_throws += 1
                    self.one_v_one_player2_total_miss += 1

                    # Ha egy pohara van az ellenfelnek, es masodikra ment be
                    if self.one_v_one_player1_cups_left == 1:
                        if self.one_v_one_player1_second_throw == True or self.one_v_one_third_shot == True:
                            if self.one_v_one_overtime_first_throw == False:
                                self.one_v_one_overtime_first_throw = True
                                return
                    
                    self.one_v_one_check_endgame()

                # 3v3 hosszabbitas
                else:
                    self.one_v_one_player2_total_throws += 1
                    self.one_v_one_player2_total_miss += 1

                    # Dobasok nyomon kovetese a hosszabbitas vegett a hosszabbitasban
                    if self.one_v_one_player2_first_throw == False:
                        self.one_v_one_player2_first_throw = True
                    elif self.one_v_one_player2_second_throw == False:
                        self.one_v_one_player2_second_throw = True

                    # Labelek megvaltoztatasa
                    self.one_v_one_player2_total_throws_var_label.configure(text=self.one_v_one_player2_total_throws + self.one_v_one_player2_throw_before_overtime + self.one_v_one_player2_throw_after_games)
                    self.one_v_one_player2_total_miss_var_label.configure(text=self.one_v_one_player2_total_miss + self.one_v_one_player2_miss_after_games)
                    self.one_v_one_player2_total_percentage_var_label.configure(text=f'{self.calculate_percentage(self.one_v_one_player2_total_hits, self.one_v_one_player2_total_throws + self.one_v_one_player2_throw_before_overtime + self.one_v_one_player2_throw_after_games)}%')

                    # Egyhuzamban torteno hitek 0-zasa es 3. dobas valtozojanak visszaallitasa
                    self.one_v_one_player2_throws_without_miss = 0
                    if self.one_v_one_third_shot == True:
                        self.one_v_one_third_shot = False

                    # Aktiv jatekos cserejenek ellenorzese(Elso korben egybol cserelunk, mert a kezdes 1 labdaval tortenik)        
                    if self.one_v_one_player2_doubles % 2 == 0:
                        if self.one_v_one_player2_total_throws % 2 == 0:
                            self.one_v_one_deactivate_button(self.one_v_one_player2)
                    else:
                        if self.one_v_one_player2_total_throws % 2 == 1:
                            self.one_v_one_deactivate_button(self.one_v_one_player2)


    # Jatek vegenek ellenorzese
    def one_v_one_check_endgame(self):
        winner = None
        # Ha valamelyik jatekosnak 0 pohara maradt
        if self.one_v_one_player1_cups_left == 0 or self.one_v_one_player2_cups_left == 0:
            if self.one_v_one_player1_cups_left == 0:
                winner = self.one_v_one_player2
            if self.one_v_one_player2_cups_left == 0:
                winner = self.one_v_one_player1

            if self.one_v_one_overtime_var == False:
                self.one_v_one_overtime_started = False # Ha az egyik jatekos elerte a 0-at akkor kikapcsoljuk a valtozot, kulonben veget er a meccs
                self.one_v_one_overtime(winner)
            else:

                # Widgetek elfelejtese:
                self.one_v_one_top_frame.pack_forget()
                self.one_v_one_player1_frame.pack_forget()
                self.one_v_one_player2_frame.pack_forget()

                # Statisztika elmentese adatbazisba
                game_mode = '1v1'
                current_date = datetime.date.today()
                # Player1 statisztikaja
                p1_total_throws = self.one_v_one_player1_throw_before_overtime + self.one_v_one_player1_total_throws
                p1hits = self.one_v_one_player1_total_hits
                p1miss = self.one_v_one_player1_total_miss               
                p1double = self.one_v_one_player1_doubles + self.one_v_one_player1_double_before_overtime
                p1triple = self.one_v_one_player1_triple   
                p1_percentage = self.calculate_percentage(p1hits, p1_total_throws)
                # Adatbazishoz adas
                self.database.add_match(self.one_v_one_player1, game_mode, p1_total_throws, p1hits, p1miss, p1double, p1triple, p1_percentage, current_date)
                
                # Player2 statisztikaja
                p2_total_throws = self.one_v_one_player2_throw_before_overtime + self.one_v_one_player2_total_throws
                p2hits = self.one_v_one_player2_total_hits
                p2miss = self.one_v_one_player2_total_miss
                p2double = self.one_v_one_player2_doubles + self.one_v_one_player2_double_before_overtime
                p2triple = self.one_v_one_player2_triple
                p2_percentage = self.calculate_percentage(p2hits, p2_total_throws)
                # Adatbazishoz adas
                self.database.add_match(self.one_v_one_player2, game_mode, p2_total_throws, p2hits, p2miss, p2double, p2triple, p2_percentage, current_date)



                # Uj ablak generalasa a gyoztes mujtatasahoz
                self.geometry('500x200')
                # Győztes nevének kiírása
                self.one_v_one_winner_label = ctk.CTkLabel(self, text=f'Congratulations! The winner is {winner}!', font=("Arial", 26))
                self.one_v_one_winner_label.pack(pady=20)

                # Gombok a játék kezelésére
                self.one_v_one_end_button_frame = ctk.CTkFrame(self)
                self.one_v_one_end_button_frame.pack(pady=10)

                new_game_one_v_one_end_button = ctk.CTkButton(self.one_v_one_end_button_frame, text="New Game", command=self.one_v_one_new_game, height=50)
                new_game_one_v_one_end_button.pack(side="left", padx=10)

                continue_one_v_one_end_button = ctk.CTkButton(self.one_v_one_end_button_frame, text="Continue", command=self.one_v_one_continue_game, height=50)
                continue_one_v_one_end_button.pack(side="left", padx=10)


    # Overtime
    def one_v_one_overtime(self, winner):
        self.one_v_one_overtime_var = True
        match winner:
            case self.one_v_one_player1:
                self.one_v_one_player1_hit_button.configure(state=ctk.DISABLED)
                self.one_v_one_player1_miss_button.configure(state=ctk.DISABLED)
                self.one_v_one_player2_hit_one_v_one_end_button.configure(state=ctk.NORMAL)
                self.one_v_one_player2_miss_one_v_one_end_button.configure(state=ctk.NORMAL)

            case self.one_v_one_player2:
                self.one_v_one_player1_hit_button.configure(state=ctk.NORMAL)
                self.one_v_one_player1_miss_button.configure(state=ctk.NORMAL)
                self.one_v_one_player2_hit_one_v_one_end_button.configure(state=ctk.DISABLED)
                self.one_v_one_player2_miss_one_v_one_end_button.configure(state=ctk.DISABLED)

        self.one_v_one_change_check_active_player() # Aktiv jatekos nevenek ellenorzese

    
    # Overtime elinditasa a sikeres visszaszallok utan
    def one_v_one_overtime_start(self):

        # Gombok allapotabol megnezzuk ki lesz a kezdo jatekos
        if self.one_v_one_player1_hit_button.cget("state") == ctk.NORMAL: # Mivel utoljara az 1-es jatekos volt ezert 2-es lesz a kezdo

            # Gombok beallitasa
            self.one_v_one_player1_hit_button.configure(state=ctk.DISABLED)
            self.one_v_one_player1_miss_button.configure(state=ctk.DISABLED)
            self.one_v_one_player2_hit_one_v_one_end_button.configure(state=ctk.NORMAL)
            self.one_v_one_player2_miss_one_v_one_end_button.configure(state=ctk.NORMAL)

        else : # Ha a 2-es jatekos volt utoljara
            self.one_v_one_player1_hit_button.configure(state=ctk.NORMAL)
            self.one_v_one_player1_miss_button.configure(state=ctk.NORMAL)
            self.one_v_one_player2_hit_one_v_one_end_button.configure(state=ctk.DISABLED)
            self.one_v_one_player2_miss_one_v_one_end_button.configure(state=ctk.DISABLED)

        # Valtozok beallitasa
        self.one_v_one_overtime_var = False
        self.one_v_one_overtime_started = True
        self.one_v_one_player1_cups_left = 3
        self.one_v_one_player2_cups_left = 3
        self.one_v_one_player1_throw_before_overtime = self.one_v_one_player1_total_throws + self.one_v_one_player1_throw_before_overtime
        self.one_v_one_player2_throw_before_overtime = self.one_v_one_player2_total_throws + self.one_v_one_player2_throw_before_overtime
        self.one_v_one_player1_total_throws = 0
        self.one_v_one_player2_total_throws = 0
        self.one_v_one_player1_double_before_overtime = self.one_v_one_player1_doubles + self.one_v_one_player1_double_before_overtime
        self.one_v_one_player2_double_before_overtime = self.one_v_one_player2_doubles + self.one_v_one_player2_double_before_overtime
        self.one_v_one_player1_doubles = 0
        self.one_v_one_player2_doubles = 0
        self.one_v_one_player1_throws_without_miss = 0
        self.one_v_one_player2_throws_without_miss = 0
        self.one_v_one_overtime_first_throw = False
        self.one_v_one_player1_first_throw = False
        self.one_v_one_player1_second_throw = False
        self.one_v_one_player2_first_throw = False
        self.one_v_one_player2_second_throw = False
        self.one_v_one_third_shot = False

        # Labelek frissitese
        self.one_v_one_player2_score_label.configure(text=self.one_v_one_player2_cups_left)
        self.one_v_one_player1_score_label.configure(text=self.one_v_one_player1_cups_left)

        self.one_v_one_change_check_active_player() # Aktiv jatekos nevenek ellenorzese
        

    # Gomb aktivalasa az aktiv jatekosnak es deaktivalas a masiknak valami a soron levo jatekos felirat updatelese
    def one_v_one_deactivate_button(self, player):
        match player:
            case self.one_v_one_player1:
                self.one_v_one_player1_hit_button.configure(state=ctk.DISABLED)
                self.one_v_one_player1_miss_button.configure(state=ctk.DISABLED)

                self.one_v_one_player2_hit_one_v_one_end_button.configure(state=ctk.NORMAL)
                self.one_v_one_player2_miss_one_v_one_end_button.configure(state=ctk.NORMAL)

                # Dobasok resetelese
                self.one_v_one_player2_first_throw = False
                self.one_v_one_player2_second_throw = False
                self.one_v_one_player2_throws_without_miss = 0


            case self.one_v_one_player2:
                self.one_v_one_player1_hit_button.configure(state=ctk.NORMAL)
                self.one_v_one_player1_miss_button.configure(state=ctk.NORMAL)

                self.one_v_one_player2_hit_one_v_one_end_button.configure(state=ctk.DISABLED)
                self.one_v_one_player2_miss_one_v_one_end_button.configure(state=ctk.DISABLED)

                # Dobasok resetelese
                self.one_v_one_player1_first_throw = False
                self.one_v_one_player1_second_throw = False
                self.one_v_one_player1_throws_without_miss = 0
            
        self.one_v_one_change_check_active_player() # Aktiv jatekos nevenek ellenorzese


    # Jelenleg aktiv jatekos Label valtoztatasa
    def one_v_one_change_check_active_player(self):
        if self.one_v_one_player1_hit_button.cget("state") == ctk.NORMAL:
            self.one_v_one_current_name_label.configure(text=self.one_v_one_player1)
        else:
            self.one_v_one_current_name_label.configure(text=self.one_v_one_player2)


    # Ha 1v1-nel az uj jatekot valasztja
    def one_v_one_new_game(self):    

        # Jelenlegi widgeteket eltuntetjuk
        self.one_v_one_winner_label.pack_forget()
        self.one_v_one_end_button_frame.pack_forget()

        # Ujra meghivtjuk a tracker window methodot
        self.one_v_one_tracker_window(self.one_v_one_player2, self.one_v_one_player1)


    # Ha 1v1-nel a continue gamet valasztja, a statisztika megmarad, nem 0-zuk
    def one_v_one_continue_game(self):

        # Jelenlegi widgeteket eltuntetjuk
        self.one_v_one_winner_label.pack_forget()
        self.one_v_one_end_button_frame.pack_forget()

        # Valtozok beallitasa
        # A jatek logikajahoz szukseges valtozokat athelyezzuk csak tarolasra hasznalt valtozoba (Fontos hogy majd keresztbe adjuk az adatokat, mert masik jatekos lesz a kezdojatekos)
        player1 = self.one_v_one_player1
        player2 = self.one_v_one_player2
        player1_hits = self.one_v_one_player1_total_hits + self.one_v_one_player1_hits_after_games
        player2_hits = self.one_v_one_player2_total_hits + self.one_v_one_player2_hits_after_games
        player1_miss = self.one_v_one_player1_total_miss + self.one_v_one_player1_miss_after_games
        player2_miss = self.one_v_one_player2_total_miss + self.one_v_one_player2_miss_after_games
        player1_total_throw = self.one_v_one_player1_total_throws + self.one_v_one_player1_throw_before_overtime + self.one_v_one_player1_throw_after_games
        player2_total_throw = self.one_v_one_player2_total_throws + self.one_v_one_player2_throw_before_overtime + self.one_v_one_player2_throw_after_games
        player1_doubles = self.one_v_one_player1_doubles + self.one_v_one_player1_double_before_overtime + self.one_v_one_player1_double_after_game
        player2_doubles = self.one_v_one_player2_doubles + self.one_v_one_player2_double_before_overtime + self.one_v_one_player2_double_after_game
        player1_triples = self.one_v_one_player1_triple + self.one_v_one_player1_triple_after_game
        player2_triples = self.one_v_one_player2_triple + self.one_v_one_player2_triple_after_game

        # Ujrageneraljuk a tracker ablakot (Fontos, hogy az adatokat keresztbe adjuk at, aki itt p1 volt, az uj jatek p2 lesz! Ez a kezdojatekos csereje miatt fontos!)
        self.one_v_one_tracker_window(
            starting_player=player2,
            other_player=player1,
            p1hag=player2_hits,
            p2hag=player1_hits,
            p1mag=player2_miss,
            p2mag=player1_miss,
            p1tag=player2_total_throw,
            p2tag=player1_total_throw,
            p1dag=player2_doubles,
            p2dag=player1_doubles,
            p1tripleag=player1_triples,
            p2tripleag=player2_triples
            )






    # Solo jatekablak
    def solo_tracker_window(self, throws=0, hits=0, miss=0, double=0, triple=0):

        # Widgetek eltuntetese as ablak meretenek atallitasa
        self.geometry('690x430')

        # Valtozok a jatekhoz
        self.solo_player = self.player1_var.get()
        self.solo_cups_left = 10
        self.solo_total_throws = 0
        self.solo_total_throws_after_game = throws
        self.solo_hits = 0
        self.solo_hits_after_game = hits
        self.solo_miss = 0
        self.solo_miss_after_game = miss
        self.solo_double = 0
        self.solo_double_after_game = double
        self.solo_triple = 0
        self.solo_triple_after_game = triple
        self.solo_round = 0
        self.solo_first_throw = False
        self.solo_second_throw = False
        self.solo_third_throw = False
        self.solo_throw_without_miss = 0

        
        # Keret a címke számára a tetején
        self.solo_top_frame = ctk.CTkFrame(self)
        self.solo_top_frame.pack(pady=10, fill="x")

        # Jelenlegi rekordtarto label
        try:
            self.solo_player_record_name = self.database.get_record_holder_player('solo')
            self.solo_current_record_player = ctk.CTkLabel(self.solo_top_frame, text=f"Jelenlegi rekordot tartja: {self.solo_player_record_name}", font=("Arial", 24))
            self.solo_current_record_player.pack(side='left', padx=(200,0))
        except TypeError:
            self.solo_current_record_player = ctk.CTkLabel(self.solo_top_frame, text=f"Elso jatek: Nincs rekordtarto", font=("Arial", 24))
            self.solo_current_record_player.pack(side='left', padx=(200,0))

        # Player keret
        self.solo_player_frame = ctk.CTkFrame(self, width=240, height=100)
        self.solo_player_frame.pack(side="left", padx=10, pady=10, fill="both", expand=True)

        # Statisztika keret
        self.solo_stat_frame = ctk.CTkFrame(self, width=240, height=100)
        self.solo_stat_frame.pack(side="right", padx=10, pady=10, fill="both", expand=True)

        # Hatralevo poharak szama
        self.solo_player_name_label = ctk.CTkLabel(self.solo_player_frame, text=self.solo_player, font=("Arial", 26))
        self.solo_player_name_label.pack(pady=(20, 5))
        self.solo_player_score_label = ctk.CTkLabel(self.solo_player_frame, text=str(self.solo_cups_left), font=("Arial", 24))
        self.solo_player_score_label.pack(pady=5)

        # Player gombok
        self.solo_button_frame = ctk.CTkFrame(self.solo_player_frame)
        self.solo_button_frame.pack(pady=10)
        self.solo_hit_button = ctk.CTkButton(self.solo_button_frame, text="Hit", command=self.solo_hit_function, fg_color="green", height=60, font=("Arial", 25))
        self.solo_hit_button.pack(side='left', padx=10)
        self.solo_miss_button = ctk.CTkButton(self.solo_button_frame, text="Miss", command=self.solo_miss_function, fg_color="red", height=60, font=("Arial", 25))
        self.solo_miss_button.pack(side='left', padx=10)

        # Player Total throw statisztika 
        self.solo_total_throws_stat_frame = ctk.CTkFrame(self.solo_player_frame)
        self.solo_total_throws_stat_frame.pack(pady=(20,0), fill="x")
        self.solo_total_throws_stat_label = ctk.CTkLabel(self.solo_total_throws_stat_frame, text="Total throws:", font=("Arial", 20))
        self.solo_total_throws_stat_label.pack(side='left', padx=10)
        self.solo_total_throws_var_label = ctk.CTkLabel(self.solo_total_throws_stat_frame, text=self.solo_total_throws + self.solo_total_throws_after_game, font=("Arial", 20))
        self.solo_total_throws_var_label.pack(side='left', padx=10)

        # Player Total hits statisztika 
        self.solo_total_hits_stat_frame = ctk.CTkFrame(self.solo_player_frame)
        self.solo_total_hits_stat_frame.pack(pady=0, fill="x")
        self.solo_total_hits_stat_label = ctk.CTkLabel(self.solo_total_hits_stat_frame, text="Total hits:", font=("Arial", 20))
        self.solo_total_hits_stat_label.pack(side='left', padx=10)
        self.solo_total_hits_var_label = ctk.CTkLabel(self.solo_total_hits_stat_frame, text=self.solo_hits + self.solo_hits_after_game, font=("Arial", 20))
        self.solo_total_hits_var_label.pack(side='left', padx=10)

        # Player Total miss statisztika 
        self.solo_total_miss_stat_frame = ctk.CTkFrame(self.solo_player_frame)
        self.solo_total_miss_stat_frame.pack(pady=0, fill="x")
        self.solo_total_miss_stat_label = ctk.CTkLabel(self.solo_total_miss_stat_frame, text="Total misses:", font=("Arial", 20))
        self.solo_total_miss_stat_label.pack(side='left', padx=10)
        self.solo_total_miss_var_label = ctk.CTkLabel(self.solo_total_miss_stat_frame, text=self.solo_miss + self.solo_miss_after_game, font=("Arial", 20))
        self.solo_total_miss_var_label.pack(side='left', padx=10)

        # Player Dupla statisztika 
        self.solo_double_stat_frame = ctk.CTkFrame(self.solo_player_frame)
        self.solo_double_stat_frame.pack(pady=0, fill="x")
        self.solo_double_stat_label = ctk.CTkLabel(self.solo_double_stat_frame, text="Doubles:", font=("Arial", 20))
        self.solo_double_stat_label.pack(side='left', padx=10)
        self.solo_double_var_label = ctk.CTkLabel(self.solo_double_stat_frame, text=self.solo_double + self.solo_double_after_game, font=("Arial", 20))
        self.solo_double_var_label.pack(side='left', padx=10)

        # Player Tripla statisztika 
        self.solo_triple_stat_frame = ctk.CTkFrame(self.solo_player_frame)
        self.solo_triple_stat_frame.pack(pady=0, fill="x")
        self.solo_triple_stat_label = ctk.CTkLabel(self.solo_triple_stat_frame, text="Triples:", font=("Arial", 20))
        self.solo_triple_stat_label.pack(side='left', padx=10)
        self.solo_triple_var_label = ctk.CTkLabel(self.solo_triple_stat_frame, text=self.solo_triple + self.solo_triple_after_game, font=("Arial", 20))
        self.solo_triple_var_label.pack(side='left', padx=10)

        # Player Total percentage statisztika 
        self.solo_total_percentage_stat_frame = ctk.CTkFrame(self.solo_player_frame)
        self.solo_total_percentage_stat_frame.pack(pady=0, fill="x")
        self.solo_total_percentage_stat_label = ctk.CTkLabel(self.solo_total_percentage_stat_frame, text="Total percentage:", font=("Arial", 20))
        self.solo_total_percentage_stat_label.pack(side='left', padx=10)
        self.solo_total_percentage_var_label = ctk.CTkLabel(self.solo_total_percentage_stat_frame, text=f'{self.calculate_percentage(self.solo_hits + self.solo_hits_after_game, self.solo_total_throws + self.solo_total_throws_after_game)}%', font=("Arial", 20))
        self.solo_total_percentage_var_label.pack(side='left', padx=10)

        # Statisztika kerethez tartozok labelek
        # Jatekos legjobb meccsenek lekerese
        try:
            best_match = self.database.get_record_for_actual_player(self.solo_player)
            total_throws = best_match[3]
            total_hits = best_match[4]
            total_miss = best_match[5]
            doubles = best_match[6]
            triples = best_match[7]
            percentage = best_match[8]
            date = best_match[9]
        except:
            total_throws = f"No data for {self.solo_player}"
            total_hits = f"No data for {self.solo_player}"
            total_miss = f"No data for {self.solo_player}"
            doubles = f"No data for {self.solo_player}"
            triples = f"No data for {self.solo_player}"
            percentage = f"No data for {self.solo_player}"
            date = f"No data for {self.solo_player}"


        # Legfelso label
        self.solo_statistic_title = ctk.CTkLabel(self.solo_stat_frame, text=f"{self.solo_player} legjobb jateka", font=("Arial", 26))
        self.solo_statistic_title.pack(padx=5, pady=(7, 15))

        # Osszes dobas
        self.solo_statistic_throws = ctk.CTkLabel(self.solo_stat_frame, text=f"Osszes dobas: {total_throws}", font=("Arial", 22))
        self.solo_statistic_throws.pack(padx=5, pady=7, anchor='w')

        # Osszes Hit
        self.solo_statistic_hits = ctk.CTkLabel(self.solo_stat_frame, text=f"Osszes Hit: {total_hits}", font=("Arial", 22))
        self.solo_statistic_hits.pack(padx=5, pady=7, anchor='w')

        # Osszes Miss
        self.solo_statistic_miss = ctk.CTkLabel(self.solo_stat_frame, text=f"Osszes Miss: {total_miss}", font=("Arial", 22))
        self.solo_statistic_miss.pack(padx=5, pady=7, anchor='w')

        # Osszes Dupla
        self.solo_statistic_double = ctk.CTkLabel(self.solo_stat_frame, text=f"Dupla: {doubles}", font=("Arial", 22))
        self.solo_statistic_double.pack(padx=5, pady=7, anchor='w')

        # Osszes Tripla
        self.solo_statistic_triple = ctk.CTkLabel(self.solo_stat_frame, text=f"Tripla: {triples}", font=("Arial", 22))
        self.solo_statistic_triple.pack(padx=5, pady=7, anchor='w')

        # Percentage
        self.solo_statistic_percentage = ctk.CTkLabel(self.solo_stat_frame, text=f"Szazalek: {percentage}%", font=("Arial", 22))
        self.solo_statistic_percentage.pack(padx=5, pady=7, anchor='w')

        # Jatszotta
        self.solo_statistic_date = ctk.CTkLabel(self.solo_stat_frame, text=f"Jatszotta: {date}", font=("Arial", 22))
        self.solo_statistic_date.pack(padx=5, pady=7, anchor='w')              


    # Solo hit funkció
    def solo_hit_function(self):
        self.solo_total_throws += 1
        self.solo_hits += 1
        self.solo_cups_left -= 1
        self.solo_throw_without_miss += 1

        if self.solo_first_throw == False:
            self.solo_first_throw = True
        elif self.solo_second_throw == False:
            self.solo_second_throw = True
        elif self.solo_throw_without_miss == 3 and self.solo_third_throw == False:
            self.solo_double += 1
            self.solo_triple += 1
            self.solo_round += 1
            self.solo_throw_without_miss = 0
            self.solo_first_throw = False
            self.solo_second_throw = False

        self.solo_update_labels()


    # Solo miss funkció
    def solo_miss_function(self):
        self.solo_total_throws += 1
        self.solo_miss += 1
        self.solo_throw_without_miss = 0

        if self.solo_first_throw == False:
            self.solo_first_throw = True
            self.solo_update_labels()
            return
        elif self.solo_second_throw == False:
            self.solo_second_throw = True
            self.solo_round += 1
        elif self.solo_third_throw == False:
            self.solo_third_throw = True
            self.solo_double += 1
            self.solo_round += 1

        self.solo_first_throw = False
        self.solo_second_throw = False
        self.solo_third_throw = False
        self.solo_update_labels()


    # Solo játékban a labelek frissítése minden dobás után
    def solo_update_labels(self):
        self.solo_total_throws_var_label.configure(text=self.solo_total_throws + self.solo_total_throws_after_game)
        self.solo_total_hits_var_label.configure(text=self.solo_hits + self.solo_hits_after_game)
        self.solo_total_miss_var_label.configure(text=self.solo_miss + self.solo_miss_after_game)
        self.solo_double_var_label.configure(text=self.solo_double + self.solo_double_after_game)
        self.solo_player_score_label.configure(text=self.solo_cups_left)
        self.solo_triple_var_label.configure(text=self.solo_triple + self.solo_triple_after_game)
        self.solo_total_percentage_var_label.configure(text=f'{self.calculate_percentage(self.solo_hits + self.solo_hits_after_game, self.solo_total_throws + self.solo_total_throws_after_game)}%')

        # Csekkoljuk, hogy véget ért-e a játék
        self.solo_check_end_game()


    # Solo játék vége
    def solo_check_end_game(self):
        # Ha a poharak száma elérte a 0-t akkor a játék véget ér
        if self.solo_cups_left == 0:
            self.solo_top_frame.pack_forget()
            self.solo_player_frame.pack_forget()
            self.solo_stat_frame.pack_forget()

            # Eredmények elmentése adatbázisba
            current_date = datetime.date.today()
            self.database.add_match(self.solo_player, 'solo', self.solo_total_throws, self.solo_hits, self.solo_miss, self.solo_double, self.solo_triple, self.calculate_percentage(self.solo_hits, self.solo_total_throws), current_date)

            # Uj ablak generalasa a játék végi menühöz
            self.geometry('500x200')
            # Győztes nevének kiírása
            self.solo_end_game_label = ctk.CTkLabel(self, text=f'A játék véget ért', font=("Arial", 26))
            self.solo_end_game_label.pack(pady=20)

            # Gombok a játék kezelésére
            self.solo_end_button_frame = ctk.CTkFrame(self)
            self.solo_end_button_frame.pack(pady=10)

            new_game_solo_end_button = ctk.CTkButton(self.solo_end_button_frame, text="New Game", command=lambda: self.solo_start_new_game('new game'), height=50)
            new_game_solo_end_button.pack(side="left", padx=10)

            continue_solo_end_button = ctk.CTkButton(self.solo_end_button_frame, text="Continue", command=lambda: self.solo_start_new_game('continue'), height=50)
            continue_solo_end_button.pack(side="left", padx=10)


    # Solo új játék
    def solo_start_new_game(self, option):
        
        # Ha teljes új játék
        if option != 'continue':
            self.solo_end_game_label.pack_forget()
            self.solo_end_button_frame.pack_forget()
            self.solo_tracker_window()

        # Ha pedig folytatás
        else:
            # Jelenlegi widgetek eltüntetése
            self.solo_end_game_label.pack_forget()
            self.solo_end_button_frame.pack_forget()

            # Változók átmentése a játék utáni változókba
            self.solo_tracker_window(
                throws=self.solo_total_throws + self.solo_total_throws_after_game,
                hits=self.solo_hits + self.solo_hits_after_game,
                miss=self.solo_miss + self.solo_miss_after_game,
                double=self.solo_double + self.solo_double_after_game,
                triple=self.solo_triple + self.solo_triple_after_game 
            )


    




    # 2v2 Jatekablak
    def two_v_two_tracker_window(self):
        print('2v2')






    # Gyorsbillentyu kezelese 1v1 jatekmodban
    def one_v_one_handle_keypress(self, event):
        match event.keysym:
            # Ha a h betut nyomjak le
            case 'h':
                if self.one_v_one_player1_hit_button.cget("state") == ctk.NORMAL:
                    self.one_v_one_hit(self.one_v_one_player1)
                else:
                    self.one_v_one_hit(self.one_v_one_player2)

            # Ha az m betut nyomjak le    
            case 'm':
                if self.one_v_one_player1_miss_button.cget("state") == ctk.NORMAL:
                    self.one_v_one_miss(self.one_v_one_player1)
                else:
                    self.one_v_one_miss(self.one_v_one_player2)

 
    # Kezdojatekos valtozoba helyezese
    def update_starting_player(self, mode, startingplayer, other_player):
        match mode:
            case '1v1':
                self.one_v_one_tracker_window(startingplayer, other_player)
            case '2v2':
                print('In work')
                # TODO


    # Szazalek szamitas
    def calculate_percentage(self, numerator, denominator):
        if denominator == 0:  # Nullával való osztás elkerülése
            return 100
        else:
            result = (numerator / denominator) * 100
            return round(result) # Kerekites


    # Jatekosok betoltese a comboboxokba
    def load_players(self):
        self.database.cursor.execute("SELECT name FROM players")
        players = self.database.cursor.fetchall()
        players_list = []
        for player in players:
            players_list.append(player[0])
        
        return players_list



# Score Window
class ScoreWindow(ctk.CTk):

    # Inicializalas
    def __init__(self, parent):
        super().__init__()
        self.title('Scores')
        self.geometry('1000x600')
        # Icon used from: https://www.flaticon.com
        self.iconbitmap(helpers.decide_logo_by_system())

        # Kapcsolat létrehozása az adatbázissal
        self.database = Database()

        # Szülőablak
        self.parent = parent

        # Bal és jobb keretek létrehozása
        self.score_frame_left = ctk.CTkFrame(self)
        self.score_frame_left.pack(side="left", fill="both", expand=True, padx=5, pady=10)

        self.score_frame_right = ctk.CTkFrame(self, width=240, height=500)
        self.score_frame_right.pack(side="right", fill="y", expand=False, padx=5, pady=10)

        # Bal oldali keretek
        self.score_frame_left_top = ctk.CTkFrame(self.score_frame_left, width=560, height=450)
        self.score_frame_left_top.pack(side="top", fill="both", expand=True, padx=10, pady=10)

        self.score_frame_left_bottom = ctk.CTkFrame(self.score_frame_left, width=560, height=200)
        self.score_frame_left_bottom.pack(side="top", fill="both", expand=True, padx=10, pady=10)

        # Treeview style
        style = ttk.Style(self)
        style.theme_use('clam')  # A 'clam' téma jobban támogatja a testreszabást
        style.configure("Treeview", background="#BDC8C8", fieldbackground="#b3d9ff")
        style.configure("Treeview", font=('Calibri', 15), rowheight=25, background="#28282B", fieldbackground="#28282B", foreground="#FFFFFF")

        # Treeview létrehozása
        self.score_tree = ttk.Treeview(self.score_frame_left_top, columns=("Player", "Throws", "Hits", "Miss", "Doubles", "Triples", "Percentage", "Date"), show="headings")
        self.score_tree.heading("Player", text="Player")
        self.score_tree.column("Player", width=140, anchor='center')
        self.score_tree.heading("Throws", text="Throws")
        self.score_tree.column("Throws", width=140, anchor='center')
        self.score_tree.heading("Hits", text="Hits")
        self.score_tree.column("Hits", width=140, anchor='center')
        self.score_tree.heading("Miss", text="Miss")
        self.score_tree.column("Miss", width=140, anchor='center')
        self.score_tree.heading("Doubles", text="Doubles")
        self.score_tree.column("Doubles", width=140, anchor='center')
        self.score_tree.heading("Triples", text="Triples")
        self.score_tree.column("Triples", width=140, anchor='center')
        self.score_tree.heading("Percentage", text="Percentage")
        self.score_tree.column("Percentage", width=140, anchor='center')
        self.score_tree.heading("Date", text="Date")
        self.score_tree.column("Date", width=140, anchor='center')
        self.score_tree.pack(expand=True, fill="both")

        # Bal also keret
        # Cím a bal alsó keretben
        self.score_title_label = ctk.CTkLabel(self.score_frame_left_bottom, text="Record Score for Player", font=('Helvetica', 14))
        self.score_title_label.pack(pady=(20, 10))

        # Jobb oldali elemek
        self.score_player_names_combobox = self.load_players()  #-------------------------------------------------->   Jatekosok neveinek comboboxba toltese
        self.score_player_combobox = ctk.CTkComboBox(self.score_frame_right, values=self.score_player_names_combobox)
        self.score_player_combobox.pack(pady=10, padx=5)

        self.score_game_modes_combobox = ['1v1', '2v2', 'Solo']
        self.score_game_mode_combobox = ctk.CTkComboBox(self.score_frame_right, values=self.score_game_modes_combobox)
        self.score_game_mode_combobox.pack(pady=10, padx=5)

        self.score_query_button = ctk.CTkButton(self.score_frame_right, text="Search", command=self.search_scores)
        self.score_query_button.pack(pady=15, padx=5)

        self.score_result_label = ctk.CTkLabel(self.score_frame_right, text="", font=('Helvetica', 14))
        self.score_result_label.pack(pady=10, padx=5)


    # Jatekosok betoltese a comboxba
    def load_players(self):
        query = "SELECT name FROM players"
        self.database.cursor.execute(query)
        players = [row[0] for row in self.database.cursor.fetchall()]
        return players
    

    # A megadott adatokkal kereses az adatbazisban
    def search_scores(self):
        player = self.score_player_combobox.get()
        game_mode = self.score_game_mode_combobox.get().lower()
        
        statistics = self.database.get_player_match_data(player, game_mode) # Összes statisztika lekérése
        best_percentage = None # Globális változó hogy megkeressük a legjobb meccsét
        best_match_id = None
        
        # Treeview kiuritese, mielott feltoltjuk ujabb adatokkal
        for data in self.score_tree.get_children():
            self.score_tree.delete(data)

        if len(statistics) == 0:
            print("No match data for that player!")
            return

        # Szétszedés és megjelenítés meccsenként
        for statistic in statistics:
            total_throws = statistic[3]
            total_hits = statistic[4]
            total_misses = statistic[5]
            doubles = statistic[6]
            triples = statistic[7]
            percentage = f"{statistic[8]}%"
            date = statistic[9]
            self.score_tree.insert('', tk.END, values=(player ,total_throws, total_hits, total_misses, doubles, triples, percentage, date))

            # Ha a változóban nincs még eredmény elmentjük az elsőt, utána meg ha nagyobb a jelenlegi iterácóban levő, akkor felülírjuk
            if best_percentage == None:
                best_percentage = statistic[8]
                best_match_id = statistic[0]
            elif statistic[8] > best_percentage:
                best_percentage = statistic[8]
                best_match_id = statistic[0]

        best_match_data = self.database.get_best_match_data(best_match_id)

        # Ha több megegyező százalékos meccset kapunk vissza, megjelenítjük a leglesőt
        best_match_data = best_match_data[0]
        print(f"Dobások száma:{best_match_data[3]}, Százalék: {best_match_data[8]}%")

        
            
        

    




app = MainWindow()
app.mainloop()