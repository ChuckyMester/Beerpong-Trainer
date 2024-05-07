import customtkinter as ctk
import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
from database import Database
import sqlite3


class MainWindow(ctk.CTk):

    # Inicializalas
    def __init__(self):
        super().__init__()
        self.title('Main Menu')
        self.geometry('200x200')
        # Icon used from: https://www.flaticon.com
        self.iconbitmap('assets/beerpong.ico')

        # Adatbazis object meghivasa
        self.database = Database()

        # Tracker mod gomb
        tracker_one_v_one_end_button = ctk.CTkButton(self, text='Tracker', command=self.open_tracker_window)
        tracker_one_v_one_end_button.pack(pady=10)

        # Training mod
        trainer_one_v_one_end_button = ctk.CTkButton(self, text='Training')
        trainer_one_v_one_end_button.pack(pady=10)

        # Scores
        score_one_v_one_end_button = ctk.CTkButton(self, text='Scores')
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



class PlayerWindow(ctk.CTk):
        
        # Inicializalas
        def __init__(self, parent):
            super().__init__()
            self.title('Player Management')
            self.geometry('500x500')
            # Icon used from: https://www.flaticon.com
            self.iconbitmap('assets/beerpong.ico')

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
            add_one_v_one_end_button = ctk.CTkButton(self, text='Add Player', command=self.add_player)
            add_one_v_one_end_button.pack(pady=5)

            delete_one_v_one_end_button = ctk.CTkButton(self, text='Delete Player', command=self.delete_player)
            delete_one_v_one_end_button.pack(pady=5)

            # Jatekosok mutatasa
            self.show_players()


        def show_players(self):
            self.cursor.execute("SELECT * FROM players")
            players = self.cursor.fetchall()
            for player in players:
                self.player_listbox.insert(tk.END, player[1])

            
        def add_player(self):
            player_name = ctk.CTkInputDialog(text="Name:", title="Add player")
            player_name = player_name.get_input()
            if player_name:
                self.cursor.execute("INSERT INTO players (name) VALUES (?)", (player_name,))
                self.connection.commit()
                self.player_listbox.insert(ctk.END, player_name)


        def delete_player(self):
            selected_index = self.player_listbox.curselection()
            if selected_index:
                player_name = self.player_listbox.get(selected_index)
                self.cursor.execute("DELETE FROM players WHERE name=?", (player_name,))
                self.connection.commit()
                self.player_listbox.delete(selected_index)
        


