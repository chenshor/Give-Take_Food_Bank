import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserIconView
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

from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
import matplotlib.pyplot as plt


class StartWindow(Screen):
    pass




""" In this class we create an account to new users"""
class CreateAccountWindow(Screen):
    nameUser = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    """ This function submits the input from the user and sends it to the database class"""
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

    """ This function takes the user back to the login  screen"""
    def login(self):
        self.reset()
        sm.current = "login"

    """ This function resets the test inputs"""
    def reset(self):
        self.email.text = ""
        self.password.text = ""
        self.nameUser.text = ""

""" In this class the user log in to our system"""
class LoginWindow(Screen):
    name1 = ObjectProperty(None)
    password = ObjectProperty(None)

    """ This function takes the user input and sends it to the database class where
     the information will be checked. If the information is valid, the menu screen will be presented,
     otherwise, an error message will be presented"""
    def loginBtn(self):
        if database.validate(self.name1.text, self.password.text):
            MainWindow.current = self.name1.text
            self.reset()
            sm.current = "main"
        else:
            pop_results('Invalid Login','Invalid username or password.')

    """ This function go back to the create an account screen"""
    def createBtn(self):
        self.reset()
        sm.current = "create"

    """ This function resets the data inputs"""
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
        # self.name1.text = "Hello: " + name + "!"
        self.name1.text = 'Welcome '+name+'!'
        self.name1.background_color=(0, 0, 1,  1)

class WindowManager(ScreenManager):
    def update_args(self,item):
        self.item=item

    def update_category(self,item):
        self.category=item

    def update_location(self,item):
        self.location=item

    def update_results(self,item):
        self.results=item


""" This Class represents the publish page where users can publish new items"""
class PublishWindow(Screen):
    email = ObjectProperty(None)
    itemName = ObjectProperty(None)
    amount = ObjectProperty(None)
    location = ObjectProperty(None)
    category = ObjectProperty(None)

    """ Initialize the drop-downs"""
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

""" In this class we presents all the posts the user published"""
class MyPostsWindow(Screen):
    btnRemove = ObjectProperty(None)
    currentItem = ObjectProperty(None)

    """This function presents the user's posts """
    def on_enter(self, *args):
        posts = database.get_posts_by_user(MainWindow.current)
        if len(posts) == 0: # the user havent published anything yet
            pop_results("Message:", "You haven't posted anything yet")
        else: # the user published items
            # initialize the positions of the items
            index_x=0.1
            index_y=0.65
            counter=1
            first = True
            for i in posts:
                if (counter > 3): # if true, we change the positions of the items
                    counter += 1
                    index_x = 0.6
                    index_y = 0.65
                    if not first:
                        index_y -= 0.2
                    first = False
                # parse the items from the query
                item =re.sub("[('),]", '', str(i[0]))
                details = "amount: " + re.sub("[('),]", '', str(i[1])) + ", location: " + re.sub("[('),]", '', str(i[3])) +", "
                t_or_f = re.sub("[('),]", '', str(i[5]))
                if(t_or_f=="TRUE"): # checks if the items is taken or not
                    details= details +"Taken"
                else:
                    details= details+ "Available"
                self.button = Button(text=item, on_press=self.choose_item,size_hint=(0.15,0.15),
                                     background_normal= "images/cir.png",
                background_down= "images/cir.png",
                                pos_hint=({"x":index_x, "y": index_y}))
                self.add_widget(self.button)
                label = Label(text=details,size_hint=(0.2,0.1), color= (.2, .1, .73, 1),
                                pos_hint=({"x":index_x+0.05, "y": index_y-0.05}) )
                self.add_widget(label)
                index_y-=0.2
                counter+=1

    """ This function saves the item that has been pressed and send it to the "update page"""
    def choose_item(self,instance):
        self.parent.update_args(instance)
        self.clear_widgets();
        #build the page all over again
        label = Label(text="My Posts", size_hint=(0.8, 0.2), color=(.2, .1, .73, 1),
                      pos_hint=({"x":0.07, "top":1.05}),font_size=(self.parent.width**2 + self.parent.height**2) / 14**4)
        self.add_widget(label)
        label = Label(text="Please choose the Item that you want to update:", size_hint=(0.8, 0.2),color=(.2, .1, .73, 1),
                      pos_hint=({"x":-0.05, "top":0.95}), font_size=(self.parent.width**2 + self.parent.height**2) / 14**4)
        self.add_widget(label)
        self.button = Button(text="Back", on_press=self.back_main, size_hint=(0.15, 0.15),
                             background_normal="images/green.png",
        background_down= "images/green.png",
                             pos_hint=({"x":0.4, "y": 0.0}))
        self.add_widget(self.button)
        self.parent.current = "updateItemWindow"

    """ This function takes us back to the main page"""
    def back_main(self,instance):
        self.parent.current = "main"

