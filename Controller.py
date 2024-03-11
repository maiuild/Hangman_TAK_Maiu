from GameTime import GameTime
from Model import Model
from View import View, draw_scoreboard, show_message
from tkinter import simpledialog


class Controller:
    def __init__(self, db_name=None):
        # Kontrollerisse tuleb kaasa ka andmebaasi nimi. Kasutatakse sisemist andmebaasi
        # Kui seal None asemel oleks andmebaasi nimi, kasutaks see seda
        self.__model = Model()  # Model tuleb importida, peavad olema sulud. Sama mis kasutatakse Views nagu ka Controll
        self.__view = View(self, self.__model)  # Luuakse ka View, peab olema kaasa antud kontroller ja Mudel, View imp
        if db_name is not None:     # Kui andmebaasi nimi on olemas
            self.__model.database = db_name
        self.__game_time = GameTime(self.__view.lbl_time)   # Kommentaar eest ära

    def main(self):
        self.__view.main()

    def btn_scoreboard_click(self):
        window = self.__view.create_scoreboard_window()
        data = self.__model.read_scores_data()  # Tagastab resulti, result kirjutatakse muutujasse data
        draw_scoreboard(window, data)

    def buttons_no_game(self):  # pakub juba kui on juurdepääs olemas
        self.__view.btn_new['state'] = 'normal'
        self.__view.btn_cancel['state'] = 'disabled'
        self.__view.btn_send['state'] = 'disabled'
        self.__view.char_input.delete(0, 'end')   # Sisestuskasti peab tühjaks tegema. 'end' vaja kirjutada, END ei sobi
        self.__view.char_input['state'] = 'disabled'    # Peale inputi ei saa ise lisada. Õiges järjekorras kirjutada!

    def buttons_to_game(self):  # Uue nupu vajutusel. Eelnevast teha koopia ja kõik vastupidiselt tõsta. Normal-disable
        self.__view.btn_new['state'] = 'disabled'
        self.__view.btn_cancel['state'] = 'normal'
        self.__view.btn_send['state'] = 'normal'
        self.__view.char_input['state'] = 'normal'
        self.__view.char_input.focus()  # Autofookus sisestuskastile

    def btn_new_click(self):   # Uus mäng
        self.buttons_to_game()
        # Muuda pilti id-ga 0
        self.__view.change_image(0)     # id on null. Modelis __init__'s on juba tehtud png laiendiga piltidest list
        self.__model.setup_new_game()
        self.__view.lbl_result.config(text=self.__model.hidden_word)
        self.__view.lbl_error.config(text='Vigased tähed:', fg='red')
        self.__game_time.reset()
        self.__game_time.start()

    def btn_cancel_click(self):
        self.__game_time.stop()     # Peab aja seisma jätma
        self.__view.change_image(-1)    # See variant sobib pythonis ainult
        # Alati töötav variant- self.__view.change_image(len(self.__model.image_files)-1)
        self.buttons_no_game()
        self.__view.lbl_result.config(text='MÄNGIME?')

    def btn_send_click(self):
        # TODO Loe sisestus kastist saadud info ja suuna mudelisse infot töötlema
        # TODO Muuda teksti tulemus aknas (äraarvatav sõna)
        # TODO Muuda teksti Vigased tähed
        # TODO Tühjanda sisestus kast (ISESESIVALT TUNNIS KOHE)
        # TODO KUI on vigu tekkinud, muuda alati vigade tekst punaseks ning näita vastavalt vea numbrile õiget pilti
        # TODO on mäng läbi. MEETOD siin samas klassis.

        if self.__model.wrong_guesses == 11:
            self.btn_cancel_click()
            show_message('lose')    # View all on show_message
            return
        self.__model.process_user_input(self.__view.char_input.get())
        self.__view.lbl_result.config(text=self.__model.hidden_word.upper())
        vigased = "Vigased tähed: " + self.__model.list_to_string().upper()
        self.__view.lbl_error.config(text=vigased, fg="red")
        self.__view.char_input.delete(0, 'end')
        self.__view.change_image(self.__model.wrong_guesses)
        self.game_over()

    # TODO JAH puhul peata mänguaeg
    # TODO Seadista nupud õigeks (meetod juba siin klassis olemas)
    # TODO Küsi mängija nime (simpledialog.askstring)
    # TODO Saada sisestatud mängija nimi ja mängu aeg sekundites mudelisse
    # TODO Saada sisestatud mängija nimi ja mängu aeg sekundites mudelisse
    # TODO kus toimub kogu muu tegevus kasutajanimega
    def game_over(self):
        if self.__model.hidden_word == self.__model.random_word:
            self.btn_cancel_click()
            show_message('won')     # # View all on show_message
            player_name = simpledialog.askstring("Mäng läbi!:", "Sisesta oma nimi:")
            if player_name:
                self.__model.add_player_score(player_name, self.__game_time.counter)
                return
