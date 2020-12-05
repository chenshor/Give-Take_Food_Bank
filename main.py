from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.dropdown import DropDown
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty
import database



class CreateAccountWindow(Screen):
    nameUser = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def submit(self):
        if self.nameUser.text != "" and self.email.text != "" and self.email.text.count(
                "@") == 1 and self.email.text.count(".") > 0 \
                and (all(x.isalpha() or x.isspace() for x in self.nameUser.text)):
            if self.password != "":
                database.add_user(self.email.text, self.password.text, self.nameUser.text)

                self.reset()

                sm.current = "login"
            else:
                invalidForm()
        else:
            invalidForm()

    def login(self):
        self.reset()
        sm.current = "login"

    def reset(self):
        self.email.text = ""
        self.password.text = ""
        self.nameUser.text = ""


class LoginWindow(Screen):
    name1 = ObjectProperty(None)
    password = ObjectProperty(None)

    def loginBtn(self):
        if database.validate(self.name1.text, self.password.text):
            MainWindow.current = self.name1.text
            self.reset()
            sm.current = "main"
        else:
            invalidLogin()

    def createBtn(self):
        self.reset()
        sm.current = "create"

    def reset(self):
        self.name1.text = ""
        self.password.text = ""

""" This class represents the main page of our app where users can publish and search for items"""
class MainWindow(Screen):
    name1 = ObjectProperty(None)
    email = ObjectProperty(None)
    current = ""

    def logOut(self):
        sm.current = "login"

    def on_enter(self, *args):
        name,password, email = database.get_user(self.current)
        self.name1.text = "Account Name: " + name
        self.email.text = "Email: " + email


class WindowManager(ScreenManager):
    pass


""" This Class represents the publish page where users can publish new items"""
class PublishWindow(Screen):
    email = ObjectProperty(None)
    itemName = ObjectProperty(None)
    amount = ObjectProperty(None)
    location = ObjectProperty(None)
    category = ObjectProperty(None)

    button_text = StringProperty('Show possibilities')
    button_text2 = StringProperty('Show possibilities')
    button_text3 = StringProperty('Show possibilities')

    def __init__(self, **kwargs):
        super(PublishWindow, self).__init__(**kwargs)
        self.dropdown = CustomDropDown1(self)
        self.dropdown2 = CustomDropDown2(self)
        self.dropdown3 = CustomDropDown3(self)

    def open_drop_down(self, widget):
        self.dropdown.open(widget)

    def open_drop_down3(self, widget):
        self.dropdown3.open(widget)

class MyPostsWindow(Screen):
    pass


    def open_drop_down2(self, widget):
        self.dropdown2.open(widget)

class SearchWindow(Screen):
    email = ObjectProperty(None)
    category = ObjectProperty(None)
    location = ObjectProperty(None)

    button_text = StringProperty('Show possibilities')
    button_text2 = StringProperty('Show possibilities')

    def __init__(self, **kwargs):
        super(SearchWindow, self).__init__(**kwargs)
        self.dropdown = CustomDropDown1(self)
        self.dropdown2 = CustomDropDown2(self)

    def open_drop_down(self, widget):
        self.dropdown.open(widget)

    def open_drop_down2(self, widget):
        self.dropdown2.open(widget)

class CustomDropDown1(DropDown):
    def __init__(self, screen_manager, **kwargs):
        super(CustomDropDown1, self).__init__(**kwargs)
        self.sm = screen_manager
        self.is2Displayed = False

    def on_select(self, data):
        self.sm.button_text = data

class CustomDropDown2(DropDown):
    def __init__(self, screen_manager, **kwargs):
        super(CustomDropDown2, self).__init__(**kwargs)
        self.sm = screen_manager
        self.is2Displayed = False

    def on_select(self, data):
        self.sm.button_text2 = data

class CustomDropDown3(DropDown):
    def __init__(self, screen_manager, **kwargs):
        super(CustomDropDown3, self).__init__(**kwargs)
        self.sm = screen_manager
        self.is2Displayed = False

    def on_select(self, data):
        self.sm.button_text3 = data


class AboutWindow(Screen):
    pass


def invalidLogin():
    pop = Popup(title='Invalid Login',
                content=Label(text='Invalid username or password.'),
                size_hint=(None, None), size=(400, 400))
    pop.open()


def invalidForm():
    pop = Popup(title='Invalid Form',
                content=Label(text='Please fill in all inputs with valid information.'),
                size_hint=(None, None), size=(400, 400))

    pop.open()


kv = Builder.load_file("my.kv")

sm = WindowManager()
# db = DataBase("users.txt")

screens = [LoginWindow(name="login"), CreateAccountWindow(name="create"), MainWindow(name="main"),
           SearchWindow(name="SearchPage"), AboutWindow(name="AboutPage"), PublishWindow(name="publish"),
           MyPostsWindow(name="MyPosts")]

for screen in screens:
    sm.add_widget(screen)

sm.current = "login"


class MyMainApp(App):
    def build(self):
        return sm


if __name__ == "__main__":
    database=database.DataBase()
    MyMainApp().run()
