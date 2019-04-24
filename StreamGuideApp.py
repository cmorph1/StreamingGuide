from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
import re
import webbrowser
import sqlite3


# Basic screen class
class BaseScreen(Screen):

    def __init__(self, **kwargs):
        super(BaseScreen, self).__init__(**kwargs)
        global screen_frame
        screen_frame = BoxLayout(orientation='vertical')
        self.app_logo = Image(source='StreamGuideLogo.jpg', pos_hint=self._get_position_hint(),
                              size_hint=self._get_size_hint())

    def screen_navigation(self, *args):
        pass

    def _get_position_hint(self):
        pass

    def _get_size_hint(self):
        pass


# Welcome screen - starts naviagetion to functional screen
class WelcomeScreen(BaseScreen):

    def __init__(self, **kwargs):
        super(WelcomeScreen, self).__init__(**kwargs)
        intro_label = Label(text='Welcome to Stream Guide! \n'
                                 'Your personal search engine for the major streaming services.\n'
                                 'Simply enter your username and password for the sites you have a subscription too,\n'
                                 'along with what you want to watch and Stream Guide will do the leg work for you.',
                            halign='center')
        start_button = Button(text='Start', font_size='20sp', pos_hint={'x': .4, 'top': 1}, size_hint=(.2, .15))
        start_button.background_color = [0, 0, 9, 1]
        start_button.bind(on_press=self.screen_navigation)
        space_label = Label(text='')
        screen_frame.add_widget(self.app_logo)
        screen_frame.add_widget(intro_label)
        screen_frame.add_widget(start_button)
        screen_frame.add_widget(space_label)
        self.add_widget(screen_frame)

    def screen_navigation(self, *args):
        self.manager.current = 'user details screen'

    def _get_position_hint(self):
        return{'y': 1, 'x': 0}

    def _get_size_hint(self):
        return .6, .5


# Screen for entering user details
class UserDetailsScreen(BaseScreen):

    def __init__(self, **kwargs):
        super(UserDetailsScreen, self).__init__(**kwargs)
        self.netflixun = None
        self.netflixp = None
        self.amazonun = None
        self.amazonp = None
        self.nowtvun = None
        self.nowtvp = None
        input_frame = GridLayout(cols=3, rows=3, padding=10, spacing=10, row_force_default=True, row_default_height=30)
        enter_details = Label(text='Please enter your username and password for the sites you are registered with \n'
                                   'If you are NOT registered with a service do NOT enter any details! \n'
                                   'If you have already registered your details on this device, '
                                   'no need to bother doing it again')
        self.streamer_name_nf = Label(text="Netflix", font_size='20sp', halign='left', size_hint_x=None, width=150)
        self.username_input_nf = TextInput(text='Username')
        self.password_input_nf = TextInput(text='Password', width=100, password=True)
        self.streamer_name_ap = Label(text="Amazon Prime", font_size='20sp', halign='left', size_hint_x=None, width=150)
        self.username_input_ap = TextInput(text='Username')
        self.password_input_ap = TextInput(text='Password', width=100, password=True)
        self.streamer_name_nt = Label(text="Now TV", font_size='20sp', halign='left', size_hint_x=None, width=150)
        self.username_input_nt = TextInput(text='Username')
        self.password_input_nt = TextInput(text='Password', width=100, password=True)
        input_frame.add_widget(self.streamer_name_nf)
        input_frame.add_widget(self.username_input_nf)
        input_frame.add_widget(self.password_input_nf)
        input_frame.add_widget(self.streamer_name_ap)
        input_frame.add_widget(self.username_input_ap)
        input_frame.add_widget(self.password_input_ap)
        input_frame.add_widget(self.streamer_name_nt)
        input_frame.add_widget(self.username_input_nt)
        input_frame.add_widget(self.password_input_nt)
        self._set_up_submit_button()
        space_label = Label(text='')
        screen_frame.add_widget(self.app_logo)
        screen_frame.add_widget(enter_details)
        screen_frame.add_widget(input_frame)
        screen_frame.add_widget(self.submit_button)
        screen_frame.add_widget(space_label)
        self.add_widget(screen_frame)

    # Submit button which stores user details and moves user to the search screen
    def _set_up_submit_button(self):
        self.submit_button = Button(text='Submit', font_size='20sp', pos_hint={'x': .4, 'top': 1}, size_hint=(.2, .2))
        self.submit_button.background_color = [0, 0, 9, 1]
        self.submit_button.bind(on_press=self.screen_navigation)
        self.submit_button.bind(on_press=self.assign_and_save_input_text)

    # Assigns the users input to a variable so it can be called on and stored in an Sqlite database
    def assign_and_save_input_text(self, *args):
        self.netflixun = self.username_input_nf.text
        self.netflixp = self.password_input_nf.text
        self.amazonun = self.username_input_ap.text
        self.amazonp = self.password_input_ap.text
        self.nowtvun = self.username_input_nt.text
        self.nowtvp = self.password_input_nt.text
        db = sqlite3.connect("userdetails.sqlite")
        db.execute("CREATE TABLE IF NOT EXISTS userdetails "
                   "(streamer TEXT, username VARCHAR, password VARCHAR, PRIMARY KEY (streamer))")
        cursor = db.cursor()
        if self.username_input_nf.text != 'Username':
            cursor.execute("INSERT OR REPLACE INTO userdetails VALUES "
                           "(?, ?, ?)", (self.streamer_name_nf.text, self.netflixun, self.netflixp))
            cursor.connection.commit()
        if self.username_input_ap.text != 'Username':
            cursor.execute("INSERT OR REPLACE INTO userdetails VALUES "
                           "(?, ?, ?)", (self.streamer_name_ap.text, self.amazonun, self.amazonp))
            cursor.connection.commit()
        if self.username_input_nt.text != 'Username':
            cursor.execute("INSERT OR REPLACE INTO userdetails VALUES "
                           "(?, ?, ?)", (self.streamer_name_nt.text, self.nowtvun, self.nowtvp))
            cursor.connection.commit()
        cursor.close()
        db.close()

    def screen_navigation(self, *args):
        self.manager.current = 'search screen'

    def _get_position_hint(self):
        return{'y': 1, 'x': 0.25}

    def _get_size_hint(self):
        return .5, .45


