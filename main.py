from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, StringProperty, ListProperty
from kivy.properties import ObjectProperty, StringProperty, partial
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.dropdown import DropDown
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty
import database
import re



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
                pop_results('Invalid Form','Please fill in all inputs with valid information.')
        else:
            pop_results('Invalid Form','Please fill in all inputs with valid information.')

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
            pop_results('Invalid Login','Invalid username or password.')

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
        name, password, email = database.get_user(self.current)
        self.name1.text = "Account Name: " + name
        self.email.text = "Email: " + email


class WindowManager(ScreenManager):
    def update_args(self,item):
        self.item=item


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

    """ Inits the dropDowns"""

    def __init__(self, **kwargs):
        super(PublishWindow, self).__init__(**kwargs)
        self.dropdown = CustomDropDown1(self)
        self.dropdown2 = CustomDropDown2(self)
        self.dropdown3 = CustomDropDown3(self)

    def open_drop_down(self, widget):
        self.dropdown.open(widget)

    def open_drop_down2(self, widget):
        self.dropdown2.open(widget)

    def open_drop_down3(self, widget):
        self.dropdown3.open(widget)

    """ This function check if the input is valid and then send to the DB class where it will be added to the DB"""
    """ This function calls to the popup function according to the result of the query"""

    def publishItem(self):
        if (
                self.itemName.text != "" and self.amount.text != "Show possibilities" and self.location.text != "Show possibilities"
                and self.category.text != "Show possibilities" and MainWindow.current != ""):
            ok = database.add_item_to_user(MainWindow.current, self.itemName.text, self.amount.text, self.location.text,
                                           self.category.text)
            if ok:  # the item was added to the db successfully
                pop_results("Message:", "A new item has been added")
                self.itemName.text = ""
                self.amount.text = "Show possibilities"
                self.location.text = "Show possibilities"
                self.category.text = "Show possibilities"
            else:  # something went wrong with the insertion
                pop_results("Message:", "OOPS! Something went wrong! \n Please try again later")
                self.itemName.text = ""
                self.amount.text = "Show possibilities"
                self.location.text = "Show possibilities"
                self.category.text = "Show possibilities"
        else:  # input is not valid
            pop_results("Message:", "Please fill in all the boxes")
            self.itemName.text = ""
            self.amount.text = "Show possibilities"
            self.location.text = "Show possibilities"
            self.category.text = "Show possibilities"


class MyPostsWindow(Screen):
    btnRemove = ObjectProperty(None)
    currentItem = ObjectProperty(None)

    def on_enter(self, *args):
        posts = database.get_posts_by_user(MainWindow.current)
        if len(posts) == 0:
            pop_results("Message:", "You haven't posted anything yet")
        else:
            index_x=0.1
            index_y=0.7
            for i in posts:
                item =re.sub("[('),]", '', str(i[0]))
                details = "amount: " + re.sub("[('),]", '', str(i[1])) + ", location: " + re.sub("[('),]", '', str(i[3])) +", "
                t_or_f = re.sub("[('),]", '', str(i[5]))
                if(t_or_f=="TRUE"):
                    details= details +"Taken"
                else:
                    details= details+ "Available"
                self.button = Button(text=item, on_press=self.choose_item,size_hint=(0.2,0.1),
                                pos_hint=({"x":index_x, "y": index_y}))
                self.add_widget(self.button)
                label = Label(text=details,size_hint=(0.2,0.1),
                                pos_hint=({"x":index_x+0.05, "y": index_y-0.1}) )
                self.add_widget(label)
                index_y-=0.2


    def choose_item(self,instance):
        self.parent.update_args(instance)
        self.parent.current="updateItemWindow"
        print(instance.text)

    def back_main(self):
        self.parent.current = "main"

class updateItemWindow(Screen):
    amount = ObjectProperty(None)
    location = ObjectProperty(None)
    item = ObjectProperty(None)
    nameI= ObjectProperty(None)

    button_text3 = StringProperty('Show possibilities')
    button_text2 = StringProperty('Show possibilities')

    """ Inits the dropDowns"""

    def __init__(self, **kwargs):
        super(updateItemWindow, self).__init__(**kwargs)
        self.dropdown2 = CustomDropDown2(self)
        self.dropdown3 = CustomDropDown3(self)
        # self.item = self.parent.item.text
        # print(self.parent.item.text)
        # self.nameI.text = self.nameI + self.item

    def on_enter(self, *args):
        self.item = self.parent.item.text
        self.nameI.text = "Item's Name: " + self.item

    def open_drop_down2(self, widget):
        self.dropdown2.open(widget)


    def open_drop_down3(self, widget):
        self.dropdown3.open(widget)

    def updateItem(self):
        if (
                self.amount.text != "Show possibilities" and self.location.text != "Show possibilities"
                and self.item!= "" and MainWindow.current != ""):
            ok = database.update(MainWindow.current, self.item, self.amount.text, self.location.text)
            if ok:  # the item was added to the db successfully
                pop_results("Message:", "The item updated successfully")
                self.parent.current = "main"
            else:
                pop_results("Message: ", "OOPS! Please try again later.")
                self.parent.current = "main"
        else:
            pop_results("Message:", "Please fill in all the boxes")
            self.amount.text=""
            self.location.text=""