""" In this class we update an existing item"""
class updateItemWindow(Screen):
    amount = ObjectProperty(None)
    location = ObjectProperty(None)
    item = ObjectProperty(None)
    nameI= ObjectProperty(None)

    """ Initialize the dropDowns"""
    button_text3 = StringProperty('Show possibilities')
    button_text2 = StringProperty('Show possibilities')
    def __init__(self, **kwargs):
        super(updateItemWindow, self).__init__(**kwargs)
        self.dropdown2 = CustomDropDown2(self)
        self.dropdown3 = CustomDropDown3(self)


    def on_enter(self, *args):
        self.item = self.parent.item.text
        self.nameI.text = "Item's Name: " + self.item

    def open_drop_down2(self, widget):
        self.dropdown2.open(widget)


    def open_drop_down3(self, widget):
        self.dropdown3.open(widget)

    """ This function updates the information about an item"""
    def updateItem(self):
        if (
                # check if the input is valid
                self.amount.text != "Show possibilities" and self.location.text != "Show possibilities"
                and self.item!= "" and MainWindow.current != ""):
            ok = database.update(MainWindow.current, self.item, self.amount.text, self.location.text)
            if ok:  # the item was added to the db successfully
                pop_results("Message:", "The item updated successfully")
                button_text3 = StringProperty('Show possibilities')
                button_text2 = StringProperty('Show possibilities')
                self.parent.current = "main"
            else: # something went wrong with the database
                pop_results("Message: ", "OOPS! Please try again later.")
                self.parent.current = "main"
        else: # the information is not valid
            pop_results("Message:", "Please fill in all the boxes")
            self.amount.text=""
            self.location.text=""

""" This class represents the search of an item by users"""
class SearchWindow(Screen):
    category = ObjectProperty(None)
    location = ObjectProperty(None)
    result = ObjectProperty(None)
    item=""
    list_products=[]
    button_text = StringProperty('Show possibilities')
    button_text2 = StringProperty('Show possibilities')
    curr_item=""

    def __init__(self, **kwargs):
        super(SearchWindow, self).__init__(**kwargs)
        self.dropdown = CustomDropDown1(self)
        self.dropdown2 = CustomDropDown2(self)


    def open_drop_down(self, widget):
        self.dropdown.open(widget)

    def open_drop_down2(self, widget):
        self.dropdown2.open(widget)

    def Back(self):
        self.button_text="Show possibilities"
        self.button_text2="Show possibilities"
        self.result.text=""

    """This function search in the database according to the input and send the output to the show results page """
    def Search(self):
        text = ""
        # invalid input
        if self.category.text == "Show possibilities" and self.location.text == "Show possibilities":
            pop_results('Invalid Search', 'Please choose at least one from the options')
        else: # no matching results
            list = database.search(self.category.text, self.location.text)
            if list == "No matching results!":
                self.result.text = list
            else: # updating the data
                self.parent.update_results(list)
                self.parent.update_category(self.button_text)
                self.parent.update_location(self.button_text2)
                self.list_products = list
                self.go_to_show_results()

    """This function clears the drop downs and goes to the show results page """
    def go_to_show_results(self):
        self.button_text = "Show possibilities"
        self.button_text2 = "Show possibilities"
        self.result.clear_widgets()
        self.parent.current = "show_results"

