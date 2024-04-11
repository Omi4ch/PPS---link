from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.recycleview import RecycleView
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.config import ConfigParser
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.metrics import dp
from datetime import datetime
import os
import ast
import time
import g4f


class MenuScreen(Screen):
    def __init__(self, **kw):
        super(MenuScreen, self).__init__(**kw)
        box = BoxLayout(orientation='vertical')
        box.add_widget(Button(text='Найти полезную ссылку', on_press=lambda x:
                              set_screen('Poisk')))
        box.add_widget(Button(text='Ваши последние запросы',
                              on_press=lambda x: set_screen('Zaprosi')))
        self.add_widget(box)


class HistoryZapros(Screen):
    def __init__(self, **kw):
        super(HistoryZapros, self).__init__(**kw)

    def on_enter(self): 

        self.LinkHis = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.LinkHis.bind(minimum_height=self.LinkHis.setter('height'))
        back_button = Button(text='< Назад в главное меню',
                             on_press=lambda x: set_screen('menu'),
                             size_hint_y=None, height=dp(40))
        self.LinkHis.add_widget(back_button)
        root = RecycleView(size_hint=(1, None), size=(Window.width,
                                                      Window.height))
        root.add_widget(self.LinkHis)
        self.add_widget(root)

        Linki = ast.literal_eval(
            App.get_running_app().config.get('General', 'user_data'))

        
        
        
        

    def on_leave(self):  

        self.LinkHis.clear_widgets() 


class PoiskLink(Screen):

    def buttonClicked(self, btn1):
        if not self.txt1.text:
            return
        self.app = App.get_running_app()
        self.app.user_data = ast.literal_eval(
            self.app.config.get('General', 'user_data'))
        self.app.user_data[self.txt1.text.encode('u8')] = int(time.time())

        self.app.config.set('General', 'user_data', self.app.user_data)
        self.app.config.write()

        text = "Ссылки:  " + self.txt1.text
        self.result.text = text
        self.txt1.text = ''

    def __init__(self, **kw):
        super(PoiskLink, self).__init__(**kw)
        box = BoxLayout(orientation='vertical')
        back_button = Button(text='< Назад в главное меню', on_press=lambda x:
                             set_screen('menu'), size_hint_y=None, height=dp(40))
        box.add_widget(back_button)
        self.txt1 = TextInput(text='', multiline=False, height=dp(40),
                              size_hint_y=None, hint_text="Тема")
        box.add_widget(self.txt1)
        btn1 = Button(text="Поиск", size_hint_y=None, height=dp(40))
        btn1.bind(on_press=self.buttonClicked)
        box.add_widget(btn1)
        self.result = Label(text='')
        box.add_widget(self.result)
        self.add_widget(box) 


def set_screen(name_screen):
    sm.current = name_screen


sm = ScreenManager()
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(HistoryZapros(name='Zaprosi'))
sm.add_widget(PoiskLink(name='Poisk'))


class FoodOptionsApp(App):
    def __init__(self, **kvargs):
        super(FoodOptionsApp, self).__init__(**kvargs)
        self.config = ConfigParser()

    def build_config(self, config):
        config.adddefaultsection('General')
        config.setdefault('General', 'user_data', '{}')

    def set_value_from_config(self):
        self.config.read(os.path.join(self.directory, '%(appname)s.ini'))
        self.user_data = ast.literal_eval(self.config.get(
            'General', 'user_data'))

    def get_application_config(self):
        return super(FoodOptionsApp, self).get_application_config(
            '{}/%(appname)s.ini'.format(self.directory))

    def build(self):
        return sm


if __name__ == '__main__':
    FoodOptionsApp().run()