import os.path
import sys

from Controller import Controller
class App:
    def __init__(self, db):  # Ehk kui seda objekti app'i looma hakatakse, siis juba siis saadakse andmebaasi nimi
        Controller(db).main()  # Ehk kui objekt Controller luuakse, siis andtakse talle kaasa argument andmebaasi -
        # nimi. (controlleri konstruktoris oli db_name = False). Kui see objekt ära on loodud, siis kutsutakse sealt
        # välja meetod main, mida seal hetkel veel ei ole. Seepärast see on õrnalt kollase taustaga hetkel
if __name__ == '__main__':  # Et App'i luua, tehakse if lause
    db_name = None  # Ehk siis algselt andmebaasi nime ei ole
    if len(sys.argv) == 2:  # Tuleb kontrollida, kas käsureal on kaks argumenti
        if os.path.exists(sys.argv[1]):  # Tuleb kontrollida argumenti. Argument indeksiga 1, kas see on olemas
            db_name = sys.argv[1]
    App(db_name)    # Sõltumata sellest if lausest on vaja luua App
# Kui me rakenduse käivitame, tuleb siia if lause juurde, öeldakse, et db_name on None, kontrollitakse kas käsurea peal
# on kaks argumenti. Üks on faili nimi, mis on alati olemas ja teine on see, mis me ise kirjutame ehk andmebaasi nimi.
# Kui see vastab tõele, et andmebaasi nimi on seal olemas, siis kontrollitakse, kas see andmebaas on reaalselt olemas.
# Kui see vastab tõele, et fail on olemas, siis db_name on see, mis käsurea pealt on kaasa antud.
# Sõltumata siis sellest if lausest luuakse App kas db_name = None või db_name see, mis käsurea pealt saadaakse
# Selle Appi loomise tulemusena tullakse App'i konstruktorisse, argument on kaasas,
# controller luuakse sellesama andmebaasi nimega ja peale loomist käivitatakse main
