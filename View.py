from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter.font as font
from datetime import datetime
import time
from PIL import ImageTk, Image  # pip install Pillow
class View(Tk):
    def __init__(self, controller, model):  # Kui vaade luuakse, siis kontrollerile peab olema ligipääs
        # Sulgudes on muutujate nimed
        super().__init__()  # Selleks, et View fail meil põhiaknana toimiks, tuleb kirjutada see super..., mainwindowina
        self.__controller = controller  # Vaja muuta need klassisiseselt kättesaadavaks teha
        self.__model = model

        # Kirjastiilid
        self.__big_font = font.Font(family="Courier", size=20, weight="bold")    # Alumise ekraanipoole kirjastiil
        self.__default = font.Font(family="Verdana", size=12)   # Ülemise ekraanipoole oma Verdana
        self.__default_bold = font.Font(family="Verdana", size=12, weight='bold')
        # Courier on pildil kollane osa, default ülemine osa. Aeg ei ole rasvane ega nupudega ega ka sisestuskast ei ole

        # Põhiakna Parameetrid
        self.__width = 555
        self.__height = 200
        self.title("Poomismäng")
        self.center(self, self.__width, self.__height)
        # Keskele joondamine- self- millist akent joondada ja mis on selle akna mõõdud. kolm argumenti

        # Loome kolm frame-t
        self.__frame_top, self.__frame_bottom, self.__frame_image = self.create_frames()
        # alt + enterit kasutades
        # kolm muutujat saavad sellest väärtuse
        # Loome kolm lokaalset frame'i
        # Erinevaid objekte on vaja panna.
        # On vaja ligi pääseda kogu klassi ulatuses sellele frame'ile. Sõltumata sellest, millises meetodis me oleme
        # Frame'i loomisel tulemusel pannakse need põhiaknale packiga, üks gridiga.

        # Loome "neli" nuppu
        self.__btn_new, self.__btn_cancel, self.__btn_send = self.create_buttons()  # Muutujaid kolm, kuid neljas?
        # Neljas nupp on edetabeli nupp. Edetabeli nupp ei muutu mitte kunagi. Loome, paneme ja sinna jääb
        # Create buttons klassi meetod- below

        # Pilt
        self.__image = ImageTk.PhotoImage(Image.open(self.__model.image_files[len(self.__model.image_files) - 1]))
        self.__lbl_image = None
        # Võtab pildid, loeb kõige viimase faili. Hangmani kujutise tekitamine

        # Loome "neli" silti (label)
        # Tegelikult isegi 5 labelit- error vigased tähed, time on jooksev aeg, result on ekraani alumine aken
        self.__lbl_error, self.__lbl_time, self.__lbl_result, self.__lbl_word = self.create_labels()
        # Loome sisestus kasti(näide kuidas veel teha)
        self.__char_input = Entry(self.__frame_top, justify="center", font=self.__default)
        self.__char_input['state'] = 'disabled'
        self.__char_input.grid(row=1, column=1, padx=5, pady=2, sticky=EW)
        # Enter klahvi funktionaalsus
        self.bind('<Return>', lambda event: self.__controller.btn_send_click())

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        if messagebox.askokcancel("Väljumine", "Kas soovid mängust väljuda?"):
            self.destroy()
    # Kõik muutujatele oleks tarvis getterid

    @property
    def btn_new(self):
        return self.__btn_new

    @property
    def btn_cancel(self):
        return self.__btn_cancel

    @property
    def btn_send(self):
        return self.__btn_send

    @property
    def char_input(self):
        return self.__char_input

    @property
    def lbl_time(self):
        return self.__lbl_time

    @property
    def lbl_result(self):
        return self.__lbl_result

    @property
    def lbl_error(self):
        return self.__lbl_error

    def main(self):
        self.mainloop()

    @staticmethod
    def center(win, w, h):
        x = int((win.winfo_screenwidth() / 2) - (w / 2))    # Tulemus täisarvuna
        y = int((win.winfo_screenheight() / 2) - (h / 2))   # # Tulemus täisarvuna
        win.geometry(f"{w}x{h}+{x}+{y}")
    # Funktsiooni mõte: tuvastada kui lai on ekraan
    # Arvutuse tulemusel ekraan jagatakse kaheks ja see ekraan, mida on tarvis, see jagataks eka kaheks.
    # Algsest numbrist lahutatakse teine, saadakse x koordinaat ja y vertikaalis tehakse samamoodi.
    # Saadakse ülemine vasakpoolne nurk ja vastavalt akna suurusele joonistatakse see aken. Tuleb täpselt keskele

    def create_frames(self):
        top = Frame(self, height=50)    # Ülemine frame 50 ühikut kõrgust, self pannakse  view peale ehk iseenda peale
        bottom = Frame(self)    # Kõrgust ei määra
        image = Frame(top, height=130, width=130, bg='white')   # Frame ei lähe selfi peale vaid topi peale.
        # 130x130 on pildi mõõt pluss vb natukene ka varu
        # Kolm objekti tuleb nüüd panna ka põhiakna peale
        # Sisestuskasti tegime valget värvi. Algul on vasakul üleval. Peale labelite ja buttonite lisamist aga paremal
        top.pack(fill=BOTH)
        bottom.pack(expand=TRUE, fill=BOTH)
        # Kui neid mitte panna, siis ei ülemist ega alumist frame-i ei teki/näe
        image.grid(row=0, column=3, rowspan=4, padx=5, pady=5)
        # topi peale pandavad on kõik grid'i pea. Kuna image on ka topi peal, siis ka gridi peal
        # Kõik labelid ja nupud ka gridi peale kuna ned on top'i peal

        return top, bottom, image

    def create_buttons(self):
        new = Button(self.__frame_top, text="Uus mäng", font=self.__default, command=self.__controller.btn_new_click)
        cancel = Button(self.__frame_top, text="Loobu", font=self.__default, command=self.__controller.btn_cancel_click,
                        state=DISABLED)  # Commandi kohe ei pane, hiljem
        send = Button(self.__frame_top, text="Saada", font=self.__default,
                      command=self.__controller.btn_send_click, state=DISABLED)
        # Need on need kolm nuppu, mille omadusi tahame mängu jooksul muuta
        (Button(self.__frame_top, text='Edetabel', font=self.__default, command=self.__controller.btn_scoreboard_click).
         grid(row=0, column=1, padx=5, pady=2, sticky=EW))  # sticky=EW- Nii laiaks kui on võimalik selles veerus
        # Nuppude asukohtade määramine
        new.grid(row=0, column=0, padx=5, pady=2, sticky=EW)
        cancel.grid(row=0, column=2, padx=5, pady=2, sticky=EW)
        send.grid(row=1, column=2, padx=5, pady=2, sticky=EW)
        return new, cancel, send
        # return new, cancel, send- Tagastab need kolm asja, õiges järjekorras tuleb kirjutada nagu on-
        # üleval kui sai init all loodud create_buttons klass

    def create_labels(self):
        # Entry label ei muutu kunagi
        Label(self.__frame_top, text='Sisesta täht', anchor='w',
              font=self.__default_bold).grid(row=1, column=0, padx=5, pady=2, sticky=EW)
        # Me loome objekti ja kohe paneme ta Frame'i peale. Ei tee eraldi rida gridi jaoks vaid kaks ühes.
        # Ei saa seda aga teha ei klickitavaks ega muid omadusi ei saa muuta

        # Kolm järgnevat labeli
        error = Label(self.__frame_top, text='Vigased tähed', anchor='w', font=self.__default_bold, fg='red')
        lbl_time = Label(self.__frame_top, text='00:00:00', font=self.__default)
        result = Label(self.__frame_bottom, text='Mängime?'.upper(), font=self.__big_font)
        word = Label(self.__frame_bottom, text='___'.upper(), font=self.__big_font)

        # Hääl kadus pausilt tulles, et ei enam kuulata, vaid lihtsalt vaadata tummfilmi ja kirjutada ülesse.
        error.grid(row=2, column=0, columnspan=3, padx=5, pady=2, sticky=EW)
        lbl_time.grid(row=3, column=0, columnspan=3, padx=5, pady=2, sticky=EW)
        result.pack(padx=5, pady=2)
        word.pack(padx=5, pady=3)

        # Pildi paigutamine
        self.__lbl_image = Label(self.__frame_image, image=self.__image)
        self.__lbl_image.pack()

        return error, lbl_time, result, word

    def create_scoreboard_window(self):
        top = Toplevel(self)
        top.title('Edetabel')
        top_w = 500
        top_h = 180
        top.resizable(False, False)
        top.grab_set()
        top.focus()

        frame = Frame(top)
        frame.pack(fill=BOTH, expand=TRUE)
        self.center(top, top_w, top_h)

        return frame

    def change_image(self, image_id):   #
        self.__image = ImageTk.PhotoImage(Image.open(self.__model.image_files[image_id]))   # Määrame uue pildi
        # Süsteemi Image on suure tähega, meie oma väikese i tähega. Listist, mis pilti tahame. Kokku 12 pilti
        self.__lbl_image.configure(image=self.__image)  #
        self.__lbl_image.image = self.__image

    def display_word(self, word):
        self.__lbl_word.config(text=word)


