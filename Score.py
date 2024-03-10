class Score:

    def __init__(self, name, word, missing, seconds, time):
        # missing- tähed, mis on valesti sisestatud; aeg sekundites;
        # time- reaalne aeg, millal mängiti ehk millal saadi edetabelisse;
        # kõikidele muutujatele self variandid teha
        # Kaasa antud väärtus kirjutatakse klassi siseseks väärtuseks, selleks et klassi sees saaks muutujaiod kasutada
        self.__name = name
        self.__word = word
        self.__missing = missing
        self.__seconds = seconds
        self.__time = time

    # Kõikidele on vaja teha getter
    # defid peavad olema kõik ühe joone peal
    # klassi nimi on suure tähega, muutujate ja meetodite nimed väikesega
    @property
    def name(self):
        return self.__name

    @property
    def word(self):
        return self.__word

    @property
    def missing(self):
        return self.__missing

    @property
    def seconds(self):
        return self.__seconds

    @property
    def time(self):
        return self.__time
    # Loome objekti, lisame sinna need 5 asja, mida tahame kätte saada muutmata kujul ehk pole vaja settereid
    # Sellepärast on meil getterid, et saada info kätte
    # Muuta saab just algandmeid
    # Praegusel hetkel ei muuda. Lihtsalt loeme andmebaasist, kirjutame ta listi objektina ja siis näidatakse edetabelis