"""This class represents the result page where all the items that matched the search will be shown"""
class show_results(Screen):

    """This function displays the results of the search"""
    def on_enter(self, *args):
        category = self.parent.category
        location = self.parent.location
        results = self.parent.results
        if category=="Show possibilities":
            category="None"
        elif location=="Show possibilities":
            location="None"
        label1 = Label(text="Results:", size_hint=(0.2, 0.3),color=(.2, .1, .73, 1),
                                              pos_hint=({"x": 0.4, "y": 0.8}),
                       font_size= (self.parent.width**2 + self.parent.height**2) / 14**4)
        self.add_widget(label1)
        text = "Category: " + category + ", Location: " + location
        label2 = Label(text=text,size_hint=(0.2, 0.2),color=(.2, .1, .73, 1),
                                              pos_hint=({"x": 0.2, "y": 0.77}))
        self.add_widget(label2)
        # initialize the positions of the items
        index_x = 0.2
        index_y = 0.7
        for item in results:
            # displays each item
            text = str(item[0]) + " - Amount: " + str(item[1]) + " - Category: " + str(
                    item[2]) + " - Location: " + str(item[3]) + " - User: " + str(item[4]) + "\n"
            result_label = Label(text=text, size_hint=(0.2, 0.1),color=(.2, .1, .73, 1),
                                 pos_hint=({"x": index_x + 0.05, "y": index_y}))
            self.add_widget(result_label)
            self.curr_item = str(item[0])
            if str(item[5]) == "FALSE": # the item was not taken
                popupButton = Button(text="Available", text_language=str(item[0]), on_press=self.take_item,
                                     size_hint=(0.2, 0.05),pos_hint=({"x": index_x + 0.55, "y": index_y+0.03}))
                self.add_widget(popupButton)
            else: # the item has been taken
                popupButton = Button(text="Taken", text_language=str(item[0]), disabled=True,
                                     size_hint=(0.2, 0.05),pos_hint=({"x": index_x + 0.55, "y": index_y+0.03}))
                self.add_widget(popupButton)
            index_y -= 0.1
        back_btn = Button(text="Go back to search",on_press=self.back_search,
                          pos_hint=({"x":0.2, "y": 0.0}) ,size_hint=(0.2, 0.1))
        self.add_widget(back_btn)
        back_btn2 = Button(text="Menu",on_press=self.back_main,
                           pos_hint=({"x": 0.6, "y": 0.0}),size_hint=(0.2, 0.1))
        self.add_widget(back_btn2)

    """This function takes us back to the main page"""
    def back_main(self,instance):
        self.clear_widgets()
        self.parent.current = "main"

    """ This function takes us back to the search page"""
    def back_search(self,instance):
        self.clear_widgets()
        self.parent.current = "SearchPage"

    # def pop_search_results(self, results):
    #     layout = GridLayout(cols=2, padding=10)
    #
    #     for i in range(len(results)):
    #
    #         line=results[i]
    #         if str(line[5]) == "FALSE":
    #             text = str(line[0]) + " - Amount: " + str(line[1]) + " - Category: " + str(line[2]) + " - Location: " + str(line[3]) + " - User: " + str(line[4]) + "\n"
    #             popupLabel = Label(text=text)
    #             layout.add_widget(popupLabel)
    #             self.curr_item=str(line[0])
    #             popupButton = Button(text="Available",text_language=str(line[0]), on_press=self.take_item, size_hint=(0.2, 0.05))
    #             layout.add_widget(popupButton)
    #     closeButton = Button(text="Close the pop-up",size_hint=(0.1, 0.1))
    #     layout.add_widget(closeButton)
    #     pop = Popup(title="RESULTS",
    #                 content=layout,
    #                 size_hint=(None, None), size=(800, 600))
    #
    #     pop.open()
    #     closeButton.bind(on_press = pop.dismiss)
    """ This function update the specific item to "taken"""""
    def take_item(self, instance):
        if instance.text == "Available":
            instance.text = "Taken"
            instance.disabled=True
            database.update_taken(instance.text_language, "TRUE")
        else:
            instance.text = "Available"

""" This class represents the drop down of the category"""
class CustomDropDown1(DropDown):
    def __init__(self, screen_manager, **kwargs):
        super(CustomDropDown1, self).__init__(**kwargs)
        self.sm = screen_manager
        self.is2Displayed = False

    def on_select(self, data):
        self.sm.button_text = data