class TrackerWindow(ctk.CTk):
    # Inicializalas
    def __init__(self, parent):
        super().__init__()
        self.title('Tracker')
        self.geometry('500x200')
        # Icon used from: https://www.flaticon.com
        self.iconbitmap('assets/beerpong.ico')

        # Kapcsolat létrehozása az adatbázissal
        self.connection = sqlite3.connect('players.db')
        self.cursor = self.connection.cursor()

        # Szülőablak
        self.parent = parent

        # Játékmód választása címke
        self.mode_label = ctk.CTkLabel(self, text="Select Game Mode:")
        self.mode_label.pack(pady=10)

        # 1v1 rádiógomb
        self.mode_1v1_var = tk.IntVar(value=1)  # Alapértelmezett kiválasztva
        self.mode_1v1_one_v_one_end_button = ctk.CTkRadioButton(self, text="1v1", variable=self.mode_1v1_var, value=1)
        self.mode_1v1_one_v_one_end_button.pack()

        # 2v2 rádiógomb
        self.mode_2v2_var = tk.IntVar(value=0)
        self.mode_2v2_one_v_one_end_button = ctk.CTkRadioButton(self, text="2v2", variable=self.mode_1v1_var, value=0)
        self.mode_2v2_one_v_one_end_button.pack(pady=10)

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

        # Jatekos varok
        self.player1_var = tk.StringVar()
        self.player2_var = tk.StringVar()
        self.player3_var = tk.StringVar()
        self.player4_var = tk.StringVar()

        # Jatekosok
        self.players = self.load_players()

        # Valasztott jatekmod alapjan ujrarendereljuk az ablakot
        # 1v1
        if self.mode_1v1_var.get() == 1:
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
        elif self.mode_2v2_var.get() == 0:
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

    def prepare_game_window(self, game_mode):
        # A kivalasztott neveket kirakjuk a valtozokba
        self.player1_var.set(self.player1_combo.get())
        self.player2_var.set(self.player2_combo.get())
        # Ha 4 jatekos van, a masik ketto valtozonak is adunk erteket
        if game_mode =='2v2':
            self.player3_var.set(self.player3_combo.get())
            self.player4_var.set(self.player4_combo.get())

        # 1v1 jatekmod eseteben ellenorzes, hogy van-e azonos nevu jatekos
        if game_mode == '1v1':
            # Letrehozunk egy halmazt, es azt vizsgaljuk, hogy van-e kozottuk azonos ertek
            if len({self.player1_var.get(), self.player2_var.get()}) < 2:
                messagebox.showerror("Error", "Nem lehet azonos nevu jatekos")
                return

        # 2v2 jatekmod eseteben ellenorzes, hogy van-e azonos nevu jatekos
        if game_mode == '2v2':
            # Letrehozunk egy halmazt, es azt vizsgaljuk, hogy van-e kozottuk azonos ertek
            if len({self.player1_var.get(), self.player2_var.get(), self.player3_var.get(), self.player4_var.get()}) < 4:
                messagebox.showerror("Error", "Nem lehet azonos nevu jatekos")
                return

        # Eddig hasznalt widgetek eltuntese
        self.player1_label.pack_forget()
        self.player1_combo.pack_forget()
        self.player2_label.pack_forget()
        self.player2_combo.pack_forget()
        self.game_start_one_v_one_end_button.pack_forget()
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


    # 1v1 Kezdojatekos kijelolese
    def one_v_one_tracker_window_starting_player(self):

        # Ablak meretnek valtoztatasa
        self.geometry('500x200')

        # Jatekosok valtozoba helyezese
        one_v_one_player1 = self.player1_var.get()
        one_v_one_player2 = self.player2_var.get()

        # Kezdojatekos eldontese
        self.starting_player_label = ctk.CTkLabel(self, text='Ki lesz a kezdojatekos?', font=('Arial',26))
        self.starting_player_label.pack(pady=20)

        self.starting_player_one_v_one_end_button1 = ctk.CTkButton(self, text=one_v_one_player1, font=('Arial',16), height=70, command=lambda: self.update_starting_player('1v1', one_v_one_player1, one_v_one_player2))
        self.starting_player_one_v_one_end_button1.place(rely=0.4, relx=0.2)

        self.starting_player_one_v_one_end_button2 = ctk.CTkButton(self, text=one_v_one_player2, font=('Arial',16), height=70, command=lambda: self.update_starting_player('1v1', one_v_one_player2, one_v_one_player1))
        self.starting_player_one_v_one_end_button2.place(rely=0.4, relx=0.5)


    # 1v1 Jatekablak
    def one_v_one_tracker_window(self, starting_player, other_player, p1thits=0, p2thits=0, p1tmiss=0, p2tmiss=0 ,p1tbot=0, p2tbot=0, p1dbot=0, p2dbot=0):

        # Widgetek eltuntetese as ablak meretenek atallitasa
        self.geometry('690x420')
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
        self.one_v_one_player1_total_hits = p1thits
        self.one_v_one_player2_total_hits = p2thits
        self.one_v_one_player1_total_miss = p1tmiss
        self.one_v_one_player2_total_miss = p2tmiss
        self.one_v_one_starter_throw_happened = False # Kezdokor valtozo
        self.one_v_one_player1_doubles = 0
        self.one_v_one_player2_doubles = 0
        self.one_v_one_player1_throws_without_miss = 0 # Duplazashoz valtozo
        self.one_v_one_player2_throws_without_miss = 0 # Duplazashoz valtozo
        self.one_v_one_third_shot = False   # 3. dobas valtozo
        self.one_v_one_overtime_var = False
        self.one_v_one_player1_throw_before_overtime = p1tbot # Overtime elotti dopbasokat overtimenal atrakjuk ebbe a valtozoba
        self.one_v_one_player2_throw_before_overtime = p2tbot # Overtime elotti dopbasokat overtimenal atrakjuk ebbe a valtozoba
        self.one_v_one_player1_double_before_overtime = p1dbot # Overtime elotti duplakat overtimenal atrakjuk ebbe a valtozoba
        self.one_v_one_player2_double_before_overtime = p2dbot # Overtime elotti duplakat overtimenal atrakjuk ebbe a valtozoba
        self.one_v_one_overtime_started = False # Ha az overtime elkezdodott true-ra allitjuk majd
        self.one_v_one_player1_first_throw = False      # Ezek az overtimenal kellenek, hogy tudjuk hany dobasa van a jatekosnak, hogy visszaszalhasson
        self.one_v_one_player1_second_throw = False     # Ezek az overtimenal kellenek, hogy tudjuk hany dobasa van a jatekosnak, hogy visszaszalhasson
        self.one_v_one_player2_first_throw = False      # Ezek az overtimenal kellenek, hogy tudjuk hany dobasa van a jatekosnak, hogy visszaszalhasson
        self.one_v_one_player2_second_throw = False     # Ezek az overtimenal kellenek, hogy tudjuk hany dobasa van a jatekosnak, hogy visszaszalhasson
        self.one_v_one_overtime_first_throw = False    # Ha ket dobas van visszaszallni, megtortent-e az elso



        # Keret a címke számára a tetején
        self.one_v_one_top_frame = ctk.CTkFrame(self)
        self.one_v_one_top_frame.pack(pady=10, fill="x")

        # Soron levo jatekos label
        self.one_v_one_current_player_label = ctk.CTkLabel(self.one_v_one_top_frame, text="Soron levo jatekos:", font=("Arial", 24))
        self.one_v_one_current_player_label.pack(side='left', padx=(180,0))

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
        self.one_v_one_player1_total_throws_var_label = ctk.CTkLabel(self.one_v_one_player1_total_throws_stat_frame, text=self.one_v_one_player1_total_throws + self.one_v_one_player1_throw_before_overtime, font=("Arial", 20))
        self.one_v_one_player1_total_throws_var_label.pack(side='left', padx=10)

        # Player1 Total hits statisztika 
        self.one_v_one_player1_total_hits_stat_frame = ctk.CTkFrame(self.one_v_one_player1_frame)
        self.one_v_one_player1_total_hits_stat_frame.pack(pady=0, fill="x")
        self.one_v_one_player1_total_hits_stat_label = ctk.CTkLabel(self.one_v_one_player1_total_hits_stat_frame, text="Total hits:", font=("Arial", 20))
        self.one_v_one_player1_total_hits_stat_label.pack(side='left', padx=10)
        self.one_v_one_player1_total_hits_var_label = ctk.CTkLabel(self.one_v_one_player1_total_hits_stat_frame, text=self.one_v_one_player1_total_hits, font=("Arial", 20))
        self.one_v_one_player1_total_hits_var_label.pack(side='left', padx=10)

        # Player1 Total miss statisztika 
        self.one_v_one_player1_total_miss_stat_frame = ctk.CTkFrame(self.one_v_one_player1_frame)
        self.one_v_one_player1_total_miss_stat_frame.pack(pady=0, fill="x")
        self.one_v_one_player1_total_miss_stat_label = ctk.CTkLabel(self.one_v_one_player1_total_miss_stat_frame, text="Total misses:", font=("Arial", 20))
        self.one_v_one_player1_total_miss_stat_label.pack(side='left', padx=10)
        self.one_v_one_player1_total_miss_var_label = ctk.CTkLabel(self.one_v_one_player1_total_miss_stat_frame, text=self.one_v_one_player1_total_miss, font=("Arial", 20))
        self.one_v_one_player1_total_miss_var_label.pack(side='left', padx=10)

        # Player1 Total percentage statisztika 
        self.one_v_one_player1_total_percentage_stat_frame = ctk.CTkFrame(self.one_v_one_player1_frame)
        self.one_v_one_player1_total_percentage_stat_frame.pack(pady=0, fill="x")
        self.one_v_one_player1_total_percentage_stat_label = ctk.CTkLabel(self.one_v_one_player1_total_percentage_stat_frame, text="Total percentage:", font=("Arial", 20))
        self.one_v_one_player1_total_percentage_stat_label.pack(side='left', padx=10)
        self.one_v_one_player1_total_percentage_var_label = ctk.CTkLabel(self.one_v_one_player1_total_percentage_stat_frame, text=f'{self.calculate_percentage(self.one_v_one_player1_total_hits, self.one_v_one_player1_total_throws + self.one_v_one_player1_throw_before_overtime)}%', font=("Arial", 20))
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
        self.one_v_one_player2_total_throws_var_label = ctk.CTkLabel(self.one_v_one_player2_total_throws_stat_frame, text=self.one_v_one_player2_total_throws + self.one_v_one_player2_throw_before_overtime, font=("Arial", 20))
        self.one_v_one_player2_total_throws_var_label.pack(side='left', padx=10)

        # Player2 Total hits statisztika 
        self.one_v_one_player2_total_hits_stat_frame = ctk.CTkFrame(self.one_v_one_player2_frame)
        self.one_v_one_player2_total_hits_stat_frame.pack(pady=0, fill="x")
        self.one_v_one_player2_total_hits_stat_label = ctk.CTkLabel(self.one_v_one_player2_total_hits_stat_frame, text="Total hits:", font=("Arial", 20))
        self.one_v_one_player2_total_hits_stat_label.pack(side='left', padx=10)
        self.one_v_one_player2_total_hits_var_label = ctk.CTkLabel(self.one_v_one_player2_total_hits_stat_frame, text=self.one_v_one_player2_total_hits, font=("Arial", 20))
        self.one_v_one_player2_total_hits_var_label.pack(side='left', padx=10)

        # Player2 Total miss statisztika 
        self.one_v_one_player2_total_miss_stat_frame = ctk.CTkFrame(self.one_v_one_player2_frame)
        self.one_v_one_player2_total_miss_stat_frame.pack(pady=0, fill="x")
        self.one_v_one_player2_total_miss_stat_label = ctk.CTkLabel(self.one_v_one_player2_total_miss_stat_frame, text="Total misses:", font=("Arial", 20))
        self.one_v_one_player2_total_miss_stat_label.pack(side='left', padx=10)
        self.one_v_one_player2_total_miss_var_label = ctk.CTkLabel(self.one_v_one_player2_total_miss_stat_frame, text=self.one_v_one_player2_total_miss, font=("Arial", 20))
        self.one_v_one_player2_total_miss_var_label.pack(side='left', padx=10)

        # Player2 Total percentage statisztika 
        self.one_v_one_player2_total_percentage_stat_frame = ctk.CTkFrame(self.one_v_one_player2_frame)
        self.one_v_one_player2_total_percentage_stat_frame.pack(pady=0, fill="x")
        self.one_v_one_player2_total_percentage_stat_label = ctk.CTkLabel(self.one_v_one_player2_total_percentage_stat_frame, text="Total percentage:", font=("Arial", 20))
        self.one_v_one_player2_total_percentage_stat_label.pack(side='left', padx=10)
        self.one_v_one_player2_total_percentage_var_label = ctk.CTkLabel(self.one_v_one_player2_total_percentage_stat_frame, text=f'{self.calculate_percentage(self.one_v_one_player2_total_hits, self.one_v_one_player2_total_throws + self.one_v_one_player2_throw_before_overtime)}%', font=("Arial", 20))
        self.one_v_one_player2_total_percentage_var_label.pack(side='left', padx=10)


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
                    self.one_v_one_player1_total_throws_var_label.configure(text=self.one_v_one_player1_total_throws + self.one_v_one_player1_throw_before_overtime)
                    self.one_v_one_player1_total_hits_var_label.configure(text=self.one_v_one_player1_total_hits)
                    self.one_v_one_player1_total_percentage_var_label.configure(text=f'{self.calculate_percentage(self.one_v_one_player1_total_hits, self.one_v_one_player1_total_throws + self.one_v_one_player1_throw_before_overtime)}%')
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
                    self.one_v_one_player1_total_throws_var_label.configure(text=self.one_v_one_player1_total_throws + self.one_v_one_player1_throw_before_overtime)
                    self.one_v_one_player1_total_hits_var_label.configure(text=self.one_v_one_player1_total_hits)
                    self.one_v_one_player1_total_percentage_var_label.configure(text=f'{self.calculate_percentage(self.one_v_one_player1_total_hits, self.one_v_one_player1_total_throws + self.one_v_one_player1_throw_before_overtime)}%')
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
                    self.one_v_one_player1_total_throws_var_label.configure(text=self.one_v_one_player1_total_throws + self.one_v_one_player1_throw_before_overtime)
                    self.one_v_one_player1_total_hits_var_label.configure(text=self.one_v_one_player1_total_hits)
                    self.one_v_one_player1_total_percentage_var_label.configure(text=f'{self.calculate_percentage(self.one_v_one_player1_total_hits, self.one_v_one_player1_total_throws + self.one_v_one_player1_throw_before_overtime)}%')
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
                    self.one_v_one_player2_total_throws_var_label.configure(text=self.one_v_one_player2_total_throws + self.one_v_one_player2_throw_before_overtime)
                    self.one_v_one_player2_total_hits_var_label.configure(text=self.one_v_one_player2_total_hits)
                    self.one_v_one_player2_total_percentage_var_label.configure(text=f'{self.calculate_percentage(self.one_v_one_player2_total_hits, self.one_v_one_player2_total_throws + self.one_v_one_player2_throw_before_overtime)}%')
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
                    self.one_v_one_player2_total_throws_var_label.configure(text=self.one_v_one_player2_total_throws + self.one_v_one_player2_throw_before_overtime)
                    self.one_v_one_player2_total_hits_var_label.configure(text=self.one_v_one_player2_total_hits)
                    self.one_v_one_player2_total_percentage_var_label.configure(text=f'{self.calculate_percentage(self.one_v_one_player2_total_hits, self.one_v_one_player2_total_throws + self.one_v_one_player2_throw_before_overtime)}%')
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
                    self.one_v_one_player2_total_throws_var_label.configure(text=self.one_v_one_player2_total_throws + self.one_v_one_player2_throw_before_overtime)
                    self.one_v_one_player2_total_hits_var_label.configure(text=self.one_v_one_player2_total_hits)
                    self.one_v_one_player2_total_percentage_var_label.configure(text=f'{self.calculate_percentage(self.one_v_one_player2_total_hits, self.one_v_one_player2_total_throws + self.one_v_one_player2_throw_before_overtime)}%')
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
                    self.one_v_one_player1_total_throws_var_label.configure(text=self.one_v_one_player1_total_throws + self.one_v_one_player1_throw_before_overtime)
                    self.one_v_one_player1_total_miss_var_label.configure(text=self.one_v_one_player1_total_miss)
                    self.one_v_one_player1_total_percentage_var_label.configure(text=f'{self.calculate_percentage(self.one_v_one_player1_total_hits, self.one_v_one_player1_total_throws + self.one_v_one_player1_throw_before_overtime)}%')

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
                    self.one_v_one_player1_total_throws_var_label.configure(text=self.one_v_one_player1_total_throws + self.one_v_one_player1_throw_before_overtime)
                    self.one_v_one_player1_total_miss_var_label.configure(text=self.one_v_one_player1_total_miss)
                    self.one_v_one_player1_total_percentage_var_label.configure(text=f'{self.calculate_percentage(self.one_v_one_player1_total_hits, self.one_v_one_player1_total_throws + self.one_v_one_player1_throw_before_overtime)}%')

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
                    self.one_v_one_player2_total_throws_var_label.configure(text=self.one_v_one_player2_total_throws + self.one_v_one_player2_throw_before_overtime)
                    self.one_v_one_player2_total_miss_var_label.configure(text=self.one_v_one_player2_total_miss)
                    self.one_v_one_player2_total_percentage_var_label.configure(text=f'{self.calculate_percentage(self.one_v_one_player2_total_hits, self.one_v_one_player2_total_throws +  self.one_v_one_player2_throw_before_overtime)}%')

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
                    self.one_v_one_player2_total_throws_var_label.configure(text=self.one_v_one_player2_total_throws + self.one_v_one_player2_throw_before_overtime)
                    self.one_v_one_player2_total_miss_var_label.configure(text=self.one_v_one_player2_total_miss)
                    self.one_v_one_player2_total_percentage_var_label.configure(text=f'{self.calculate_percentage(self.one_v_one_player2_total_hits, self.one_v_one_player2_total_throws +  self.one_v_one_player2_throw_before_overtime)}%')

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
        self.one_v_one_change_check_active_player() # Aktiv jatekos nevenek ellenorzese
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
        self.one_v_one_player1_throw_before_overtime = self.one_v_one_player1_total_throws
        self.one_v_one_player2_throw_before_overtime = self.one_v_one_player2_total_throws
        self.one_v_one_player1_total_throws = 0
        self.one_v_one_player2_total_throws = 0
        self.one_v_one_player1_double_before_overtime = self.one_v_one_player1_doubles
        self.one_v_one_player2_double_before_overtime = self.one_v_one_player2_doubles
        self.one_v_one_player1_doubles = 0
        self.one_v_one_player2_doubles = 0
        self.one_v_one_player1_throws_without_miss = 0
        self.one_v_one_player2_throws_without_miss = 0
        self.one_v_one_overtime_first_throw = False

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
        player1_hits = self.one_v_one_player1_total_hits
        player2_hits = self.one_v_one_player2_total_hits
        player1_miss = self.one_v_one_player1_total_miss
        player2_miss = self.one_v_one_player2_total_miss
        player1_total_throw = self.one_v_one_player1_total_throws + self.one_v_one_player1_throw_before_overtime
        player2_total_throw = self.one_v_one_player2_total_throws + self.one_v_one_player2_throw_before_overtime
        player1_doubles = self.one_v_one_player1_doubles + self.one_v_one_player1_double_before_overtime
        player2_doubles = self.one_v_one_player2_doubles + self.one_v_one_player2_double_before_overtime

        # Ujrageneraljuk a tracker ablakot (Fontos, hogy az adatokat keresztbe adjuk at, aki itt p1 volt, az uj jatek p2 lesz! Ez a kezdojatekos csereje miatt fontos!)
        self.one_v_one_tracker_window(
            starting_player=player2,
            other_player=player1,
            p1thits=player2_hits,
            p2thits=player1_hits,
            p1tmiss=player2_miss,
            p2tmiss=player1_miss,
            p1tbot=player2_total_throw,
            p2tbot=player1_total_throw,
            p1dbot=player2_doubles,
            p2dbot=player1_doubles
            )


            

    # 2v2 Jatekablak
    def two_v_two_tracker_window(self):
        print('2v2')

    
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
        self.cursor.execute("SELECT name FROM players")
        players = self.cursor.fetchall()
        players_list = []
        for player in players:
            players_list.append(player[0])
        
        return players_list




app = MainWindow()
app.mainloop()