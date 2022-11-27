from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.core.window import Window
Window.size = (1080,2400)

# Klasse für Popup window bei Fehlern
class Poppy:
    # Funktion für Popup window die zwischen Label und Button entscheidet, außerdem noch den Titel und den Text nimmt

    def popup(self,cont,titel,label_text):
        self.content = None
        if cont == 1:  # wenn der Content = 1, dann wird Label angezeigt
            self.content = Label(text=label_text)
        if cont == 2:  # wenn der Content = 2, dann wird der Button angezeigt
            self.content = Button(text = label_text,
                             size_hint=(0.3,0.2),
                             pos_hint={"top":0.5,"right":0.5},
                             #on_release = self.button_dismiss(),
                             background_color=[200 / 255., 200 / 255., 200 / 255., 1],
                             color=[1 / 255., 1 / 255., 1 / 255., 1],
                             font_size=40)

        # das ist das Kivy Widget für das Popup
        self.pop = Popup(title= titel,
                    content=self.content,
                    title_size=64,
                    background_color=[1 / 255., 18 / 255., 172 / 255., 0.52],
                    size_hint=(0.8, 0.5))
        self.pop.open()

    def button_dismiss(self,*args):
        self.pop.dismiss()


popp = Poppy()  # hier wird eine Instanz der Klasse erzeugt um sie in anderen Klassen aufrufen zu können

# Klasse für den Home Screen mit den drei Buttons die jeweils auf die verschiedenen Nutzer führen (später dynamische und generelle Nutzer)


class Home(Screen):

    # Funktion um die Screens zu wechseln, wenn man aud Personenbutton drückt
    def switchScreen(self, name):
        sm.current = "score1"
        sm.get_screen("score1").ids.spiel.text = name

    def names(self):
        self.n = self.ids.marian.text

# dynamischer Score Screen wo das meiste sich abspielt


class Score1(Screen):

    # startet den timer, der alle 2 Sekunden überpfüt ob der Button deaktiviert werden soll -> um fehler von user zu verhindern
    def on_start(self):
        if sm.current == "score1":
            self.function_interval = Clock.schedule_interval(self.check_regularly, 3)

    def check_regularly(self,*args):
        self.calc_total()
        self.calc_round()
        #self.check_disable()

    def calc_total(self,*args):
        self.filename = "{}.txt".format(self.ids.spiel.text)
        self.sum = 0
        self.add = False
        self.file = open(self.filename,"r")
        for index in self.file.read():
            if index.isnumeric():
                self.sum += int(index)
        self.sum_total = self.sum - 51
        self.ids.total.text = str(self.sum_total)
        self.file.close()

    def calc_round(self,*args):
        if self.ids.spinner_id.text != "Runde Auswählen":

            self.filename = "{}.txt".format(self.ids.spiel.text)
            self.sum_round = 0
            self.current_round = int(self.ids.spinner_id.text[6:])
            self.file = open(self.filename,"r")
            self.content_read = str(self.file.read())
            self.round_format = "{})".format(self.current_round)
            self.i = self.content_read.find(self.round_format)

            if self.current_round >= 10:
                for num in self.content_read[self.i + 3:]:
                    if num == "(":
                        break
                    if num.isnumeric():
                        self.sum_round += int(num)
            else:
                for num in self.content_read[self.i + 2:]:
                    if num == "(":
                        break
                    if num.isnumeric():
                        self.sum_round += int(num)


            self.ids.this_round.text = str(self.sum_round)
            self.file.close()

    def check_disable(self, *args):
        if self.ids.one.text != "" and self.ids.two.text != "" and self.ids.three.text != "" and self.ids.four.text != "" and self.ids.five.text != "" and self.ids.six.text != "":
            self.ids.confirm.disabled = True
        else:
            self.ids.confirm.disabled = False

    def stop_timer(self, *args):
        try:
            self.function_interval.cancel()
        except:
            pass

    def back(self):
        sm.current = "home"


    def spinner_clicked(self, value):
        pass

    def delete(self):
        self.filename = "{}.txt".format(self.ids.spiel.text)
        self.file = open(self.filename,"w")
        #popp.popup(2, "LÖSCHEN?", "Ja")
        self.file.write("(01)(02)(03)(04)(05)(06)(07)(08)(09)(10)(11)(12)")
        self.file.close()

    def add_value(self):
        self.filename = "{}.txt".format(self.ids.spiel.text)
        self.file = open(self.filename)

        if self.ids.one.text == "" or self.ids.two.text == "" or self.ids.three.text == "" or self.ids.four.text == "" or self.ids.five.text == "" or self.ids.six.text == "":
            popp.popup(1, "FEHLER", "Nicht alle Felder sind richtig ausgefüllt worden")
        elif self.ids.spinner_id.text == "Runde Auswählen":
            popp.popup(1, "FEHLER", "Es wurde keine Runde ausgewählt")
        else:
            self.read_content = self.file.read()

            for i in range(1,13):
                if self.ids.spinner_id.text == "Runde {}".format(i):
                    if i <= 9:
                        self.index = self.read_content.find("(0{})".format(i))
                    else:
                        self.index = self.read_content.find("({})".format(i))

                    self.new_content = self.read_content[0:self.index+4] + "{},{},{},{},{},{}".format(self.ids.one.text,
                                                                                                    self.ids.two.text,
                                                                                                    self.ids.three.text,
                                                                                                    self.ids.four.text,
                                                                                                    self.ids.five.text,
                                                                                                    self.ids.six.text) + self.read_content[self.index + 4:]

            self.file = open(self.filename,"w")
            self.file.write(self.new_content)
            self.file.close()


s1 = Score1()


class ArcheryApp(App):
    def build(self):
        return sm

    icon = "pictures/icon.png"


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("kivy.kv")

sm = WindowManager()

screens = [Home(name="home"), Score1(name="score1")]

for screen in screens:
    sm.add_widget(screen)

sm.current = "home"

if __name__ == '__main__':
    ArcheryApp().run()