""" This class represents the drop down of the location"""
class CustomDropDown2(DropDown):
    def __init__(self, screen_manager, **kwargs):
        super(CustomDropDown2, self).__init__(**kwargs)
        self.sm = screen_manager
        self.is2Displayed = False

    def on_select(self, data):
        self.sm.button_text2 = data

""" This class represents the drop down of the amount"""
class CustomDropDown3(DropDown):
    def __init__(self, screen_manager, **kwargs):
        super(CustomDropDown3, self).__init__(**kwargs)
        self.sm = screen_manager
        self.is2Displayed = False

    def on_select(self, data):
        self.sm.button_text3 = data

class CustomDropDown4(DropDown):
    def __init__(self, screen_manager, **kwargs):
        super(CustomDropDown4, self).__init__(**kwargs)
        self.sm = screen_manager
        self.is2Displayed = False

    def on_select(self, data):
        self.sm.button_text4 = data


class AboutWindow(Screen):
    pass

class DataWindow(Screen):
    data=[]
    isShow=False
    button_text4 = StringProperty('Show possibilities')

    def __init__(self, **kwargs):
        super(DataWindow, self).__init__(**kwargs)
        self.dropdown4 = CustomDropDown4(self)

    def open_drop_down(self, widget):
        self.dropdown4.open(widget)

    def show_graphs(self):
        if self.button_text4=='Show possibilities':
            pop_results("invalid input", "invalid input, you must choose an option")
        else:
            # if self.isShow:
            #     self.isShow = False
            #     self.canvas.clear()
            #     self.__init__()
            #
            # else:
            #     self.isShow = True
            x = []
            y = []
            self.data = []
            plt.clf()
            if self.button_text4=='Location':
                self.data=database.get_data_on_location()
                for i in self.data:
                    x.append(i[0])
                    y.append(i[1])
                plt.bar(x, y)
                plt.ylabel('Amounts')
                plt.title('Amounts by location')

            elif self.button_text4 == 'Category':
                self.data = database.get_data_on_category()
                for i in self.data:
                    x.append(i[0])
                    y.append(i[1])
                plt.plot(x, y)
                plt.ylabel('Amounts')
                plt.title('Amounts by category')
            else:
                self.data = database.get_data_on_amounts()
                for i in self.data:
                    x.append(i[0])
                    y.append(i[1])
                fig = plt.figure()
                ax = fig.add_axes([0, 0, 1, 1])
                ax.axis('equal')
                ax.set_title("Distribution of quantities")
                ax.pie(y, labels=x, autopct='%1.2f%%')

            welcomePage = FloatLayout()
            box = BoxLayout(orientation='vertical', size_hint=(0.95, 0.5),
                            padding=8, pos_hint={'top': 0.7, 'center_x': 0.5})

            box.add_widget(FigureCanvasKivyAgg(plt.gcf()))

            welcomePage.add_widget(box)
            self.add_widget(welcomePage)

            # x = []
            # y = []
            # self.data = database.get_data_on_category()
            # for i in self.data:
            #     x.append(i[0])
            #     y.append(i[1])
            # plt.bar(x, y)
            # welcomePage = FloatLayout()
            # box = BoxLayout(orientation='vertical', size_hint=(0.5, 0.5),
            #                 padding=8, pos_hint={'top': 0.7, 'center_x': 0.7})
            #
            # box.add_widget(FigureCanvasKivyAgg(plt.gcf()))
            #
            # welcomePage.add_widget(box)
            # self.add_widget(welcomePage)

    def Back(self):
        self.data=[]
        self.button_text4 = 'Show possibilities'
        self.canvas.clear()
        self.__init__()


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

screens = [StartWindow(name="StartWindow"),LoginWindow(name="login"), CreateAccountWindow(name="create"), MainWindow(name="main"),
           SearchWindow(name="SearchPage"), AboutWindow(name="AboutPage"), DataWindow(name="DataPage"),
           PublishWindow(name="publish"),show_results(name="show_results"),
           MyPostsWindow(name="MyPostsWindow"), updateItemWindow(name="updateItemWindow")
           ]


for screen in screens:
    sm.add_widget(screen)

sm.current = "StartWindow"


class MyMainApp(App):
    def build(self):
        return sm


if __name__ == "__main__":
    database = database.DataBase()
    MyMainApp().run()


