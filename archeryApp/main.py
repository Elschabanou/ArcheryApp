from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.properties import ObjectProperty
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
import fileinput
from kivy.uix.popup import Popup


from kivy.core.window import Window
Window.size = (1080,2400)

class Poppy:

    def popup(self,cont,titel,label_text):
        content = None
        if cont == 1:
            content = Label(text=label_text)
        if cont == 2:
            content = Button(text = label_text,
                             size_hint=(0.3,0.2),
                             pos_hint={"top":0.5,"right":0.5},
                             background_color=[200 / 255., 200 / 255., 200 / 255., 1],
                             color=[1 / 255., 1 / 255., 1 / 255., 1],
                             font_size=40)

        pop = Popup(title= titel,
                    content=content,
                    title_size=64,
                    background_color=[1 / 255., 18 / 255., 172 / 255., 0.52],
                    size_hint=(0.8, 0.5))
        pop.open()

popp = Poppy()


class Home(Screen):

    def switchScreen(self,name):
        sm.current = "score1"
        sm.get_screen("score1").ids.spiel.text = name


    def names(self):
        self.n = self.ids.marian.text

class Score1(Screen):


    def back(self):
        sm.current = "home"
    def spinner_clicked(self, value):
        pass

    def delete(self):
        self.file = open("marian.txt","w")
        popp.popup(2,"LÖSCHEN?","Ja")
        self.file.write("")
        self.file.close()

    def add_value(self):

        self.filename = "marian.txt"
        self.file = open(self.filename)

        if self.ids.one.text == "" or self.ids.two.text == "" or self.ids.three.text == "" or self.ids.four.text == "" or self.ids.five.text == "" or self.ids.six.text == "":
            popp.popup(1,"FEHLER","Nicht alle Felder sind richtig ausgefüllt worden")
        elif self.ids.spinner_id.text == "Runde Auswählen":
            popp.popup(1,"FEHLER","Es wurde keine Runde ausgewählt")

        else:
            self.content = self.file.readlines()
            self.content = self.content + ["{},{},{},{},{},{}".format(self.ids.one.text,
                                                                          self.ids.two.text,
                                                                          self.ids.three.text,
                                                                          self.ids.four.text,
                                                                          self.ids.five.text,
                                                                          self.ids.six.text)]
            self.file = open(self.filename,"w")
            self.file.write(str(self.content))
            self.file.close()

class ArcheryApp(App):
    def build(self):
        return sm

    icon = "pictures/icon.png"


class WindowManager(ScreenManager):
    pass

kv = Builder.load_file("my.kv")

sm = WindowManager()

screens = [Home(name="home"),Score1(name="score1")]

for screen in screens:
    sm.add_widget(screen)

sm.current = "home"

if __name__ == '__main__':
    ArcheryApp().run()