class SearchWindow(Screen):
    category = ObjectProperty(None)
    location = ObjectProperty(None)
    result = ObjectProperty(None)
    button_text = StringProperty('Show possibilities')
    button_text2 = StringProperty('Show possibilities')
    button_text3 = StringProperty('Show possibilities')

    def __init__(self, **kwargs):
        super(SearchWindow, self).__init__(**kwargs)
        self.dropdown = CustomDropDown1(self)
        self.dropdown2 = CustomDropDown2(self)


    def open_drop_down(self, widget):
        self.dropdown.open(widget)

    def open_drop_down2(self, widget):
        self.dropdown2.open(widget)


    def Search(self):
        text = ""
        if self.category.text == "Show possibilities" or self.location.text == "Show possibilities":
            pop_results('Invalid Search', 'Please choose from the options')
        else:
            list = database.search(self.category.text, self.location.text)
            if list == "no results":
                self.result.text = list
            else:
                for line in list:
                    text = text + str(line[0]) + " " + str(line[1]) + " " + str(line[2]) + " " + str(line[3]) + " " \
                           + str(line[4]) + " " +  str(line[5]) + "\n"
                self.result.text = text



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

class DataWindow(Screen):
    pass

def invalidLogin():
    pop = Popup(title='Invalid Login',
                content=Label(text='Invalid username or password.'),
                size_hint=(None, None), size=(400, 400))

    pop.open()
    """ This function shows popups according to a message"""


def pop_results(title, results):
    layout = GridLayout(cols=1, padding=10)
    popupLabel = Label(text=results)
    layout.add_widget(popupLabel)
    closeButton = Button(text="Close the pop-up")
    layout.add_widget(closeButton)
    pop = Popup(title=title,
                content=layout,
                size_hint=(None, None), size=(400, 400))

    pop.open()
    closeButton.bind(on_press=pop.dismiss)


def invalidForm():
    pop = Popup(title='Invalid Form',
                content=Label(text='Please fill in all inputs with valid information.'),
                size_hint=(None, None), size=(400, 400))

    pop.open()



kv = Builder.load_file("my.kv")

sm = WindowManager()
# db = DataBase("users.txt")

screens = [LoginWindow(name="login"), CreateAccountWindow(name="create"), MainWindow(name="main"),
           SearchWindow(name="SearchPage"), AboutWindow(name="AboutPage"), DataWindow(name="DataPage"), PublishWindow(name="publish"),
           MyPostsWindow(name="MyPostsWindow"), updateItemWindow(name="updateItemWindow")]


for screen in screens:
    sm.add_widget(screen)

sm.current = "login"


class MyMainApp(App):
    def build(self):
        return sm


if __name__ == "__main__":
    database = database.DataBase()
    MyMainApp().run()


""" Dynamic buttons - instead of posts do your function"""

""""
      posts = database.get_posts_by_user(MainWindow.current)
        if len(posts) == 0:
            pop_results("Message:", "You haven't posted anything yet")
            button = Button(text="Back", on_press=lambda x: self.back_main(), size_hint=(0.2, 0.1),
                            pos_hint=({"x":0.4, "y": 0.0}))
            self.add_widget(button)
        else:
            index_x=0.5
            index_y=0.5
            for i in posts:
                item =re.sub("[('),]", '', str(i[0]))
                t_or_f = re.sub("[('),]", '', str(i[1]))
                taken=""
                if(t_or_f=="TRUE"):
                    taken="Taken"
                else:
                    taken="Available"
                label = Label(text=item,size_hint=(0.2,0.1),
                                pos_hint=({"x":index_x-0.2, "y": index_y}) )
                self.add_widget(label)
                self.button = Button(text=taken, on_press=self.take_item,size_hint=(0.2,0.1),
                                pos_hint=({"x":index_x, "y": index_y}))
                self.add_widget(self.button)
                button = Button(text="Back", on_press=lambda x: self.back_main(), size_hint=(0.2, 0.1),
                                pos_hint=({"x": 0.4, "y": 0.0}))
                self.add_widget(button)
                index_y-=0.1"""

"""
    def take_item(self,instance):
        if instance.text=="Available":
            instance.text="Taken"
            database.update_taken(MainWindow.current, self.text1, "TRUE")
        else:
            instance.text="Available"""