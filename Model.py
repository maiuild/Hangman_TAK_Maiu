import glob
import sqlite3
import datetime
from Score import Score


class Model:
    def __init__(self):
        self.__database = 'databases/hangman_words_ee.db'  # Andmebaas
        # Käsureale pip install Pillow. Vaja selleks , et saaks piltidega graafilise kasutaja liideses toimetada
        # pip on pyhtoni enda rakendus tarkvara installimiseks/eemaldamiseks
        # Pillow moodulit originaalis ei ole, seetõttu vaja pip'i abil eraldi installida
        # python.exe -m pip install --upgrade pip
        self.__image_files = glob.glob('images/*.png')  # List mängu piltidega.
        # Käsklus võttis kõik png laiendiga failid õiges järjekorras ja kirjutas listi õiges järjekorras
        # TODO juhuslik sõna
        # TODO kõik sisestatud tähed (list)
        #  TODO vigade lugeja (s.h. pildi id)
        #  TODO kasutaja leitud tähed (visuaal muidu on seal allkriips _)
        self.__random_word = ''
        self.__typed_letters = []
        self.__wrong_letters = []
        self.__wrong_guesses = 0
        self.__user_found_letters = []
        self.__hidden_word = ""

    @property
    def database(self):
        return self.__database

    @property
    def image_files(self):
        return self.__image_files

    @property
    def random_word(self):
        return self.__random_word

    @property
    def typed_letters(self):
        return self.__typed_letters

    @property
    def wrong_letters(self):
        return self.__wrong_letters

    @property
    def wrong_guesses(self):
        return self.__wrong_guesses

    @property
    def user_found_letters(self):
        return self.__user_found_letters

    @property
    def hidden_word(self):
        return self.__hidden_word

    @database.setter
    def database(self, value):
        self.__database = value

    def read_scores_data(self):     # Loeb andmebaasi tabelist edetabeli kõik kirjed. Tuleb teha andmebaasi ühendus
        # Return tagastab andmed, mida küsime.
        connection = None
        try:
            connection = sqlite3.connect(self.__database)
            sql = 'SELECT * FROM scores ORDER BY seconds;'
            # Kui saadaks data mujale, nt controllerisse, siis ei oleks midagi selle dataga peale hakata kuna-
            # kontroller ei saa sellest datast midagi aru. Sest kuna see on andmebaasi info,
            # siis ta hoiab seda andmebaasi infot niikaua kui andmebaasi ühendus on püsti.
            # Seepõast on vaja panna andmed listi. Tuleb kõigepealt tekitada tühi list,
            # kirjutada data listi ja saata list vajalikku kohta
            cursor = connection.execute(sql)
            data = cursor.fetchall()
            result = []
            for row in data:
                result.append(Score(row[1], row[2], row[3], row[4], row[5]))  # Score'i lahti võttes näha mitu on vaja
            # Row 0 jääb välja, sest see on ID kuna me võtsime kogu info
            return result
        except sqlite3.Error as error:
            print(f'Viga ühenduda andmebaasi {self.__database}: {error}')

        finally:
            if connection:
                connection.close()

    # Ülesanded on blokkidena. Iga plokk on üks meetod.

    #  TODO Seadistab uue sõna äraarvamiseks
    #  TODO Seadistab mõningate muutujate algväärtused (vaata ___init__ kolme viimast .
    #  TODO Neljas muutuja on eelmine rida)
    #  TODO Seadistab ühe muutuja nii et iga tähe asemel paneb allkiriipsu mida näidata aknas äraarvatavas sõnas (LIST)
    def setup_new_game(self):   # Meetod, mis seadistab uue mängu
        self.__random_word = self.get_random_word()
        print(self.random_word)
        self.__hidden_word = len(self.random_word) * '-'
        self.__typed_letters = []
        self.__wrong_letters = []
        self.__wrong_guesses = 0
        self.__user_found_letters = ['_' for _ in range(len(self.random_word))]

    #  TODO Meetod mis seadistab juhusliku sõna muutujasse
    #  TODO Teeb andmebaasi ühenduse ja pärib sealt ühe juhusliku sõna ning kirjutab selle muutujasse
    def get_random_word(self):  # Meetod mis seadistab juhusliku sõna muutujasse
        connection = None
        try:  # Teeb andmebaasi ühenduse ja pärib sealt ühe juhusliku sõna ning kirjutab selle muutujasse
            connection = sqlite3.connect(self.__database)
            cursor = connection.cursor()
            cursor.execute('SELECT word FROM words ORDER BY RANDOM() LIMIT 1;')
            random_word = cursor.fetchone()[0]
            return random_word.lower()
        except sqlite3.Error as error:
            print(f'Andmebaasiga ühendumise viga: {error}')
            return ''
        finally:
            if connection:
                connection.close()

    #  TODO kasutaja siestuse kontroll (Vaata COntrolleris btn_send_click esimest )
    #  TODO Kui on midagi sisestatud võta sisestusest esimene märk
    #  TODO (me saame sisestada pika teksti aga esimene täht on oluline!)
    #  TODO Kui täht on otsitavas sõnas, siis asneda tulemuses allkriips õige tähega.
    #  TODO kui tähte polnud, siis vigade arv kasvab +1 ning lisa vigane täht eraldi listi
    def process_user_input(self, user_input):
        if user_input:
            letter = user_input[0].lower()
            if letter in self.__typed_letters:
                self.__wrong_guesses += 1
                self.__wrong_letters.append(letter)
            self.__typed_letters.append(letter)
            if letter in self.random_word:
                for i, char in enumerate(self.random_word):
                    if char == letter:
                        self.__user_found_letters[i] = letter
                new_hidden_word = ""
                for i, char1 in enumerate(self.random_word):
                    if char1 == letter:
                        new_hidden_word += letter
                    elif self.hidden_word[i] != '-':
                        new_hidden_word += self.hidden_word[i]
                    else:
                        new_hidden_word += '-'
                self.__hidden_word = new_hidden_word
                print(self.hidden_word)
            else:
                self.__wrong_guesses += 1
                self.__wrong_letters.append(letter)

    #  TODO Meetod mis tagastab vigaste tähtede listi asemel tulemuse stringina. ['A', 'B', 'C'] => A, B, C
    def list_to_string(self):
        return ', '.join(self.__wrong_letters)

    #  TODO Meetod mis lisab mängija ja tema aja andmebaasi (Vaata Controlleris viimast  rida)
    #  TODO Võtab hetke/jooksva aja kujul AAAA-KK-PP TT:MM:SS (Y-m-d H:M:S)
    #  TODO Kui kasutaja sisestas nime, siis eemalda algusest ja lõpust tühikud
    #  TODO Tee andmebaasi ühendus ja lisa kirje tabelisse scores. Salvesta andmed tabelis ja sulge ühendus.
    def add_player_score(self, player_name, time_counter):
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        player_name = player_name.strip()
        connection = None
        try:
            connection = sqlite3.connect(self.__database)
            cursor = connection.cursor()
            cursor.execute(
                'INSERT INTO scores (name, word, missing, seconds, date_time) VALUES (?, ?, ?, ?, ?);',
                (player_name, self.random_word, self.list_to_string().upper(),
                 time_counter, current_time))
            connection.commit()
        except sqlite3.Error as error:
            print(f'Viga andmebaasiga {self.__database} ühendamisel: {error}')
        finally:
            if connection:
                connection.close()