# This is for searching and viewing results
class SearchScreen(BaseScreen):

    def __init__(self, **kwargs):
        super(SearchScreen, self).__init__(**kwargs)
        top_frame = BoxLayout(orientation='vertical')
        search_bar_frame = FloatLayout()
        self.netf_results_frame = None
        self.amap_results_frame = None
        self.ntv_results_frame = None
        self.netf_results = None
        self.ntv_results = None
        self.amap_results = None
        self._search_string = None
        self.netf_box = BoxLayout(orientation='vertical')
        self.amap_box = BoxLayout(orientation='vertical')
        self.ntv_box = BoxLayout(orientation='vertical')
        self.search_input = TextInput(text='Your search', width=400, height=30, size_hint=(None, None),
                                      pos_hint={'x': .25, 'y': 0.8})
        self._setup_search_button()
        back_button = Button(text='Back', font_size='20sp', pos_hint={'x': 0.5, 'y': 0.5}, size_hint=(.2, .25))
        back_button.background_color = [0, 0, 9, 1]
        back_button.bind(on_press=self.screen_navigation)
        search_bar_frame.add_widget(self.search_input)
        search_bar_frame.add_widget(self.search_button)
        search_bar_frame.add_widget(back_button)
        netflix_label = Label(text='Netflix:', font_size='18sp', valign='top')
        self.netf_box.add_widget(netflix_label)
        amazon_label = Label(text='Amazon Prime:', font_size='18sp', valign='top')
        self.amap_box.add_widget(amazon_label)
        nowtv_label = Label(text='Now TV:', font_size='18sp', valign='top')
        self.ntv_box.add_widget(nowtv_label)
        top_frame.add_widget(self.app_logo)
        top_frame.add_widget(search_bar_frame)
        screen_frame.add_widget(top_frame)
        screen_frame.add_widget(self.netf_box)
        screen_frame.add_widget(self.amap_box)
        screen_frame.add_widget(self.ntv_box)
        self.add_widget(screen_frame)

    # Button used to search and reset previous search
    def _setup_search_button(self):
        self.search_button = Button(text='Search', font_size='20sp', pos_hint={'x': 0.3, 'y': 0.5}, size_hint=(.2, .25))
        self.search_button.background_color = [0, 0, 9, 1]
        self.search_button.bind(on_press=self.assign_input_text)
        self.search_button.bind(on_press=self.clear_search)
        self.search_button.bind(on_release=self.check_user_details)

    # This function clears the previous search, so the new links can be added
    def clear_search(self, *args):
        if self.netf_results_frame:
            self.netf_box.remove_widget(self.netf_results_frame)
        if self.ntv_results_frame:
            self.ntv_box.remove_widget(self.ntv_results_frame)
        if self.amap_results_frame:
            self.amap_box.remove_widget(self.amap_results_frame)

    # This enures that only sites where the user has entered details, are searched
    def check_user_details(self, *args):
        db = sqlite3.connect("userdetails.sqlite")
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM userdetails WHERE streamer = 'Netflix'")
        nf_details_check = cursor.fetchone()[0]
        if nf_details_check != 0:
            self.search_netflix()
        cursor.execute("SELECT COUNT(*) FROM userdetails WHERE streamer = 'Now TV'")
        ntv_details_check = cursor.fetchone()[0]
        if ntv_details_check != 0:
            self.search_nowtv()
        cursor.execute("SELECT COUNT(*) FROM userdetails WHERE streamer = 'Amazon Prime'")
        ap_details_check = cursor.fetchone()[0]
        if ap_details_check != 0:
            self.search_amazon()

    # Function to search Netflix
    def search_netflix(self, *args):
        from StreamGuideProgram import Netflix
        self.netf_results_frame = GridLayout(cols=2, rows=5, row_force_default=True, row_default_height=15)
        netflix_search = Netflix()
        self.netf_results = netflix_search.search(self._search_string)
        try:
            for result in self.netf_results:
                results_label = Label(text='[ref={}]{}[/ref]'.format(result[1], result[0]), markup=True)
                results_label.bind(on_ref_press=lambda self,
                                   x: webbrowser.open(re.search('=(.*?)]', self.text).group(1)))
                self.netf_results_frame.add_widget(results_label)
        except TypeError:
            results_label = Label(text="Either your search was incorrect or "
                                       "Netflix doesn't have what you are looking for")
            self.netf_results_frame.add_widget(results_label)
        self.netf_box.add_widget(self.netf_results_frame)

    # Function to search Now TV
    def search_nowtv(self, *args):
        from StreamGuideProgram import NowTV
        nowtv_search = NowTV()
        self.ntv_results_frame = GridLayout(cols=2, rows=5, row_force_default=True, row_default_height=15)
        self.ntv_results = nowtv_search.search(self._search_string)
        try:
            for result in self.ntv_results:
                results_label = Label(text='[ref={}]{}[/ref]'.format(result[1], result[0]), markup=True)
                results_label.bind(on_ref_press=lambda self,
                                   x: webbrowser.open(re.search('=(.*?)]', self.text).group(1)))
                self.ntv_results_frame.add_widget(results_label)
        except IndexError:
            results_label = Label(text=self.ntv_results)
            self.ntv_results_frame.add_widget(results_label)
        self.ntv_box.add_widget(self.ntv_results_frame)

    # Function to search Amazon Prime
    def search_amazon(self, *args):
        from StreamGuideProgram import Amazon
        amazon_search = Amazon()
        self.amap_results_frame = GridLayout(cols=2, rows=5, row_force_default=True, row_default_height=15)
        self.amap_results = amazon_search.search(self._search_string)
        for result in self.amap_results:
            results_label = Label(text='[ref={}]{}[/ref]'.format(result[1], result[0]), markup=True)
            results_label.bind(on_ref_press=lambda self,
                               x: webbrowser.open(re.search('=(.*?)]', self.text).group(1)))
            self.amap_results_frame.add_widget(results_label)
        self.amap_box.add_widget(self.amap_results_frame)

    # Assigns the users search to a variable to be used in the searching Methonds
    def assign_input_text(self, *args):
        self._search_string = self.search_input.text

    def screen_navigation(self, *args):
        self.manager.current = 'user details screen'

    def _get_position_hint(self):
        return{'y': 1, 'x': 0.055}

    def _get_size_hint(self):
        return .9, .9


class MyApp(App):

    def build(self):
        app_manager = ScreenManager()
        welcome_screen = WelcomeScreen(name='welcome screen')
        user_details_screen = UserDetailsScreen(name='user details screen')
        search_screen = SearchScreen(name='search screen')
        app_manager.add_widget(welcome_screen)
        app_manager.add_widget(user_details_screen)
        app_manager.add_widget(search_screen)
        return app_manager


if __name__ == '__main__':
    MyApp().run()