def show_message(result):
    if result == "won":
        messagebox.showinfo("Võitsid!", f'Palju õnne, arvasid sõna ära!')
    if result == "lose":
        messagebox.showinfo("Kaotasid!", "Kaotasid, kas mängime veel?")


def draw_scoreboard(frame, data):  # Need kaks asja saame sellestsamastt kontrolleri klickist kätte
    if len(data) > 0:
        # Tabeli vaade
        my_table = ttk.Treeview(frame)  # Lisaks tabelile on võimalik sinna ka faili struktuuri joonistada

        # Vertikaalne kerimisriba- vertical scroll bar
        vsb = ttk.Scrollbar(frame, orient=VERTICAL, command=my_table.yview)
        vsb.pack(side=RIGHT, fill=Y)    # Täitmine ülevalt alla ehk y telg, paremal scrollbar
        my_table.configure(yscrollcommand=vsb.set)

        # Veergude id
        my_table['columns'] = ('name', 'word', 'missing', 'seconds', 'date_time')

        # Veergude seaded
        my_table.column('#0', width=0, stretch=NO)
        my_table.column('name', anchor=W, width=100)
        my_table.column('word', anchor=W, width=100)
        my_table.column('missing', anchor=W, width=100)
        my_table.column('seconds', anchor=W, width=50)
        my_table.column('date_time', anchor=W, width=100)

        # Tabeli päis(nähtav)- kõik päise veeru nimed on keskel
        my_table.heading('#0', text='', anchor=CENTER)
        my_table.heading('name', text='Nimi', anchor=CENTER)
        my_table.heading('word', text='Sõna', anchor=CENTER)
        my_table.heading('missing', text='Valed tähed', anchor=CENTER)
        my_table.heading('seconds', text='Kestvus', anchor=CENTER)
        my_table.heading('date_time', text='Mängitud', anchor=CENTER)

        # Lisa info tabelisse(visuaal)
        x = 0
        for p in data:  # score struktuur. Päev-kuu-aasta on vaja teha. Muudab aasta-kuu-päeva ära, nii nagu varem
            dt = datetime.strptime(p.time, '%Y-%m-%d %H:%M:%S').strftime('%d.%m.%Y %T')
            sec = time.strftime('%T', time.gmtime(p.seconds))
            time.strftime('%T', time.gmtime(p.seconds))
            my_table.insert(parent='', index='end', iid=str(x), text='',
                            values=(p.name, p.word, p.missing, sec, dt))
            x += 1

        my_table.pack(expand=TRUE, fill=BOTH)
